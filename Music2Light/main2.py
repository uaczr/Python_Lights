import time
from LLCommunicator import LLSignalToReactionEngine, LLReaction, LLSignal, LLSubscription, LLTopic, LLCommunicator, LLSignalToReactionEntry
from LLFiniteStateMachine import LLEvent, LLEventMatrix, LLFiniteStateMachine, LLTransitionEntry, LLTransitionMatrix, LLState
from LLLogic import LLLogic

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
        type, id = self.findTypeAndId(signal.path)
        print('Device of type {} with id {} changed to status {}'.format(type, id, signal.value))
        device = self.logic.find_device(type,id)
        device.set_status(signal.value)


    def findTypeAndId(self, path):
        type_begin = path.find("/")+1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]

class LLReactionButtonBox(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionButtonBox, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        type, id = self.findTypeAndId(signal.path)
        device = self.logic.find_device(type, id)
        if (device == -1):
            print('Error, Device not found')
        else:
            if(signal.value == "1"):
                print("Button on {} with id {} is pushed".format(type, id))
                device.set_button()
            else:
                print("Button on {} with id {} is not pushed".format(type, id))
                device.unset_button()

    def findTypeAndId(self, path):
        type_begin = path.find("/")+1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]


class LLReactionGameChange(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionButtonBox, self).__init__(name, eventmatrix)







if __name__ == "__main__":
    FsmEventMatrix = LLEventMatrix()
    reactionEngine = LLSignalToReactionEngine()
    communicator = LLCommunicator("127.0.0.1", 1883)
    logic = LLLogic(communicator)


    '''
    Events
    '''
    Stop = LLEvent("Stop")
    Start = LLEvent("Start")

    FsmEventMatrix.addEvent(Stop)
    FsmEventMatrix.addEvent(Start)


    '''
    Signals
    '''
    subscription_start = LLSubscription("start", "start", reactionEngine)
    subscription_stop = LLSubscription("stop", "stop", reactionEngine)
    subscription_configmode = LLSubscription("configmode", "configmode", reactionEngine)

    subscription_hello_type = LLSubscription("hello_type", "hello/type", reactionEngine)
    subscription_hello_mac = LLSubscription("hello_mac", "hello/mac", reactionEngine)

    subscription_device_stati = LLSubscription("device_status","devices/+/+/status", reactionEngine)
    subscription_buttonbox_buttons = LLSubscription("button","devices/StandardButtonBox/+/button", reactionEngine)

    signal_random_game = LLSignal("random_game", reactionEngine)
    signal_light_game = LLSignal("light_game", reactionEngine)
    signal_party_game = LLSignal("party_game", reactionEngine)


    '''
    Reactions
    '''
    reaction_stop = LLReactionStop("Stop", FsmEventMatrix, communicator)
    reaction_start = LLReactionStart("Start", FsmEventMatrix, communicator)
    reaction_configmode = LLReactionConfigMode("Configmode", FsmEventMatrix, communicator)
    reaction_hello_type = LLReactionHelloType("HelloType", FsmEventMatrix, logic)
    reaction_hello_mac = LLReactionHelloMac("HelloMac", FsmEventMatrix, logic)
    reaction_device_status = LLReactionDeviceStatus("DeviceStatus", FsmEventMatrix, logic)
    reaction_button_pressed = LLReactionButtonBox("ButtonPressed", FsmEventMatrix, logic)
    '''
    States
    '''
    state1 = LLState("Online")
    state1.addReaction(LLSignalToReactionEntry("stop", reaction_stop))
    state1.addReaction(LLSignalToReactionEntry("hello_type", reaction_hello_type))
    state1.addReaction(LLSignalToReactionEntry("hello_mac", reaction_hello_mac))
    state1.addReaction(LLSignalToReactionEntry("configmode", reaction_configmode))
    state1.addReaction(LLSignalToReactionEntry("device_status", reaction_device_status))
    state1.addReaction(LLSignalToReactionEntry("button", reaction_button_pressed))


    state2 = LLState("Offline")
    state2.addReaction(LLSignalToReactionEntry("start", reaction_start))

    '''
    Transitions
    '''
    FsmTransitionsMatrix = LLTransitionMatrix()
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(state1, Stop, state2))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(state2, Start, state1))

    '''
    FiniteStateMachine
    '''
    fsm = LLFiniteStateMachine(FsmEventMatrix, FsmTransitionsMatrix, reactionEngine)
    fsm.start(state1)

    '''
    Logic
    '''
    logic.start_registration()

    '''
    Communicator
    '''
    communicator.connect()
    communicator.addSubscription(subscription_start)
    communicator.addSubscription(subscription_stop)
    communicator.addSubscription(subscription_configmode)
    communicator.addSubscription(subscription_hello_mac)
    communicator.addSubscription(subscription_hello_type)
    communicator.addSubscription(subscription_device_stati)
    communicator.addSubscription(subscription_buttonbox_buttons)

    while(True):
        time.sleep(1)

