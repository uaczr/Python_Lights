import pygame
from LLCommunicator import LLSignal, LLTopic
from threading import Timer
import glob
import Settings
import random, time

class soundplayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        print("Soundplayer initialised.")



    def load_sound(self, path):
        return pygame.mixer.Sound(path)

    def play_sound(self, sound):
        sound.play()

    def load_music(self, path):
        pygame.mixer.music.load(path)

    def play_music(self):
        pygame.mixer.music.play()

    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()

    def fadeout_music(self):
        pygame.mixer.fadeout(Settings.Cutsong_LevelFinishTime)

    def unpause_music(self):
        pygame.mixer.music.unpause()

    def pos_music(self):
        return pygame.mixer.music.get_pos()





class LLTimerSignal(LLSignal):
    def __init__(self, name, signal2Reaction, game_timer, type="random", length=10000):
        super(LLTimerSignal, self).__init__(name, signal2Reaction)
        self.type = type
        self.length = length
        self.game_timer = game_timer

    def signal(self):
        print "Signal {} was triggered".format(self.name)
        self.signal2Reaction.signal2reaction(self)



class gametimer:
    def __init__(self, name):
        print "Initialised Game Timer {}".format(name)
        self.Timer = None

    def create_timer(self, signal):
        self.Timer = Timer(signal.length / 1000, signal.signal)
        self.Timer.start()

    def kill_timer(self):
        if self.Timer is not None:
            self.Timer.cancel()
            self.Timer = None


class cutsongmanager:
    def __init__(self, game_timer, signal,  sound_player, gametimer, timersignal, buttonsignal, logic):
        self.game_timer = game_timer
        self.timer_signal = signal
        self.state = "Start"
        self.timer = gametimer
        self.sound_player = sound_player
        self.music_files = glob.glob(Settings.Cutsong_Music_Folder + "/*.ogg")
        self.max = len(self.music_files)
        self.music_index = 0
        self.timersignal = timersignal
        self.buttonsignal = buttonsignal
        self.logic = logic
        self.wantedButtonNum = -1
        self.wantedButton = None
        self.currentLevel = 0
        self.counter = 0
        self.songlength = 0
        self.currentrest = 0

    def findTypeAndId(self, path):
        type_begin = path.find("/") + 1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]

    def transition(self):
        self.logic.disable_all()
        self.sound_player.stop_music()
        for button in self.logic.buttons:
            button.enable_light()
        self.counter = 0
        self.currentLevel = 0
        self.logic.change_red()
        self.logic.level1_lights()
        self.timer_signal.length = Settings.Cutsong_Duration
        self.game_timer.kill_timer()
        self.game_timer.create_timer(self.timer_signal)

    def reactionButton(self, signal):
        if(self.state == "Start"):
            print "Cutsong: Starting Cutsong Game"
            mode = self.sound_player.load_sound(Settings.Cutsong_Mode_File)
            self.sound_player.play_sound(mode)

            if self.music_index >= self.max:
                self.music_index = 0
            self.timersignal.length = 2000
            self.timer.create_timer(self.timersignal)
            self.state = "Play_Intro"
            for button in self.logic.buttons:
                button.disable()
            return

        if(self.state == "Game_Waiting" or self.state == "Game_Waiting2"):
            type, id = self.findTypeAndId(signal.path)
            if(int(id) == self.wantedButton.id):
                print "Cutsong: Right Button pressed"
                self.timer.kill_timer()
                pling = self.sound_player.load_sound(Settings.Cutsong_Pling_File)
                self.sound_player.play_sound(pling)
                self.state = "Game_Started"
                self.counter += 1
                self.sound_player.unpause_music()

                self.currentrest = self.songlength - self.sound_player.pos_music()/1000
                print "Cutsong: Songrest {}".format(self.currentrest)
                if(self.currentrest <= Settings.Cutsong_Levels[self.currentLevel][3]/1000):
                    print "Cutsong: Level geschafft"
                    self.state = "Level_Finished"
                    win = self.sound_player.load_sound(Settings.Cutsong_Win_File)
                    self.sound_player.play_sound(win)
                    self.timersignal.length = Settings.Cutsong_LevelFinishTime
                    self.timer.create_timer(self.timersignal)
                    self.counter = 0
                    self.logic.level0_lights
                    for button in self.logic.buttons:
                        button.flash_light(7)
                    return
                lightlevel = int(self.currentrest/4)
                if int(lightlevel) == 0:
                    self.logic.level1_lights()

                if int(lightlevel) == 1:
                    self.logic.level2_lights()

                if int(lightlevel) == 2:
                    self.logic.level3_lights()

                if int(lightlevel) == 3:
                    self.logic.level4_lights()


                self.timersignal.length = (self.currentrest / self.songlength + 0.5) * random.uniform(0.2, 1.5) * Settings.Cutsong_Levels[self.currentLevel][0]
                self.timer.create_timer(self.timersignal)
                self.wantedButton.disable()

                return
            else:
                print "Cutsong: Wrong Button pressed"
                self.sound_player.pause_music()
                time.sleep(0.2)
                lose = self.sound_player.load_sound(Settings.Cutsong_Pling_File)
                self.sound_player.play_sound(lose)
                self.state = "Start"
                self.counter = 0
                self.currentLevel = 0
                self.wantedButton.disable()
                return



    def reactionTimer(self, signal):
        if(self.state == "Play_Intro"):
            print "Cutsong: Playing Introduction"
            musicfile = self.music_files[random.randrange(0, self.max)]
            self.songlength = self.sound_player.load_sound(musicfile).get_length()
            print "Cutsong: Songlength {}".format(self.songlength)
            self.sound_player.load_music(musicfile)
            self.music_index += 1
            self.sound_player.play_music()
            self.state = "Game_Started"
            self.timersignal.length = 5000
            self.logic.level1_lights()
            self.game_timer.kill_timer()
            self.timer.create_timer(self.timersignal)
            return

        if(self.state == "Game_Started"):
            print "Cutsong: Game Started"

            num = len(self.logic.buttons)
            # Buttons mussen Angeschlossen sein
            self.wantedButtonNum = random.randrange(0, num)
            self.wantedButton = self.logic.buttons[self.wantedButtonNum]
            self.wantedButton.enable_light()
            self.timersignal.length = (self.currentrest / self.songlength + 0.5) * Settings.Cutsong_Levels[self.currentLevel][1]
            self.timer.create_timer(self.timersignal)
            self.state = "Game_Waiting"
            return

        if (self.state == "Game_Waiting"):
            self.timersignal.length = (self.currentrest / self.songlength + 0.5) * Settings.Cutsong_Levels[self.currentLevel][2]
            self.timer.create_timer(self.timersignal)
            self.sound_player.pause_music()
            self.state = "Game_Waiting2"
            self.sound_player.pause_music()
            return

        if (self.state == "Game_Waiting2"):
            print "Cutsong: Timeout"
            self.sound_player.pause_music()
            time.sleep(0.2)
            lose = self.sound_player.load_sound(Settings.Cutsong_Pling_File)
            self.sound_player.play_sound(lose)
            self.state = "Start"
            self.counter = 0
            self.currentLevel = 0
            self.wantedButton.disable()
            return

        if (self.state == "Game_Waiting2"):
            print "Cutsong: Timeout"
            self.sound_player.pause_music()
            time.sleep(0.2)
            lose = self.sound_player.load_sound(Settings.Cutsong_Pling_File)
            self.sound_player.play_sound(lose)
            self.state = "Start"
            self.counter = 0
            self.currentLevel = 0
            self.wantedButton.disable()
            return

        if(self.state == "Level_Finished"):
            print "Doing Something nice"
            self.logic.level5_lights()
            self.currentLevel += 1
            self.currentrest = self.songlength - self.sound_player.pos_music()/1000
            self.timersignal.length = self.currentrest
            if self.currentLevel == 0:
                print "Cutsong: Level 0 Win"

            if self.currentLevel == 1:
                print "Cutsong: Level 1 Win"

            if self.currentLevel == 2:
                print "Custong: Level 2 Win"

            if self.currentLevel >= 3:
                print " Cutsong: Level >3 Win"


            self.timer.create_timer(self.timersignal)
            self.state = "Play_Intro"
            return


class jukeboxmanager:
    def __init__(self, game_timer, signal,  sound_player, buttonsignal, logic):
        self.game_timer = game_timer
        self.timer_signal = signal
        self.soundplayer = sound_player
        self.buttonsignal = buttonsignal
        self.logic = logic
        self.music_files = glob.glob(Settings.Jukebox_Music_Folder + "*.ogg")
        self.next_command = sound_player.load_sound(Settings.Jukebox_Next_File)
        self.prev_command = sound_player.load_sound(Settings.Jukebox_Previous_File)
        self.index = 0
        self.max = len(self.music_files)
        self.next_id = -1
        self.previous_id = -1
        print "Found {} Jukebox Music Files".format(self.max)
        self.timer = Timer(1, self.music_stopped)

    def findTypeAndId(self, path):
        type_begin = path.find("/") + 1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]

    def reactionButton(self, signal):
        type, id = self.findTypeAndId(signal.path)
        if type == "StandardButtonBox":
            if int(id) == self.next_id:
                print("Jukebox: Play Next!")
                if self.timer.isAlive():
                    self.timer.cancel()
                self.soundplayer.play_sound(self.next_command)
                length = self.soundplayer.load_sound(self.music_files[self.index]).get_length()
                self.soundplayer.load_music(self.music_files[self.index])
                self.index += 1

                if self.index >= self.max:
                    self.index = 0
                self.soundplayer.play_music()
                self.timer = Timer(length, self.music_stopped)
                self.timer.start()
                self.logic.level2_lights()

            if int(id) == self.previous_id:
                print("Jukebox: Play Previous!")
                if self.timer.isAlive():
                    self.timer.cancel()
                self.soundplayer.play_sound(self.prev_command)
                self.index -= 1

                if self.index < 0:
                    self.index = self.max - 1
                length = self.soundplayer.load_sound(self.music_files[self.index]).get_length()
                self.soundplayer.load_music(self.music_files[self.index])
                self.soundplayer.play_music()
                self.timer = Timer(length, self.music_stopped)
                self.timer.start()
                self.logic.level2_lights()

    def music_stopped(self):
        self.logic.level1_lights()

    def transition(self):
        self.logic.disable_all()
        self.soundplayer.stop_music()
        self.timer_signal.length = Settings.Jukebox_Duration
        self.game_timer.kill_timer()
        self.game_timer.create_timer(self.timer_signal)
        # Set Next and Previous buttons and enable their light
        if len(self.logic.buttons) >= 2:
            self.logic.buttons[0].enable_light()
            self.logic.buttons[1].enable_light()
            self.next_id = self.logic.buttons[0].id
            self.previous_id = self.logic.buttons[1].id
        else:
            self.next_id = -1
            self.previous_id = -1
        # Switch on Level1 Ligths - DMX
        self.logic.change_red()
        self.logic.level1_lights()

class noshitmanager:
    def __init__(self, game_timer, signal, sound_player, buttonsignal, logic):
        self.game_timer = game_timer
        self.timer_signal = signal
        self.soundplayer = sound_player
        self.buttonsignal = buttonsignal
        self.logic = logic
        self.soundsamples = glob.glob(Settings.Noshit_Music_Folder + "/*.ogg")
        self.max = len(self.soundsamples)
        print "Noshit Found {} Music Samples".format(self.max)

    def transition(self):
        self.logic.disable_all()
        self.soundplayer.stop_music()
        self.timer_signal.length = Settings.Noshit_Duration
        self.game_timer.create_timer(self.timer_signal)
        self.logic.change_red()
        self.logic.level1_lights()


    def reactionButton(self, signal):
        sound = self.soundplayer.load_sound(self.soundsamples[random.randrange(0, self.max)])
        self.soundplayer.play_sound(sound)


class orchestermanager:
    def __init__(self, game_timer, signal, sound_player, buttonsignal, logic):
        self.game_timer = game_timer
        self.timer_signal = signal
        self.soundplayer = sound_player
        self.buttonsignal = buttonsignal
        self.logic = logic


        sound_paths = glob.glob(Settings.Orchester_Sounds_Folder + "*.wav")
        self.sounds = []
        self.logic = logic
        for sound_path in sound_paths:
            self.sounds.append(self.soundplayer.load_sound(sound_path))

    def findTypeAndId(self, path):
        type_begin = path.find("/") + 1
        type_end = path.find("/", type_begin)
        id_begin = type_end + 1
        id_end = path.find("/", id_begin)
        return path[type_begin:type_end], path[id_begin:id_end]

    def reactionButton(self, signal):
        type, id = self.findTypeAndId(signal.path)
        i = 0
        for button in self.logic.buttons:
            if int(id) == button.id:
                self.soundplayer.play_sound(self.sounds[i])
                button.flash_light(1)
                break
            i += 1

        if len(self.logic.barlights) > i:
            self.logic.barlights[i].flash_light()

    def transition(self):
        self.logic.disable_all()
        self.soundplayer.stop_music()
        self.game_timer.kill_timer()
        self.timer_signal.length = Settings.Orchester_Duration
        self.game_timer.create_timer(self.timer_signal)
        self.logic.change_red()
        self.logic.level1_lights()

class pushallbuttonsmanager:
    def __init__(self, game_timer, signal, sound_player, buttonsignal, logic):
        self.game_timer = game_timer
        self.timer_signal = signal
        self.soundplayer = sound_player
        self.buttonsignal = buttonsignal
        self.logic = logic
        self.music_files = Settings.Pushbuttons_Music_Folder

