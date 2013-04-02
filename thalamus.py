#!/usr/bin/python

import time
import signal
import multiprocessing
import stomp
from listeners import JSONListener
from models import InitCommand, UpdateCommand, ProvisionCommand
import logging



# Handle SIGTERM stops
stop_event = multiprocessing.Event()

def stop(signum, frame):
   stop_event.set()

signal.signal(signal.SIGTERM, stop)

#=============================================
logger = logging.getLogger('thalamus')
hdlr = logging.FileHandler('/var/log/mpi/thalamus.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

#logger.error('We have a problem')
logger.info('signal setup complete')
#=============================================

#conn.disconnect() # This may no longer be necessary. Stop handler?

def main():
   command_map = {"INITIALIZE": InitCommand, "UPDATE_CLASS": UpdateCommand, "UPDATE_STUDENT": UpdateCommand, "PROVISION_VM": ProvisionCommand} 
   conn = stomp.Connection([('localhost',61613)])
   conn.set_listener('', JSONListener(command_map, default_handler))
   conn.start()
   conn.connect()
   conn.subscribe(destination='/queue/test', ack='auto')
   while not stop_event.is_set():
      logger.info("sleeping")
      time.sleep(3)

# if command do was __call__, this could be a function
class default_handler(object):
   def __init__(self, context):
      super(default_handler, self).__init__()
   def do(self):
      print "Command mapping not found!"

if __name__ == '__main__':
   main()
