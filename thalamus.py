#!/usr/bin/python

import time
import stomp
from listeners import JSONListener
from models import InitCommand, UpdateCommand

# if command do was __call__, this could be a function
class default_handler(object):

   def __init__(self, context):
      super(default_handler, self).__init__()
   
   def do(self):
      print "WHOA NELLY"

conn = stomp.Connection([('localhost',61613)])
command_map = {"INITIALIZE": InitCommand, "UPDATE_CLASS": UpdateCommand, "UPDATE_STUDENT": UpdateCommand} 
conn.set_listener('', JSONListener(command_map, default_handler))
conn.start()
conn.connect()

conn.subscribe(destination='/queue/test', ack='auto')

time.sleep(2000)

# work on daemon...
#while True:
#   pass

conn.disconnect()
