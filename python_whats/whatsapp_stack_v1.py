from yowsup.stacks import  YowStackBuilder

from whatsapp_layer_v1 import WhatsAppLayer
from test_layer import TestLayer

from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.axolotl.layer import YowAxolotlLayer
import sys
import logging

class YowsupCliStack(object):
    def __init__(self, credentials, encryptionEnabled = True):
        stackBuilder = YowStackBuilder()
        self.thread = ''
        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(WhatsAppLayer)\
            .push(TestLayer)\
            .build()

        # self.stack.setCredentials(credentials)
        self.stack.setCredentials(credentials)
        self.stack.setProp(YowAxolotlLayer.PROP_IDENTITY_AUTOTRUST, True)
    def start(self):
        logging.info("Yowsup Cli client\n==================\nType /help for available commands\n", exc_info=True)
        
        self.stack.broadcastEvent(YowLayerEvent(WhatsAppLayer.EVENT_START))
        self.stack.broadcastEvent(YowLayerEvent('start_pika'))
        try:
            self.stack.loop(timeout = 0.5, discrete = 0.5)
        except AuthError as e:
            logging.info("Auth Error, reason {}".format(e))
        except KeyboardInterrupt:
            self.stack.broadcastEvent(TestLayer('kill_pika'))
            self.stack.broadcastEvent(YowLayerEvent('kill_pika'))            
            print("\nYowsdown")
            sys.exit(0)

CREDENTIALS = ("5493517653646", "RfrfIgmgwcP2QPn+tvkZwTpBScE=") # replace with your phone and password

if __name__==  "__main__":
    stack = YowsupCliStack(credentials=CREDENTIALS, encryptionEnabled=True)
    stack.start() #this is the program mainloop