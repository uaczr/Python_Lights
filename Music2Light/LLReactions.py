


class LLReactionStop(LLReaction):
    def __init__(self, name, eventmatrix, communicator):
        super(LLReactionStop, self).__init__(name, eventmatrix)
        self.communicator = communicator

    def react(self, signal):
        print("Reacting to Stop")
        self.eventmatrix.triggerEvent("Stop")

class LLReactionStart(LLReaction):
    def __init__(self, name, eventmatrix, communicator):
        super(LLReactionStart, self).__init__(name, eventmatrix)
        self.communicator = communicator

    def react(self, signal):
        print("Reacting to Start")
        self.eventmatrix.triggerEvent("Start")

class LLReactionConfigMode(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionConfigMode, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print("Reacting to Config Mode")
        if(signal.value == "1"):
            logic.configMode = True

        if (signal.value == "0"):
            logic.configMode = False


class LLReactionHelloType(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionHelloType, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print("Reacting to HelloType")
        self.logic.registrationState += 1
        self.logic.hello_type = signal.value


class LLReactionHelloMac(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionHelloMac, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print("Reacting to HelloMac")
        self.logic.registrationState += 1
        self.logic.hello_mac = signal.value

class LLReactionDeviceStatus(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionDeviceStatus, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print("Reacting to DeviceStatus")
        device, id = self.findTypeAndId(signal.path)
        print('Device of type {} with id {} changed to status {}'.format(device, id, signal.value))

    def findTypeAndId(self, path):
        type_begin = path.find("/")+1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]

class LLReactionButtonBox(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionDeviceStatus, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
