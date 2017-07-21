import pygame
from LLCommunicator import LLSignal
from threading import Timer
import glob
import Settings

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

    def unpause_music(self):
        pygame.mixer.music.unpause()





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

    def create_timer(self, signal):
        Timer(signal.length / 1000, signal.signal).start()



