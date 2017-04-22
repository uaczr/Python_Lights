#################################################################
# Autor: Simon
# date: 2017-04-05
# Name: audio_main
# Usage: extracts audio-features from microphone-stream
#################################################################
"""import os
import json
import numpy as np
import pyaudio
from essentia.standard import *

# https://github.com/MTG/essentia/issues/152
# erkennt alle Beats und die BPM
# Frage - laeuft das auch wenn es nur ein Auszug des Songs ist?
import essentia
import essentia.standard as es

fn = '/home/snape6666/Schreibtisch/LichtUndLaessig/Buffer_File.wav'

audio = es.MonoLoader(filename=fn)()
rhy = es.RhythmExtractor2013()

tes = rhy(audio)
# bpm, ticks, confidence, estimates, bpmIntervals

print tes
print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
print tes[1].size"""



"""
WINDOWSIZE = 1024  # number of data points to read at a time
HOPSIZE = 512
RATE = 44100  # time resolution of the recording device (Hz)

### microphone-Input
p = pyaudio.PyAudio()  # start the PyAudio class
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True,
                frames_per_buffer=WINDOWSIZE)  # uses default input device

# initiate the frameBuffer once with the initial stream-data
frameBuffer = np.fromstring(stream.read(WINDOWSIZE), dtype=np.float32)

i = 0
while i < 100:
    data = np.fromstring(stream.read(WINDOWSIZE), dtype=np.float32)

    if len(frameBuffer) != len(data):
        # save the new data into new windowframe
        windowframe = np.fromstring(data[:], dtype=np.float32)
        # save the 2. half of the previous window into the new windowframe
        windowframe[:HOPSIZE] = frameBuffer

        # Essentia
        # Instanciate the Window, Spectrum and mfcc
        w = Windowing(type='hann')



        # saves the 2. half of the Window and safes it into frameBuffer
    frameBuffer = np.fromstring(data[HOPSIZE:], dtype=np.float32)
    i += 1
print "fertig"
"""

# returns every tick BPM and Beat_detected
"""def extract_Rhythm():
    BPM = 10
    Beat_detected = 20



    return [BPM, Beat_detected]"""

"""def extract_all():
    ### command-line Python Music-extractor
    PATH_MusicExtractor = '/usr/local/bin/essentia_streaming_extractor_music'
    PATH_Buffer_File = '/home/snape6666/Schreibtisch/LichtUndLaessig/Buffer_File.wav'
    PATH_Output_File = '/home/snape6666/Schreibtisch/LichtUndLaessig/output_MusicExtractor.json'
    PATH_config_MusicExtractor = '/home/snape6666/Schreibtisch/LichtUndLaessig/config_MusicExtractor'

    ### execute MusicExtractor
    ## check Config-file after changing directory
    os.system(PATH_MusicExtractor + ' ' + PATH_Buffer_File + ' ' + PATH_Output_File + ' ' + PATH_config_MusicExtractor)

    # open output.json
    with open(PATH_Output_File) as data_file:
        data = json.load(data_file)

    ### danceability as string and Float32
    # print(data["highlevel"]["danceability"]["value"])
    # print(data["highlevel"]["danceability"]["probability"])
    ### genre_dortmund
    ## alternative, blues, electronic, folkcountry, funksoulrnb, jazz, pop, raphiphop, rock
    # print(data["highlevel"]["genre_dortmund"]["all"])
    print(data["highlevel"]["genre_dortmund"]["probability"])
    print(data["highlevel"]["genre_dortmund"]["value"])

    genre = getGenre(data)
    mood_agressive = data["highlevel"]["mood_aggressive"]["value"]
    mood_happy = data["highlevel"]["mood_happy"]["value"]
    mood_relaxed = data["highlevel"]["mood_relaxed"]["value"]
    mood_sad = data["highlevel"]["mood_sad"]["value"]
        # {"bright", "dark"}
    timber = data["highlevel"]["timber"]["value"]
        # {"tonal", "atonal"}
    tonal_atonal = data["highlevel"]["tonal_atonal"]["value"]
        # {"instrumental", "voice"}
    voice_instrumental = data["highlevel"]["voice_instrumental"]["value"]
        # {"Cluster1", "Cluster2", "Cluster3", "Cluster4", "Cluster5"}
        # Cluster_1: passionate, rousing, confident,boisterous, rowdy
        # Cluster_2: rollicking, cheerful, fun, sweet, amiable/good nature
        # Cluster_3: literate, poignant, wistful, bittersweet, autumnal, brooding
        # Cluster_4: humorous, silly, campy, quirky, whimsical, witty, wry
        # Cluster_5: aggressive, fiery,tense/anxious, intense, volatile,visceral
        # http://www.music-ir.org/mirex/wiki/2010%3AAudio_Music_Mood_Classification
    moods_mirex = data["highlevel"]["moods_mirex"]["value"]


    BPM = ["rhythm"]["bpm"]

    chords_key = data["tonal"]["chords_key"]
    chords_scale = data["tonal"]["chords_scale"]
    key_key = data["tonal"]["key_key"]
    key_scale = data["tonal"]["key_scale"]

    return 
"""

"""def getGenre(data):
    genre = data["highlevel"]["genre_dortmund"]["value"]

    if(genre == "electronic"):
        genre = data["highlevel"]["genre_electronic"]["value"]

    return genre
"""