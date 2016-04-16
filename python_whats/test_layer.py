from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
import json

class TestLayer(YowInterfaceLayer):
    def __init__(self, transport = None):
        super(TestLayer, self).__init__()
        if transport:
            self.transport = transport
        self.name = 'redis'
        self.detached = False
        self.thread = False

    def send_to_human(self,user, msg):
        _msg = TextMessageProtocolEntity(
            msg.encode("UTF-8"),
            to=self.normalizeJid(user))        
        self.toLower(_msg)        
        print _msg

    #https://github.com/tgalal/yowsup/issues/475
    def normalizeJid(self, number):
        if '@' in number:
            return number

        return "%s@s.whatsapp.net" % number
    def print_this(self,item)        :
        data = json.loads(item['data'])
        self.send_to_human(data['from_user'],data['message'])
        print item 
        print 'LLEGO!!!!'
        
    def onEvent(self, layerEvent):
        print layerEvent.getName()
        if layerEvent.getName() == 'start_redis':
            print 'redis started'
            import redis
            client = redis.Redis(host='redis',port=6379)
            pubsub = client.pubsub()
        #pubsub.subscribe('test_channel')    
            pubsub.subscribe(**{'message_ready': self.print_this})
            self.thread = pubsub.run_in_thread(sleep_time=0.001)
        if layerEvent.getName() == 'killredis':
            self.thread.stop()
        #for item in pubsub.listen():        
        #    print item
    
    def isDetached(self):
        return self.detached

    def getName(self):
        return self.name        