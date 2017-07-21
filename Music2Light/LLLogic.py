from LLCommunicator import LLTopic, LLCommunicator, LLSubscription
import Settings
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
        topic = LLTopic(path="devices/{}/{}/light".format(self.type, self.id), value="1")
        self.communicator.publish(topic)

    def disable(self):
        topic = LLTopic(path="devices/{}/{}/light".format(self.type, self.id), value="0")
        self.communicator.publish(topic)

    def enable_light(self, index, dim):
        topic_r = LLTopic(path="devices/{}/{}/index". format(self.type, self.id), value="{}".format(r))
        topic_dim = LLTopic(path="devices/{}/{}/dim".format(self.type, self.id), value="{}".format(dim))
        self.communicator.publish(topic_r)
        self.communicator.publish(topic_g)
        self.communicator.publish(topic_b)
        self.communicator.publish(topic_dim)

#
# DMX Devices werden angeschlossen
# DMX Addressen mussen in Lichtbereiche, Nebelbereiche aufgeteilt sein.
class LLDMXDevice(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLDMXLight, self).__init__(mac, type, id, communicator)

    def disable_light(self):
        # Licht
        for i in range(Settings.DMXKannenStart, Settings.DMXKannenEnd, Settings.DMXKannenStep):
            topic_r = LLTopic(path="devices/{}/{}/{}". format(self.type, self.id, i), value="{}".format(0))
            topic_g = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, i+1), value="{}".format(0))
            topic_b = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, i+2), value="{}".format(0))
            topic_dim = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, i + 3), value="{}".format(0))
            self.communicator.publish(topic_r)
            self.communicator.publish(topic_g)
            self.communicator.publish(topic_b)
            self.communicator.publish(topic_dim)

    def disable_fog(self):
        for channel in Settings.DMXNebelChannels:
            topic_off = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, channel[0]), value="{}".format(channel[1]))
            self.communicator.publish(topic_off)

    def enable_fog(self):
        for channel in Settings.DMXNebelChannels:
            topic_on = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, channel[0]), value="{}".format(channel[2]))
            self.communicator.publish(topic_on)

    def enable_light(self, index, dim):
        # Get Color from Colormap
        r = Settings.ColorMap[index][0]
        g = Settings.ColorMap[index][1]
        b = Settings.ColorMap[index][2]
        # iterate over all possible DMX lights on the Devices
        for i in range(Settings.DMXKannenStart, Settings.DMXKannenEnd, Settings.DMXKannenStep):
            topic_r = LLTopic(path="devices/{}/{}/{}". format(self.type, self.id, i), value="{}".format(r))
            topic_g = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, i+1), value="{}".format(g))
            topic_b = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, i+2), value="{}".format(b))
            topic_dim = LLTopic(path="devices/{}/{}/{}".format(self.type, self.id, i + 3), value="{}".format(dim))
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
        topic = LLTopic(path="devices/{}/{}/beep_n_times". format(self.type, self.id), value="1")
        self.communicator.publish(topic)
        self.audio = 1

    def disable_audio(self):
        topic = LLTopic(path="devices/{}/{}/beep_n_times". format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        self.audio = 0

    def enable_vibration(self):
        topic = LLTopic(path="devices/{}/{}/vibe".format(self.type, self.id), value="3")
        self.communicator.publish(topic)
        self.vibration = 1

    def disable_vibration(self):
        topic = LLTopic(path="devices/{}/{}/vibe".format(self.type, self.id), value="0")
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

    def disable(self):
        self.disable_audio()
        self.disable_light()
        self.disable_vibration()

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
        self.configMode = True
        self.registrationState = 0
        self.hello_mac = ""
        self.hello_type = ""
        self.devices = []
        self.communicator = communicator



    def registration(self, hello_mac, hello_type):
        if (self.configMode):
            """Searches for Mac in known devices, when found publishes id of the known device to hello/mac/id"""
            for device in self.devices:
                if (device.mac == hello_mac):
                    print("Registrated known device of type {} with mac {} on id {}".format(hello_type,
                                                                                            hello_mac,
                                                                                            self.id))
                    topic = LLTopic("hello/{}/id".format(hello_mac), str(device.id))
                    self.communicator.publish(topic)
                    return

            """When no Mac of known devices matches the received mac, a new device is created."""

            print(
            "Registrated new device of type {} with mac {} on id {}".format(hello_type, hello_mac,
                                                                            self.id))
            topic = LLTopic("hello/{}/id".format(hello_mac), str(self.id))
            self.communicator.publish(topic)

            '''
            Register Device Types
            '''
            if (hello_type == "StandardLight"):
                self.devices.append(
                    LLStandardLight(hello_mac, hello_type, self.id, self.communicator))

            if (hello_type == "StandardButtonBox"):
                self.devices.append(
                    LLStandardButtonBox(hello_mac, hello_type, self.id, self.communicator))

            if (hello_type == "StandardController"):
                self.devices.append(
                    LLStandardController(hello_mac, hello_type, self.id, self.communicator))

            self.id += 1

        else:

            """If Registration is not active, known devices are registered the same way as if registration was active."""
            for device in self.devices:
                if (device.mac == hello_mac):
                    print("Registrated known device of type {} with mac {} on id {}".format(hello_type,
                                                                                            hello_mac,
                                                                                            self.id))
                    topic = LLTopic("hello/{}/id".format(hello_mac), str(device.id))
                    self.communicator.publish(topic)
                    return

            """If Registration is inactive, devices can't be registered. -1 is send as id."""
            topic = LLTopic("hello/{}/id".format(hello_mac), str(-1))
            self.communicator.publish(topic)


    def find_device(self, type, id):
        for device in self.devices:
            if(device.type == type and device.id == int(id)):
                return device

        return -1



