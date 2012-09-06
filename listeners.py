import json

# Set up a shared class for command flow, somewhere
class JSONListener(object):

   def __init__(self, command_list, default):
      super(JSONListener, self).__init__()
      self.commands = command_list # how are references handled?!! TODO figure out immediately if copy needed
      self.default = default # will likely be an error broadcast

   def on_error(self, headers, message):
      print 'received an error %s' % message

   def on_message(self, headers, message):
      print 'received a message %s' % message
      j_message = json.loads(message)
      print 'moving to if statement'
      if 'command' in j_message:
         print  'command existed'
         action = j_message['command']
         print "command was", action
         try:
            context = j_message['context']
         except Exception, err:
            print 'gotcha', str(err)
         command = self.commands.get(action, self.default)(context)
         command.do() # hope
      else:
         print "Unrecognized broadcast"
