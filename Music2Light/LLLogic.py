from LLCommunicator import LLTopic, LLCommunicator, LLSubscription
from threading import Thread
from time import sleep
class LLDevice(object):
    type = ""
    mac = ""
    id = ""
    def __init__(self, mac, type, id, communicator):
        self.mac = mac
        self.type = type
        self.id = id
        self.communicator = communicator

    def set_status(self, status):
        self.status = status


'''
@class LLStandardLight
@brief Object for Standard Light

topics:
- status
- light (0/1)
- r
- g
- b
- dim
'''
class LLStandardLight(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStandardLight, self).__init__(mac, type, id, communicator)
        self.disable()
        self.set_color()

    def enable(self):
        topic = LLTopic(path="devices/{}/{}/light". format(self.type, self.id), topic="1")
        self.communicator.publish(topic)

    def disable(self):
        topic = LLTopic(path="devices/{}/{}/light". format(self.type, self.id), topic="0")
        self.communicator.publish(topic)

    def set_color(self, r=255, g=255, b=255, dim=255):
        topic_r = LLTopic(path="devices/{}/{}/r". format(self.type, self.id), topic="{}".format(r))
        topic_g = LLTopic(path="devices/{}/{}/g".format(self.type, self.id), topic="{}".format(g))
        topic_b = LLTopic(path="devices/{}/{}/b".format(self.type, self.id), topic="{}".format(b))
        topic_dim = LLTopic(path="devices/{}/{}/dim".format(self.type, self.id), topic="{}".format(dim))
        self.communicator.publish(topic_r)
        self.communicator.publish(topic_g)
        self.communicator.publish(topic_b)
        self.communicator.publish(topic_dim)

'''
@class LLStandardButtonBox
@brief Object for ButtonBox

topics:
- status
- button (0/1)
- audio (0/1)
- vibration (0/1)
- light (0/1)
'''
class LLStandardButtonBox(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStandardButtonBox, self).__init__(mac, type, id, communicator)
        self.disable_light()
        self.disable_audio()
        self.disable_vibration()

    def enable_audio(self):
        topic = LLTopic(path="devices/{}/{}/audio". format(self.type, self.id), value="1")
        self.communicator.publish(topic)
        self.audio = 1

    def disable_audio(self):
        topic = LLTopic(path="devices/{}/{}/audio". format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        self.audio = 0

    def enable_vibration(self):
        topic = LLTopic(path="devices/{}/{}/vibration".format(self.type, self.id), value="1")
        self.communicator.publish(topic)
        self.vibration = 1

    def disable_vibration(self):
        topic = LLTopic(path="devices/{}/{}/vibration".format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        self.vibration = 0

    def enable_light(self):
        topic = LLTopic(path="devices/{}/{}/light".format(self.type, self.id), value="1")
        self.communicator.publish(topic)
        self.light = 1

    def disable_light(self):
        topic = LLTopic(path="devices/{}/{}/light".format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        self.light = 0

    def set_button(self):
        self.pushed = 1

    def unset_button(self):
        self.pushed = 0



class LLStandardController(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStandardController, self).__init__(mac, type, id, communicator)

class LLLogic(object):
    def __init__(self, communicator):
        print("Initialise Logic")
        self.id = 0
        self.configMode = False
        self.registrationState = 0
        self.hello_mac = ""
        self.hello_type = ""
        self.devices = []
        self.communicator = communicator

    def start_registration(self):
        self.loop_registration = Thread(target=self.registration_loop)
        self.loop_registration.start()

    def registration_loop(self):
        while(True):
            self.registration()
            self.game()
            sleep(0.1)

    def game(self):
        print("Gaming")


    def registration(self):
        if (self.configMode):
            if (self.registrationState == 2):
                for device in self.devices:
                    if (device.mac == self.hello_mac):
                        print("Registrated known device of type {} with mac {} on id {}".format(self.hello_type,
                                                                                                self.hello_mac,
                                                                                                self.id))
                        topic = LLTopic("hello/{}/id".format(self.hello_mac), str(self.id))
                        self.communicator.publish(topic)
                        self.id += 1
                        self.registrationState = 0
                        device.id = self.id - 1
                if (self.registrationState == 2):
                    print(
                    "Registrated new device of type {} with mac {} on id {}".format(self.hello_type, self.hello_mac,
                                                                                    self.id))
                    topic = LLTopic("hello/{}/id".format(self.hello_mac), str(self.id))
                    self.communicator.publish(topic)

                    '''
                    Register Device Types
                    '''
                    if (self.hello_type == "StandardLight"):
                        self.devices.append(
                            LLStandardLight(self.hello_mac, self.hello_type, self.id, self.communicator))

                    if (self.hello_type == "StandardButtonBox"):
                        self.devices.append(
                            LLStandardButtonBox(self.hello_mac, self.hello_type, self.id, self.communicator))

                    if (self.hello_type == "StandardController"):
                        self.devices.append(
                            LLStandardController(self.hello_mac, self.hello_type, self.id, self.communicator))

                    self.id += 1
                    self.registrationState = 0


        else:
            if (self.registrationState == 2):

                for device in self.devices:
                    if (device.mac == self.hello_mac):
                        print("Registrated known device of type {} with mac {} on id {}".format(self.hello_type,
                                                                                                self.hello_mac,
                                                                                                self.id))
                        topic = LLTopic("hello/id", str(self.id))
                        self.communicator.publish(topic)
                        self.id += 1
                        self.registrationState = 0
                        device.id = self.id - 1
                if (self.registrationState == 2):
                    topic = LLTopic("hello/id", str(-1))
                    self.communicator.publish(topic)
                    self.registrationState = 0


    def find_device(self, type, id):
        for device in self.devices:
            if(device.type == type and device.id == int(id)):
                return device

        return -1



