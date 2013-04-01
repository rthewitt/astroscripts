from subprocess import call
import myutil
import notify
import provision
#import LookupError

class Tutorial(object):
   pass
   
class Command(object):
   
   def __init__(self, context):
      super(Command, self).__init__()
      self.course_uuid = context['courseUUID']
      self.prototype = context['prototype']
      self.command_id = '' if not 'id' in context else context['id']

   # we could just use __call__, but I don't want inheritance
   # I want implementation
   def do(self):
      raise LookupError('Action not not implemented')



class InitCommand(Command):
   """ This command is issued when we want to create a course, regardless of professor's existence.
       (bot may be used) """

   setup_script = "./setup-class-branches.sh"

   def __init__(self, context):
      super(InitCommand, self).__init__(context)
      self.students = context['students']

   def do(self):
      print "INSIDE"
      try:
         call([ self.setup_script, self.course_uuid, self.prototype['repository'], self._get_students_as_string() ])
         notify.send_receipt({'status':'success', 'type':'INITIALIZE', 'courseUUID': self.course_uuid, 'id':self.command_id})
      except Exception, fu:
         notify.send_receipt({'status':'failure', 'type':'INITIALIZE', 'courseUUID': self.course_uuid, 'id':self.command_id, 'message': str(fu)})

   def _get_students_as_string(self):
      return " ".join([str(s['studentId']) for s in self.students])

class ProvisionCommand(Command):
   """ This command is used to spin up virtual machines for the purpose of authoring, student work or general tutorials.
       Current provider is AWS via Boto """

   def __init__(self, context):
      super(ProvisionCommand, self).__init__(context)
      self.token = context["token"]
      self.init_ref = context["initRef"]
      self.student_ids = context["studentIds"]
      if len(self.command_id) < 1:
         self.command_id = self.token
      self.image_type = context["type"]

   def do(self):
      print "Starting provision with Boto for image type", self.image_type, "and token", self.token, "with students", " ".join(self.student_ids)
      try:
         reservation = provision.provision_boto(self.image_type, self.student_ids, self.init_ref, self.token)
         print "boto reservation received:", reservation
         print "separately printing by inspection"
         for item in reservation:
            print "item:", item
      except Exception, pe:
         notify.send_receipt({'status':'failure', 'type':'PROVISION_VM', 'courseUUID': self.course_uuid, 'id':self.command_id, 'message': str(pe)})


class UpdateCommand(Command):
   """ This command is issued when we want to merge a commit in from the Prototype branch """

   update_script = "./proto-merge.sh"
   
   def __init__(self, context):
      super( UpdateCommand, self).__init__(context)
      self.next_commit = context['commitRef']
      try:
         self.student = context['student']
      except Exception, err:
         print "problem getting student from context", err

   def do(self):
      proc_arr = [ self.update_script, self.course_uuid, self.next_commit ]
      try:
         if self.student is not None:
            proc_arr.append(self.student)
         print 'calling...'
         call(proc_arr)
      except Exception, fu:
         print "crud", str(fu)
