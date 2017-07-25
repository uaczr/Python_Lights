from LLCommunicator import LLSignalToReactionEntry, LLSignalToReactionEngine
from threading import Thread
from time import sleep

class LLState(object):
    signalToReactionMapping = []
    def __init__(self, name):
        self.name = name
        self.signalToReactionMapping = []

    def addReaction(self, signal2reaction):
        self.signalToReactionMapping.append(signal2reaction)

class LLTransitionEntry(object):
    def __init__(self, c_state, event, f_state, t_function=None):
        self.c_state = c_state
        self.event = event
        self.f_state = f_state
        self.t_function = t_function

class LLTransitionMatrix(object):
    transitionMatrix = []
    def __init__(self):
        self.transitionMatrix = []

    def addEntry(self, transitionEntry):
        self.transitionMatrix.append(transitionEntry)

    def getFutureState(self, current_state, event):
        for transition in self.transitionMatrix:
            if(transition.c_state.name == current_state.name):
                if(transition.event.name == event):
                    print("Transition to state {}".format(transition.f_state.name))
                    return transition

class LLEvent:
    name = ""
    triggered = False

    def __init__(self, name):
        self.name = name


class LLEventMatrix(object):
    events = []
    def __init__(self):
        print("Init EventMatrix")

    def addEvent(self, event):
        self.events.append(event)

    def triggerEvent(self, name):
        for event in self.events:
            if event.name == name:
                event.triggered = True

    def getTriggeredEvent(self):
        for event in self.events:
            if event.triggered == True:
                event.triggered = False
                print("Triggered event {}".format(event.name))
                return event.name
        return "None"


class LLFiniteStateMachine(object):
    current_event = 0
    current_state = 0
    eventMatrix = 0


    def __init__(self, eventMatrix, transistionMatrix, reactionEngine):
        self.eventMatrix = eventMatrix
        self.transitionMatrix = transistionMatrix
        self.reactionEngine = reactionEngine
        self.transition = None

    def start(self, start_transition):
        self.transition = start_transition
        self.reactionEngine.setSignal2ReactionList(self.transition.f_state.signalToReactionMapping)
        if self.transition.t_function is not None:
            self.transition.t_function()

        loop = Thread(target=self.loop_forever)
        loop.start()

    def loop_forever(self):
        while(True):
            self.current_event = self.eventMatrix.getTriggeredEvent()
            if self.current_event != "None":
                self.transition = self.transitionMatrix.getFutureState(self.transition.f_state, self.current_event)
                self.reactionEngine.setSignal2ReactionList(self.transition.f_state.signalToReactionMapping)
                if self.transition.t_function is not None:
                    self.transition.t_function()
            sleep(0.1)

    def set_state(self, state):
        self.current_state = state

