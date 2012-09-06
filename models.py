from subprocess import call
import myutil
#import LookupError

class Tutorial(object):
   pass
   
class Command(object):
   
   def __init__(self, context):
      super(Command, self).__init__()
      self.course_name = context['courseName']
      self.prototype = context['prototype']

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

   # TODO determine if self should be used given overwrite possibility.  Mad security leak
   def do(self):
      print "INSIDE"
      try:
         call([ self.setup_script, self.course_name, self.prototype['repository'], self._get_students_as_string() ])
      except Exception, fu:
         print "Crap", str(fu)

   def _get_students_as_string(self):
      return " ".join([str(s['studentId']) for s in self.students])

class UpdateCommand(Command):
   """ This command is issued when we want to merge a commit in from the Prototype branch """

   update_script = "./proto-merge.sh"
   
   def __init__(self, context):
      super( UpdateCommand, self).__init__(context)
      self.next_commit = context['commitRef']
      print 'next was: ', self.next_commit

   # TODO determine if self should be used given overwrite possibility.  Mad security leak
   def do(self):
      print 'calling...'
      try:
         call([ self.update_script,  self.course_name, self.next_commit ])
      except Exception, fu:
         print "crud", str(ru)
