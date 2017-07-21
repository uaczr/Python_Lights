import time
import glob
from LLCommunicator import LLSignalToReactionEngine, LLReaction, LLSignal, LLSubscription, LLTopic, LLCommunicator, LLSignalToReactionEntry
from LLFiniteStateMachine import LLEvent, LLEventMatrix, LLFiniteStateMachine, LLTransitionEntry, LLTransitionMatrix, LLState
from LLLogic import LLLogic
from LLGame import soundplayer, gametimer, LLTimerSignal
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
    def __init__(self, name, eventmatrix, sound_player, sounds_path):
        super(LLReactionButtonBoxSound, self).__init__(name, eventmatrix)
        self.soundplayer = sound_player
        sound_paths = glob.glob(sounds_path + "*.wav")
        self.sounds = []
        for sound_path in sound_paths:
            self.sounds.append(self.soundplayer.load_sound(sound_path))

    def react(self, signal):
        type, id = self.findTypeAndId(signal.path)
        #device = self.logic.find_device(type, id)
        if(signal.value == "1"):
            print("Button on {} with id {} is pushed".format(type, id))
            if(len(self.sounds) > int(id)):
                self.soundplayer.play_sound(self.sounds[int(id)])
        else:
            print("Button on {} with id {} is not pushed".format(type, id))


class LLReactionButtonLight(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionButtonLight, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        type, id = self.findTypeAndId(signal.path)
        if (signal.value == "1"):
            i = -1
            print("Button on {} with id {} is pushed".format(type, id))
            for device in self.logic.devices:
                if (device.type == "StandardButtonBox"):
                    device.enable_light()
                if(device.type == "StandardLight"):
                    i += 1
                if(int(id) == i):
                    device.enable()

        else:
            print("Button on {} with id {} is not pushed".format(type, id))




class LLReactionJukeboxButton(LLReaction):
    def __init__(self, name, eventmatrix, logic, soundplayer):
        super(LLReactionButtonLight, self).__init__(name, eventmatrix)
        self.logic = logic
        self.soundplayer = soundplayer

        self.music_files = glob.glob(Settings.Cutsong_Music_Folder + "*.ogg")
        self.next_command = soundplayer.load_sound(Settings.Jukebox_Next_File)
        self.prev_command = soundplayer.load_sound(Settings.Jukebox_Previous_File)
        self.index = 0
        self.max = len(self.music_files)


    def react(self, signal):
        type, id = self.findTypeAndId(signal.path)
        i = 0

        if (signal.value == "1"):
            for device in self.logic.devices:
                if(device.type == "StandardButtonBox"):
                    if(i == 0):
                        self.soundplayer.play_sound(self.next_command)
                        self.soundplayer.load_music(self.music_files[self.index])
                        self.index += 1

                        if(self.index >= self.max):
                            self.index = 0

                    if(i == 1):
                        self.soundplayer.play_sound(self.prev_command)
                        self.index += 1

                        if(self.index < 0):
                            self.index = self.max - 1

                        self.soundplayer.load_music(self.music_files[self.index])
                    self.soundplayer.play_music()
                    i += 1







class LLReactionStopGameTimer(LLReaction):
    def __init__(self, name, eventmatrix):
        super(LLReactionStopGameTimer, self).__init__(name, eventmatrix)

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")
        signal.length = Settings.Orchester_Duration
        signal.game_timer.create_timer(signal)


class LLReactionOrchesterGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionOrchesterGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")
        signal.length = Settings.Jukebox_Duration
        signal.game_timer.create_timer(signal)


class LLReactionJukeboxGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionJukeboxGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")
        signal.length = Settings.Cutsong_Duration
        signal.game_timer.create_timer(signal)


class LLReactionCutsongGameTimer(LLReaction):
    def __init__(self, name, eventmatrix, logic):
        super(LLReactionCutsongGameTimer, self).__init__(name, eventmatrix)
        self.logic = logic

    def react(self, signal):
        print "React to signal {}".format(signal.name)
        self.eventmatrix.triggerEvent("Next")
        signal.length = Settings.Startup_Duration
        signal.game_timer.create_timer(signal)






if __name__ == "__main__":
    FsmEventMatrix = LLEventMatrix()
    reactionEngine = LLSignalToReactionEngine()
    communicator = LLCommunicator(Settings.Mqtt_Address, Settings.Mqtt_Port)
    logic = LLLogic(communicator)
    sound_player = soundplayer()
    game_timer = gametimer("Timer")

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
    subscription_configmode = LLSubscription("configmode", "configmode", reactionEngine)
    subscription_hello_type = LLSubscription("hello_type", "hello/+/type", reactionEngine)
    subscription_buttonbox_buttons = LLSubscription("button","devices/StandardButtonBox/+/button", reactionEngine)
    signal_current_game = LLSubscription("current_game", "currentgame", reactionEngine)
    signal_game_change = LLTimerSignal("game_change", reactionEngine, game_timer, type="random", length=Settings.Orchester_Duration)
    signal_cut_song = LLTimerSignal("beep_timer", reactionEngine, game_timer, type="random", length=5000)

    '''
    Reactions
    '''
    reaction_stop = LLReactionStop("Stop", FsmEventMatrix, communicator)
    reaction_start = LLReactionStart("Start", FsmEventMatrix, communicator)
    reaction_configmode = LLReactionConfigMode("Configmode", FsmEventMatrix, communicator)
    reaction_hello_type = LLReactionHelloType("HelloType", FsmEventMatrix, logic)

    # Stopped Reactions
    reaction_stopped_game_change = LLReactionStopGameTimer("StopGameTimer", FsmEventMatrix)

    # Orchester Reactions
    reaction_orchester_sound = LLReactionButtonBoxSound("ButtonPressedSound", FsmEventMatrix, sound_player, Settings.Orchester_Sounds_Folder)
    reaction_orchester_light = LLReactionButtonLight("ButtonPressedLight", FsmEventMatrix, logic)
    reaction_orchester_game_change = LLReactionOrchesterGameTimer("OrchesterGameTimer", FsmEventMatrix, logic)

    # Jukebox Reactions
    # reaction_jukebox_music
    reaction_jukebox_game_change = LLReactionJukeboxGameTimer("JukeboxGameTimer", FsmEventMatrix, logic)

    # Cutsong Reactions
    reaction_cutsong_game_change = LLReactionCutsongGameTimer("CutsongGameTimer", FsmEventMatrix, logic)


    '''
    States
    '''
    orchester_game = LLState("Orchester")
    orchester_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))
    orchester_game.addReaction(LLSignalToReactionEntry("button", [reaction_orchester_sound, reaction_orchester_light]))
    orchester_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_orchester_game_change, ]))


    jukebox_game = LLState("JukeBox")
    jukebox_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    jukebox_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    jukebox_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))

    # jukebox_game.addReaction(LLSignalToReactionEntry("button", [reaction_button_sound, reaction_button_light]))
    jukebox_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_jukebox_game_change, ]))

    cutsong_game = LLState("CutSong")
    cutsong_game.addReaction(LLSignalToReactionEntry("stop", [reaction_stop, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("hello_type", [reaction_hello_type, ]))
    cutsong_game.addReaction(LLSignalToReactionEntry("configmode", [reaction_configmode, ]))

    cutsong_game.addReaction(LLSignalToReactionEntry("game_change", [reaction_cutsong_game_change, ]))

    noshit_game = LLState("NoShit")




    stopped = LLState("Stopped")
    stopped.addReaction(LLSignalToReactionEntry("start", [reaction_start, ]))
    stopped.addReaction(LLSignalToReactionEntry("game_change", [reaction_stopped_game_change, ]))

    '''
    Transitions
    '''
    FsmTransitionsMatrix = LLTransitionMatrix()
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(stopped, Next, orchester_game))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(orchester_game, Next, jukebox_game))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(jukebox_game, Next, cutsong_game))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(cutsong_game, Next, orchester_game))
    FsmTransitionsMatrix.addEntry(LLTransitionEntry(noshit_game, Next, orchester_game))


    '''
    FiniteStateMachine
    '''
    fsm = LLFiniteStateMachine(FsmEventMatrix, FsmTransitionsMatrix, reactionEngine)
    fsm.start(LLTransitionEntry(stopped, Next, orchester_game))

    game_timer.create_timer(signal_game_change)

    '''
    Communicator
    '''
    communicator.connect()
    communicator.addSubscription(subscription_start)
    communicator.addSubscription(subscription_stop)
    communicator.addSubscription(subscription_configmode)
    communicator.addSubscription(subscription_hello_type)
    communicator.addSubscription(subscription_buttonbox_buttons)

    while(True):
        time.sleep(1000)

