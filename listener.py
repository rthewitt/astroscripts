#!/usr/bin/python

import time
import sys
from subprocess import call
import json
import stomp


# Set up a shared class for command flow, somewhere
class JSONListener(object):
   def on_error(self, headers, message):
      print 'received an error %s' % message

   def on_message(self, headers, message):
      print 'received a message %s' % message
      j_message = json.loads(message)
      if 'command' in j_message:
         action = j_message['command']
         if action == "INITIALIZE":
            request = j_message['context']
            course_name = str(request['courseName'])
            repo_url = str(request['prototype']['repository'])
            all_students = " ".join([str(s['studentId']) for s in request['students']])
            call(["./setup-class-branches.sh", course_name, repo_url, all_students])
         elif action == "MERGE_REQUEST":
            request = j_message['context']
            course_name = str(request['courseName'])
            repo_url = str(request['prototype']['repository'])
            commit_ref = str(request['prototype']['commitRef'])
            git_method = str(request['prototype']['method'])
            # Wow, this is dirty as hell.  Do some serious checking here, yeah?
            if git_method == "merge":
               call(["./proto-merge.sh", course_name, commit_ref])
            else:
               pass #coming soon, I promise
         else:
            print "Unsupported command"
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
