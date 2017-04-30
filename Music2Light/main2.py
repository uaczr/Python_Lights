import time
from LLCommunicator import LLSignalToReactionEngine, LLReaction, LLSignal, LLSubscription, LLTopic, LLCommunicator, LLSignalToReactionEntry
from LLFiniteStateMachine import LLEvent, LLEventMatrix, LLFiniteStateMachine, LLTransitionEntry, LLTransitionMatrix, LLState

class LLReactionStop(LLReaction):
    def __init__(self, name, eventmatrix, communicator):
        super(LLReactionStop, self).__init__(name, eventmatrix)
        self.communicator = communicator

    def react(self, signal):
        print("Stop")
        self.eventmatrix.triggerEvent("Stop")

class LLReactionStart(LLReaction):
    def __init__(self, name, eventmatrix, communicator):
        super(LLReactionStart, self).__init__(name, eventmatrix)
        self.communicator = communicator

    def react(self, signal):
        print("Start")
        self.eventmatrix.triggerEvent("Start")

if __name__ == "__main__":
    FsmEventMatrix = LLEventMatrix()
    reactionEngine = LLSignalToReactionEngine()
    communicator = LLCommunicator("127.0.0.1", 1883)



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

    '''
    Reactions
    '''
    reaction_stop = LLReactionStop("Stop", FsmEventMatrix, communicator)
    reaction_start = LLReactionStart("Start", FsmEventMatrix, communicator)

    '''
    States
    '''
    state1 = LLState("Wait For Stop")
    state1.addReaction(LLSignalToReactionEntry(subscription_stop, reaction_stop))

    state2 = LLState("Wait For Start")
    state2.addReaction(LLSignalToReactionEntry(subscription_start, reaction_start))

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
    Communicator
    '''
    communicator.connect()
    communicator.addSubscription(subscription_start)
    communicator.addSubscription(subscription_stop)


    while(True):
        time.sleep(1)

