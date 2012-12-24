#!/usr/bin/python

# Called by post-receive hook.

import time
import sys
import json
import stomp


if not len(sys.argv[1:]) == 4:
   print 'usage: notify.py <course_name> <student_id> <status_tag> <commit>'
   sys.exit(1)

command = json.dumps({'command': 'ADVANCE_STUDENT', 'context': {'courseName': sys.argv[1], 'studentId': sys.argv[2], 'checkpoint': sys.argv[3], 'commit': sys.argv[4]}})

class NotifyListener(object):
   def on_error(self, headers, message):
      print 'received an error %s' % message

   def on_message(self, headers, message):
      print 'received a message %s' % message

conn = stomp.Connection([('localhost',61613)])
conn.set_listener('', NotifyListener())
print 'set up connection'
conn.start()
conn.connect()

# Currently not listening - if we do, probably on a feedback queue
#conn.subscribe(destination='/queue/test', ack='auto')

conn.send(command, destination='/queue/incoming')

# NOTE
# We're currently sending the message to a queue.  We may wish to have a richer ecosystem
# wherein messages are broadcast to a topic, logged, etc.  Additionally, the listener for
# professor bot may want to be alerted in that manner.  This would provide failover behavior
# so that if the main site is down, assignments can still be turned in or manually dealt with.

time.sleep(2)
conn.disconnect()
