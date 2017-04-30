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


class LLStandardLight(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStandardLight, self).__init__(mac, type, id, communicator)


class LLStandardButtonBox(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStandardButtonBox, self).__init__(mac, type, id, communicator)

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
            if(self.configMode):
                if(self.registrationState == 2):
                    for device in self.devices:
                        if(device.mac == self.hello_mac):
                            print("Registrated known device of type {} with mac {} on id {}".format(self.hello_type, self.hello_mac, self.id))
                            topic = LLTopic("hello/id", str(self.id))
                            self.communicator.publish(topic)
                            self.id += 1
                            self.registrationState = 0
                            device.id = self.id - 1
                    if(self.registrationState == 2):
                        print("Registrated new device of type {} with mac {} on id {}".format(self.hello_type, self.hello_mac, self.id))
                        topic = LLTopic("hello/id", str(self.id))
                        self.communicator.publish(topic)

                        '''
                        Register Device Types
                        '''
                        if(self.hello_type == "StandardLight"):
                            self.devices.append(LLStandardLight(self.hello_mac, self.hello_type, self.id, self.communicator))

                        if (self.hello_type == "StandardButtonBox"):
                            self.devices.append(LLStandardButtonBox(self.hello_mac, self.hello_type, self.id, self.communicator))

                        if (self.hello_type == "StandardController"):
                            self.devices.append(LLStandardController(self.hello_mac, self.hello_type, self.id, self.communicator))


                        self.id += 1
                        self.registrationState = 0


            else:
                if (self.registrationState == 2):

                    for device in self.devices:
                        if(device.mac == self.hello_mac):
                            print("Registrated known device of type {} with mac {} on id {}".format(self.hello_type, self.hello_mac, self.id))
                            topic = LLTopic("hello/id", str(self.id))
                            self.communicator.publish(topic)
                            self.id += 1
                            self.registrationState = 0
                            device.id = self.id -1
                    if(self.registrationState == 2):
                        topic = LLTopic("hello/id", str(-1))
                        self.communicator.publish(topic)
                        self.registrationState = 0

            sleep(0.1)



