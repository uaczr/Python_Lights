from LLCommunicator import LLTopic, LLCommunicator, LLSubscription
import Settings
from threading import Timer
import  time
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

    def disable(self):
        print "Unimplemented Disablefunction"


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

Pattern
strobe
nextColor
Strobe
kill
'''
class LLStandardLight(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStandardLight, self).__init__(mac, type, id, communicator)
        self.disable()
        self.flash_light()
        self.Timer = None
        self.State = "Off"
        self.oldState = "Off"

    def disable(self):
        topic = LLTopic(path="devices/{}/{}/enable_strobe".format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        topic = LLTopic(path="devices/{}/{}/enable_light".format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        self.State = "Off"

    def enable_light(self):
        topic_r = LLTopic(path="devices/{}/{}/enable_light". format(self.type, self.id), value="{}".format(1))
        self.communicator.publish(topic_r)
        self.State = "Light"

    def flash_light(self):
        self.enable_strobe()
        self.Timer = Timer(1.0, self.unflash_light)
        self.Timer.start()
        self.oldState = self.State
        self.State = "Flash"

    def unflash_light(self):
        self.disable_strobe()
        if self.oldState == "Light":
            self.enable_light()

    def enable_strobe(self):
        topic_r = LLTopic(path="devices/{}/{}/enable_light". format(self.type, self.id), value="{}".format(1))
        self.communicator.publish(topic_r)

        topic = LLTopic(path="devices/{}/{}/enable_strobe". format(self.type, self.id), value="{}".format(1))
        self.communicator.publish(topic)
        self.State = "Strobe"

    def disable_light(self):
        topic_r = LLTopic(path="devices/{}/{}/enable_light". format(self.type, self.id), value="{}".format(0))
        self.communicator.publish(topic_r)
        self.State = "Off"

    def disable_strobe(self):
        topic = LLTopic(path="devices/{}/{}/enable_strobe". format(self.type, self.id), value="{}".format(0))
        self.communicator.publish(topic)
        topic_r = LLTopic(path="devices/{}/{}/enable_light". format(self.type, self.id), value="{}".format(0))
        self.communicator.publish(topic_r)
        self.State = "Off"

    def change_color(self, n):
        topic = LLTopic(path="devices/{}/{}/color". format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

    def change_pattern(self, n):
        topic = LLTopic(path="devices/{}/{}/pattern". format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

    def change_strobe(self, n):
        topic = LLTopic(path="devices/{}/{}/strobe". format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

    def dim(self, n):
        topic = LLTopic(path="devices/{}/{}/dim". format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

'''
@class LLStandardLight
@brief Object for Standard Light

enable_light
enable_strobo
pattern
strobe
color
dim
'''

class LLStrobo(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLStrobo, self).__init__(mac, type, id, communicator)
        self.disable()
        self.flash_light()
        self.Timer = None
        self.State = "Off"
        self.oldState = "Off"

    def disable(self):
        topic = LLTopic(path="devices/{}/{}/enable_strobe".format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        topic = LLTopic(path="devices/{}/{}/enable_light".format(self.type, self.id), value="0")
        self.communicator.publish(topic)
        self.State = "Off"

    def enable_light(self):
        topic_r = LLTopic(path="devices/{}/{}/enable_light".format(self.type, self.id), value="{}".format(1))
        self.communicator.publish(topic_r)
        self.State = "Light"

    def flash_light(self):
        self.enable_strobe()
        self.Timer = Timer(1.0, self.unflash_light)
        self.Timer.start()
        self.oldState = self.State
        self.State = "Flash"

    def unflash_light(self):
        self.disable_strobe()
        if self.oldState == "Light":
            self.enable_light()

    def enable_strobe(self):
        topic_r = LLTopic(path="devices/{}/{}/enable_light".format(self.type, self.id), value="{}".format(1))
        self.communicator.publish(topic_r)

        topic = LLTopic(path="devices/{}/{}/enable_strobe".format(self.type, self.id), value="{}".format(1))
        self.communicator.publish(topic)
        self.State = "Strobe"

    def disable_light(self):
        topic_r = LLTopic(path="devices/{}/{}/enable_light".format(self.type, self.id), value="{}".format(0))
        self.communicator.publish(topic_r)
        self.State = "Off"

    def disable_strobe(self):
        topic = LLTopic(path="devices/{}/{}/enable_strobe".format(self.type, self.id), value="{}".format(0))
        self.communicator.publish(topic)
        topic_r = LLTopic(path="devices/{}/{}/enable_light".format(self.type, self.id), value="{}".format(0))
        self.communicator.publish(topic_r)
        self.State = "Off"

    def change_color(self, n):
        topic = LLTopic(path="devices/{}/{}/color".format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

    def change_pattern(self, n):
        topic = LLTopic(path="devices/{}/{}/pattern".format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

    def change_strobe(self, n):
        topic = LLTopic(path="devices/{}/{}/strobe".format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

    def dim(self, n):
        topic = LLTopic(path="devices/{}/{}/dim".format(self.type, self.id), value="{}".format(n))
        self.communicator.publish(topic)

#
# DMX Devices werden angeschlossen
# DMX Addressen mussen in Lichtbereiche, Nebelbereiche aufgeteilt sein.
# DMX_kill
# DMX_update    "channel,value"
# DMX_init      Anzahl Channels

class LLDMXDevice(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLDMXDevice, self).__init__(mac, type, id, communicator)
        self.color = self.convert_hex2rgb("0000FF")
        self.dim = 1.0
        self.colors = [
            "FFFFFF",
            "0000FF",
            "800080",
            "BC8F8F",
            "9932CC",
            "FF6347",
            "FF0000",
            "A0522D",
            "FF00FF",
            "FFFFFF"
        ]
        self.disable_light()

    def convert_hex2rgb(self, hex):
        rgb = []
        for i in (0, 2, 4):
            rgb.append(int(hex[i:i+2], 16))
        return rgb

    def disable(self):
        self.disable_fog()
        self.disable_light()

    def disable_light(self):
        # Licht
        value = ""
        for i in range(Settings.DMXKannenStart, Settings.DMXKannenEnd, Settings.DMXKannenStep):
            r = "{},{},".format(i, 0)
            g = "{},{},".format(i+1, 0)
            b = "{},{},".format(i+2, 0)
            value += r
            value += g
            value += b

        value = value[0:len(value)-1]
        topic = LLTopic(path="devices/{}/{}/DMX_update".format(self.type, self.id), value=value)
        self.communicator.publish(topic)

    def disable_fog(self):
        value = ""
        for channel in Settings.DMXNebelChannels:
            value += "{},{},".format(channel[0], channel[1])

        value = value[0:len(value) - 2]
        topic_off = LLTopic(path="devices/{}/{}/DMX_update".format(self.type, self.id), value=value)
        self.communicator.publish(topic_off)

    def enable_fog(self):
        value = ""
        for channel in Settings.DMXNebelChannels:
            value += "{},{},".format(channel[0], channel[2])

        value = value[0:len(value) - 1]
        topic_off = LLTopic(path="devices/{}/{}/DMX_update".format(self.type, self.id), value=value)
        self.communicator.publish(topic_off)

    def enable_light(self):
        # Licht
        value = ""
        for i in range(Settings.DMXKannenStart, Settings.DMXKannenEnd, Settings.DMXKannenStep):
            r = "{},{},".format(i, int(self.dim*self.color[0]))
            g = "{},{},".format(i + 1, int(self.dim*self.color[1]))
            b = "{},{},".format(i + 2, int(self.dim*self.color[2]))
            value += r
            value += g
            value += b

        value = value[0:len(value) - 1]
        topic = LLTopic(path="devices/{}/{}/DMX_update".format(self.type,self.id), value=value)
        self.communicator.publish(topic)

    def enable_strobe(self):
        print "DMX has no strobe."

    def disable_strobe(self):
        print "DMX has no strobe"

    def change_pattern(self,n):
        print "DMX has no pattern"

    def change_strobe(self,n):
        print "DMX has no strobe"

    def change_color(self, n):
        self.color = self.convert_hex2rgb(self.colors[int(n/9)])
        value = ""
        for i in range(Settings.DMXKannenStart, Settings.DMXKannenEnd, Settings.DMXKannenStep):
            r = "{},{},".format(i, int(self.dim*self.color[0]))
            g = "{},{},".format(i + 1, int(self.dim*self.color[1]))
            b = "{},{},".format(i + 2, int(self.dim*self.color[2]))
            value += r
            value += g
            value += b

        value = value[0:len(value) - 1]
        topic = LLTopic(path="devices/{}/{}/DMX_update".format(self.type,self.id), value=value)
        self.communicator.publish(topic)

    def dim(self, n):
        self.dim = n






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
        topic = LLTopic(path="devices/{}/{}/vibe".format(self.type, self.id), value="1")
        self.communicator.publish(topic)
        self.vibration = 1

    def flash_vibe(self, n):
        topic = LLTopic(path="devices/{}/{}/vibe_n_times".format(self.type, self.id), value=str(n))
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

    def flash_light(self, n):
        topic = LLTopic(path="devices/{}/{}/flash_n_times".format(self.type, self.id), value=str(n))
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

"""
Topics Seilwinde
/drop in ms
/lift in ms
"""
class LLSeilwinde(LLDevice):
    def __init__(self, mac, type, id, communicator):
        super(LLSeilwinde, self).__init__(mac, type, id, communicator)
        self.State = "UP"
        self.lifttime = Settings.Seilwinde_Lifttime
        self.droptime = Settings.Seilwinde_Droptime
        self.last_call = time.time()

    def disable(self):
        if self.State == "DOWN":
            diff = (time.time() - self.last_call) * 1000
            if diff < self.droptime:
                rest = int(self.lifttime - (self.droptime - diff))
                topic = LLTopic(path="devices/{}/{}/lift".format(self.type, self.id), value=str(rest))
                self.communicator.publish(topic)
            else:
                topic = LLTopic(path="devices/{}/{}/lift".format(self.type, self.id), value=str(self.lifttime))
                self.communicator.publish(topic)
            self.last_call = time.time()
            self.State = "UP"

    def enable(self):
        if self.State == "UP":
            if diff < self.lifttime:
                rest = int(self.droptime - (self.lifttime - diff))
                topic = LLTopic(path="devices/{}/{}/lift".format(self.type, self.id), value=str(rest))
                self.communicator.publish(topic)
            else:
                topic = LLTopic(path="devices/{}/{}/lift".format(self.type, self.id), value=str(self.droptime))
                self.communicator.publish(topic)
            self.last_call = time.time()
            self.State = "DOWN"



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
        self.buttons = []
        self.lights = []
        self.dmx = []
        self.barlights = []
        self.strobolights = []
        self.seilwinde = []
        self.colorindex = 0
        self.patternindex = 0
        self.strobeindex = 0
        self.seilwinden = []



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
            if(hello_type == "DMXBox"):
                device = LLDMXDevice(hello_mac, hello_type, self.id, self.communicator)
                self.devices.append(device)
                self.lights.append(device)
                self.dmx.append(device)

            if (hello_type == "StandardLight"):
                device = LLStandardLight(hello_mac, hello_type, self.id, self.communicator)
                self.devices.append(device)
                self.lights.append(device)
                self.barlights.append(device)

            if (hello_type == "StandardButtonBox"):
                device = LLStandardButtonBox(hello_mac, hello_type, self.id, self.communicator)
                self.devices.append(device)
                self.buttons.append(device)

            if (hello_type == "Seilwinde"):
                device = LLSeilwinde(hello_mac, hello_type, self.id, self.communicator)
                self.devices.append(device)
                self.seilwinden.append(device)

            if (hello_type == "Strobo"):
                device = LLStrobo(hello_mac, hello_type, self.id, self.communicator)
                self.devices.append(device)
                self.lights.append(device)
                self.strobolights.append(device)

            if (hello_type == "StandardController"):
                device = LLStandardController(hello_mac, hello_type, self.id, self.communicator)
                self.devices.append(device)

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

    def disable_all(self):
        print("Disable all devices!")
        for device in self.devices:
            device.disable()

    def change_color(self):
        self.colorindex += 1
        self.patternindex += 1
        # self.colorindex += 1
        if self.colorindex > Settings.ColorIndexMax:
            self.colorindex = 0

        if self.patternindex > Settings.PatternIndexMax:
            self.patternindex = 0

        for light in self.lights:
            light.change_color(self.colorindex)
            light.change_pattern(self.patternindex)
            light.change_strobe(self.strobeindex)

    def change_red(self):
        self.colorindex = 60
        for light in self.lights:
            light.change_color(self.colorindex)
            light.change_pattern(self.patternindex)
            light.change_strobe(self.strobeindex)

    def change_blue(self):
        self.colorindex = 10
        for light in self.lights:
            light.change_color(self.colorindex)
            light.change_pattern(self.patternindex)
            light.change_strobe(self.strobeindex)

    def level0_lights(self):
        for light in self.lights:
            light.disable_light()

        for seilwinde in self.seilwinden:
            seilwinde.disable()

    def level1_lights(self):
        for light in self.lights:
            light.disable_light()

        for seilwinde in self.seilwinden:
            seilwinde.disable()

        for light in self.dmx:
            light.enable_light()

    def level2_lights(self):
        for light in self.lights:
            light.disable_light()

        for seilwinde in self.seilwinden:
            seilwinde.disable()

        for light in self.dmx:
            light.enable_light()

        for light in self.barlights:
            light.enable_light()

    def level3_lights(self):
        for light in self.lights:
            light.disable_light()

        for seilwinde in self.seilwinden:
            seilwinde.disable()

        for light in self.lights:
            light.enable_light()

    def level4_lights(self):
        for light in self.lights:
            light.disable_light()

        for seilwinde in self.seilwinden:
            seilwinde.disable()

        for light in self.lights:
            light.enable_light()

        for light in self.barlights:
            light.enable_strobe()

    def level5_ligths(self):
        for light in self.lights:
            light.disable_light()

        for light in self.lights:
            light.enable_strobe()

        for seilwinde in self.seilwinden:
            seilwinde.enable()

    def dim_all(self, n):
        for light in self.lights:
            light.dim(n)




