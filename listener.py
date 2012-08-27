#!/usr/bin/python

import time
import sys
from subprocess import call
import json
import stomp

class JSONListener(object):
   def on_error(self, headers, message):
      print 'received an error %s' % message

   def on_message(self, headers, message):
      print 'received a message %s' % message
      j_message = json.loads(message)
      if 'command' in j_message:
         action = j_message['command']
         request = j_message['context']
         course_name = str(request['courseName'])
         repo_url = str(request['prototype']['repository'])
         all_students = " ".join([str(s['studentId']) for s in request['students']])
         call(["./setup-class-branches.sh", course_name, repo_url, all_students])
      else:
         print "Unrecognized broadcast"

conn = stomp.Connection([('localhost',61613)])
conn.set_listener('', JSONListener())
print 'set up connection'
conn.start()
conn.connect()

conn.subscribe(destination='/queue/test', ack='auto')

#conn.send(' '.join(sys.argv[1:]), destination='/queue/test')

time.sleep(20)
conn.disconnect()
