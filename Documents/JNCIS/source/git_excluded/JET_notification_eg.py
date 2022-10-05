"""
JET 1.0  
JET Notification Application
The following JET application illustrates the use of notification using the Notification API (see the Juniper Extension Toolkit API Guide).
"""

#!/usr/bin/env python

import argparse
import os
import time
import logging
import sys

# JET shim layer imports
from jnpr.jet.JetHandler import *

# Default Notification topic parameters
DEFAULT_NOTIFICATION_IFD_NAME = "ge-0/0/0"
DEFAULT_NOTIFICATION_IFL_NAME = "lt-0/0/0"
DEFAULT_NOTIFICATION_IFL_UNIT = "11"

# Logging Parameters
DEFAULT_LOG_FILE_NAME = os.path.basename(__file__).split('.')[0]+'.log'
DEFAULT_LOG_LEVEL = logging.DEBUG

# Enable Logging to a file
logging.basicConfig(filename=DEFAULT_LOG_FILE_NAME, level=DEFAULT_LOG_LEVEL)

# To display the messages from junos-jet-api package on the screen uncomment the below line
myLogHandler = logging.getLogger()
myLogHandler.setLevel(logging.INFO)
logChoice = logging.StreamHandler(sys.stdout)
logChoice.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logChoice.setFormatter(formatter)
myLogHandler.addHandler(logChoice)


def handleEvents1(message):
    print "I am in first handle"
    print "Event Received : " + message['jet-event']['event-id']
    print "Attributes : ", message['jet-event']['attributes']
    return

def handleEvents2(message):
    print "I am in second handle"
    print "Event Received : " + message['jet-event']['event-id']
    print "Attributes : ", message['jet-event']['attributes']
    return



def Main():
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__), description='Sample JET application')
    parser.add_argument("--address", nargs='?', help="Address of the JSD server. (default: %(default)s)",
                        type=str, default='localhost')
    parser.add_argument("--port", nargs='?', help="Port number of the JSD notification server. default: %(default)s",
                        type=int, default=1883)
    parser.add_argument("--bind_address", nargs='?', help="Client source address to bind.",
                        type=str, default="")
    args = parser.parse_args()

    try:


        # Create a client handler for connecting to server
        client = JetHandler()

        # open session with MQTT server
        evHandle = client.OpenNotificationSession(device=args.address, port=args.port, bind_address=args.bind_address)
        # different ways of creating topic
        ifdtopic = evHandle.CreateIFDTopic(op=evHandle.ALL, ifd_name=DEFAULT_NOTIFICATION_IFD_NAME)
        ifltopic = evHandle.CreateIFLTopic(evHandle.ALL,
                                           DEFAULT_NOTIFICATION_IFL_NAME,
                                           DEFAULT_NOTIFICATION_IFL_UNIT)
        ifatopic = evHandle.CreateIFATopic(evHandle.DELETE)
        ifftopic = evHandle.CreateIFFTopic(evHandle.CHANGE)
        rtmtopic = evHandle.CreateRouteTableTopic(evHandle.ALL)
        rttopic = evHandle.CreateRouteTopic(evHandle.ALL)
      

        # Subscribe for events
        print "Subscribing to IFD notifications"
        evHandle.Subscribe(ifdtopic, handleEvents1)
        evHandle.Subscribe(ifltopic, handleEvents2)
        evHandle.Subscribe(ifatopic, handleEvents1)
        evHandle.Subscribe(rtmtopic, handleEvents2)
        evHandle.Subscribe(rttopic, handleEvents2)
      
        time.sleep(120)
        # Unsubscribe events
        print "Unsubscribe from all the event notifications"
        evHandle.Unsubscribe()

        # Close session
        print "Closing the Client"
        client.CloseNotificationSession()

    except Exception, tx:
        print '%s' % (tx.message)


    return

if __name__ == '__main__':
    Main()
