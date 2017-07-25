#!/usr/bin/env python

import time
import glob
from LLCommunicator import LLSignalToReactionEngine, LLReaction, LLSignal, LLSubscription, LLTopic, LLCommunicator, LLSignalToReactionEntry
from LLFiniteStateMachine import LLEvent, LLEventMatrix, LLFiniteStateMachine, LLTransitionEntry, LLTransitionMatrix, LLState
from LLLogic import LLLogic
from LLGame import soundplayer, gametimer, LLTimerSignal, cutsongmanager, jukeboxmanager, noshitmanager, orchestermanager
import Settings


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
        hello_type = signal.value
        mac_start = signal.path.find("/") + 1
        mac_end = signal.path.find("/",mac_start)
        hello_mac = signal.path[mac_start:mac_end]
        self.logic.registration(hello_mac, hello_type)


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


class LLReactionButtonBoxSound(LLReaction):
    def __init__(self, name, eventmatrix, orchestermanager):
        super(LLReactionButtonBoxSound, self).__init__(name, eventmatrix)
        self.orchestermanager = orchestermanager

    def react(self, signal):
        if(signal.value == "1"):
            self.orchestermanager.reactionButton(signal)

        else:
            self.orchestermanager.reactionButtonOff(signal)


class LLReactionJukeboxButton(LLReaction):
    def __init__(self, name, eventmatrix, jukebox_manager):
        super(LLReactionJukeboxButton, self).__init__(name, eventmatrix)
        self.jukeboxmanager = jukebox_manager

    def react(self, signal):
        if (signal.value == "1"):
            self.jukeboxmanager.reactionButton(signal)


class LLReactionCutsongButton(LLReaction):
    def __init__(self, name, eventmatrix, cutsongmanager):
        super(LLReactionCutsongButton, self).__init__(name, eventmatrix)
        self.cutsongmanager = cutsongmanager

    def react(self, signal):
        print "CutSong: Reacting to Button"
        if(signal.value == "1"):
            self.cutsongmanager.reactionButton(signal)


class LLReactionCutsongTimer(LLReaction):
    def __init__(self, name, eventmatrix, cutsongmanager):
        super(LLReactionCutsongTimer, self).__init__(name, eventmatrix)
        self.cutsongmanager = cutsongmanager

    def react(self, signal):
        self.cutsongmanager.reactionTimer(signal)


class LLReactionNoshitButton(LLReaction):
    def __init__(self, name, eventmatrix, noshitmanager):
        super(LLReactionNoshitButton, self).__init__(name, eventmatrix)
        self.noshitmanager = noshitmanager

    def react(self, signal):
        if(signal.value == "1"):
            self.noshitmanager.reactionButton(signal)






class LLReactionStopGameTimer(LLReaction):
    def __init__(self, name, eventmatrix):
        super(LLReactionStopGameTimer, self).__init__(name, eventmatrix)

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")


class LLReactionOrchesterGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionOrchesterGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")


class LLReactionJukeboxGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionJukeboxGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")


class LLReactionCutsongGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionCutsongGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")

class LLReactionNoshitGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionNoshitGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")

class LLReactionNext(LLReaction):
    def __init__(self, name, eventmatrix):
        super(LLReactionNext, self).__init__(name, eventmatrix)

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")




if __name__ == "__main__":
    FsmEventMatrix = LLEventMatrix()
    reactionEngine = LLSignalToReactionEngine()
    communicator = LLCommunicator(Settings.Mqtt_Address, Settings.Mqtt_Port)
    logic = LLLogic(communicator)
    sound_player = soundplayer()
    game_timer = gametimer("Timer")
    cutsong_timer = gametimer("Songtimer")


    '''
    Events
    '''
    Stop = LLEvent("Stop")
    Next = LLEvent("Next")

    FsmEventMatrix.addEvent(Stop)
    FsmEventMatrix.addEvent(Next)




    '''
    Signals
    '''
    subscription_start = LLSubscription("start", "start", reactionEngine)
    subscription_stop = LLSubscription("stop", "stop", reactionEngine)
    subscription_next = LLSubscription("next", "next", reactionEngine)
    subscription_configmode = LLSubscription("configmode", "configmode", reactionEngine)
    subscription_hello_type = LLSubscription("hello_type", "hello/+/type", reactionEngine)
    subscription_buttonbox_buttons = LLSubscription("button","devices/StandardButtonBox/+/button", reactionEngine)
    signal_current_game = LLSubscription("current_game", "currentgame", reactionEngine)
    signal_game_change = LLTimerSignal("game_change", reactionEngine, game_timer, type="random", length=Settings.Orchester_Duration)
    signal_cutsong_timer = LLTimerSignal("cutsong_timer", reactionEngine, cutsong_timer, type="random", length=5000)

    orchester_manager = orchestermanager(game_timer, signal_game_change, sound_player, subscription_buttonbox_buttons, logic)
    cutsong_manager = cutsongmanager(game_timer, signal_game_change, sound_player, cutsong_timer, signal_cutsong_timer, subscription_buttonbox_buttons, logic)
    jukebox_manager = jukeboxmanager(game_timer, signal_game_change, sound_player, subscription_buttonbox_buttons, logic)
    noshit_manager = noshitmanager(game_timer, signal_game_change, sound_player, subscription_buttonbox_buttons, logic)

    '''
    Reactions
    '''
    reaction_stop = LLReactionStop("Stop", FsmEventMatrix, communicator)
    reaction_start = LLReactionStart("Start", FsmEventMatrix, communicator)
    reaction_configmode = LLReactionConfigMode("Configmode", FsmEventMatrix, communicator)
    reaction_hello_type = LLReactionHelloType("HelloType", FsmEventMatrix, logic)
    reaction_next = LLReactionNext("Next", FsmEventMatrix)

    # Stopped Reactions
    reaction_stopped_game_change = LLReactionStopGameTimer("StopGameTimer", FsmEventMatrix)

    # Orchester Reactions
    reaction_orchester_sound = LLReactionButtonBoxSound("ButtonPressedSound", FsmEventMatrix, orchester_manager)
    reaction_orchester_game_change = LLReactionOrchesterGameTimer("OrchesterGameTimer", FsmEventMatrix, logic)

    # Jukebox Reactions
    reaction_jukebox_music = LLReactionJukeboxButton("JukeboxButton", FsmEventMatrix, jukebox_manager)
    reaction_jukebox_game_change = LLReactionJukeboxGameTimer("JukeboxGameTimer", FsmEventMatrix, logic)

    # Cutsong Reactions
    reaction_cutsong_game_change = LLReactionCutsongGameTimer("CutsongGameTimer", FsmEventMatrix, logic)
    reaction_cutsong_button = LLReactionCutsongButton("CutsongGameButton", FsmEventMatrix, cutsong_manager)
    reaction_cutsong_timer = LLReactionCutsongTimer("CutsongGameTimer", FsmEventMatrix, cutsong_manager)

    reaction_noshit_game_change = LLReactionNoshitGameTimer("NoshitGameTimer", FsmEventMatrix, logic)
    reaction_noshit_button = LLReactionNoshitButton("NoshitButton", FsmEventMatrix, noshit_manager)


    '''
    States
    '''
    orchester_game = LLState("Orchester")
    orchester_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("button", [reaction_orchester_sound, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_orchester_game_change, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("next", [reaction_next, ]))


    jukebox_game = LLState("JukeBox")
    jukebox_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    jukebox_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    jukebox_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))
    jukebox_game.addReaction(LLSignalToReactionEntry("next", [reaction_next, ]))

    jukebox_game.addReaction(LLSignalToReactionEntry("button", [reaction_jukebox_music, ]))
    jukebox_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_jukebox_game_change, ]))

    cutsong_game = LLState("CutSong")
    cutsong_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("next", [reaction_next, ]))

    cutsong_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_cutsong_game_change, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("button", [reaction_cutsong_button, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("cutsong_timer", [reaction_cutsong_timer, ]))

    noshit_game = LLState("NoShit")
    noshit_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    noshit_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    noshit_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))
    noshit_game.addReaction(LLSignalToReactionEntry("next", [reaction_next, ]))

    noshit_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_noshit_game_change, ]))
    noshit_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_noshit_button, ]))






    stopped = LLState("Stopped")
    stopped.addReaction(LLSignalToReactionEntry("start", [reaction_start, ]))
    stopped.addReaction(LLSignalToReactionEntry("game_change", [reaction_stopped_game_change, ]))

    '''
    Transitions
    '''
    FsmTransitionsMatrix = LLTransitionMatrix()
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(stopped, Next, orchester_game, orchester_manager.transition))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(orchester_game, Next, jukebox_game, jukebox_manager.transition))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(jukebox_game, Next, cutsong_game, cutsong_manager.transition))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(cutsong_game, Next, noshit_game, noshit_manager.transition))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(noshit_game, Next, orchester_game, orchester_manager.transition))


    '''
    FiniteStateMachine
    '''
    fsm = LLFiniteStateMachine(FsmEventMatrix, FsmTransitionsMatrix, reactionEngine)
    fsm.start(LLTransitionEntry(stopped, Next, orchester_game, orchester_manager.transition))

    '''
    Communicator
    '''
    communicator.connect()
    communicator.addSubscription(subscription_start)
    communicator.addSubscription(subscription_stop)
    communicator.addSubscription(subscription_configmode)
    communicator.addSubscription(subscription_hello_type)
    communicator.addSubscription(subscription_buttonbox_buttons)
    communicator.addSubscription(subscription_next)

    while(True):
        time.sleep(1)

