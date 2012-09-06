#!/usr/bin/python

import time
import sys
import json
import stomp


if not len(sys.argv[1:]) == 2:
   print 'usage: notify.py <student_id> <commit>'
   sys.exit(1)

command = json.dumps({'command': 'ADVANCE', 'context': {'studentId': sys.argv[1], 'commit': sys.argv[2]}})

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

# Here, we may want to send the current commit hash, so that we can
# revert/reset later if there's a problem
conn.send(' '.join(sys.argv[1:]), destination='/queue/incoming')

# NOTE
# We're currently sending the message to a queue.  We may wish to have a richer ecosystem
# wherein messages are broadcast to a topic, logged, etc.  Additionally, the listener for
# professor bot may want to be alerted in that manner.  This would provide failover behavior
# so that if the main site is down, assignments can still be turned in or manually dealt with.

time.sleep(2)
conn.disconnect()
