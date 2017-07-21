import paho.mqtt.client as mqtt
from threading import Thread



'''
Entry for the signal2reaction list
'''
class LLSignalToReactionEntry:
    def __init__(self, signal, reaction):
        self.signal = signal
        self.reaction = reaction


'''
Creates Link between signal and reaction
'''
class LLSignalToReactionEngine(object):
    signalreactionlist = []

    def __init__(self):
        print("Init Signal2Reaction")

    def setSignal2ReactionList(self, signalreactionlist):
        self.signalreactionlist = signalreactionlist

    def signal2reaction(self, signal):
        for signalToReaction in self.signalreactionlist:
            if(signalToReaction.signal == signal.name):
                for reaction in signalToReaction.reaction:
                    reaction.react(signal)
                break

'''
Base Class for all signals
'''
class LLSignal(object):
    def __init__(self, name, signal2Reaction):
        self.name = name
        self.signal2Reaction = signal2Reaction

    def signal(self):
        self.signal2Reaction.signal2reaction(self)


'''
Base class for all reactions
'''
class LLReaction(object):
    def __init__(self, name, eventmatrix):
        self.name = name
        self.eventmatrix = eventmatrix

    def react(self, signal):
        self.signal = signal
        return 0

    def findTypeAndId(self, path):
        type_begin = path.find("/") + 1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]

'''
MQTT Topic
'''
class LLTopic:
    def __init__(self, path, value):
        self.path = path
        self.value = value

    def setValue(self, value):
        self.value = value

'''
MQTT Subscription Signal
'''


class LLSubscription(LLSignal):
    def __init__(self, name, path, signal2Reaction):
        super(LLSubscription, self).__init__(name, signal2Reaction)
        self.topic = LLTopic(path, 0)

    def signal(self, value=0, path=""):
        self.value = value
        self.path = path
        self.signal2Reaction.signal2reaction(self)



class LLCommunicator(object):
    subscriptions = []
    loop = 0
    def __init__(self, brocker_address, port):
        self.broker_address = brocker_address
        self.port = port
        self.MqttClient = mqtt.Client()
        self.MqttClient.on_connect = self.on_connect
        self.MqttClient.on_message = self.on_message


    def connect(self):
        print('Connecting to Brocker {} at port {}'.format(self.broker_address, self.port))
        self.MqttClient.connect(host=self.broker_address, port=self.port, keepalive=60)
        self.loop = Thread(target=self.MqttClient.loop_forever)
        self.loop.start()

    def  addSubscription(self, subscription):
        print('Subscribed to Topic {}'.format(subscription.topic.path))
        self.subscriptions.append(subscription)
        self.MqttClient.subscribe(subscription.topic.path)

    def on_connect(self, client, userdata, flags, rc):
        print('Connected to Brocker {} at port {}'.format(self.broker_address, self.port))


    def on_message(self, client, user_data, msg):
        print('Received Message on Topic {} with Value {}'.format(msg.topic, msg.payload))
        for subscription in self.subscriptions:
            if(mqtt.topic_matches_sub(subscription.topic.path, msg.topic)):
                subscription.signal(value=msg.payload, path=msg.topic)

    def publish(self, topic):
        print('Published Message on Topic {} with Value {}'.format(topic.path, topic.value))
        self.MqttClient.publish(topic=topic.path, payload=topic.value)