############################################################################
# Autor: Simon Fritz
# Date: 2017.03.14
# Comment: This Code uses the standard-mode of essentia the streaming-mode will follow in the 2. release
#
############################################################################
import os
import json
import time
import numpy as np
import pyaudio
from essentia import Pool, array
from essentia.standard import *

# from essentia.streaming import *


WINDOWSIZE = 1024  # number of data points to read at a time
HOPSIZE = 512
RATE = 44100  # time resolution of the recording device (Hz)
# windowframe = np.

### microphone-Input
p = pyaudio.PyAudio()  # start the PyAudio class
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=RATE, input=True,
                frames_per_buffer=WINDOWSIZE)  # uses default input device

# initiate the frameBuffer once with the initial stream-data
frameBuffer = np.fromstring(stream.read(WINDOWSIZE), dtype=np.float32)

audio = frameBuffer

start = time.time()

lastOnset = 0
onsetCount = 0

# create a numpy array holding a single read of audio data
for i in range(100):  # to it a few times just to see

    data = np.fromstring(stream.read(WINDOWSIZE), dtype=np.float32)

    if (audio.size > 7000):
        audio = audio[WINDOWSIZE:]
        audio = np.hstack([audio, data])
    else:
        audio = np.hstack([audio, data])

    w = Windowing(type='hann')
    # spectrum = Spectrum()  # The spectrum of the frame # FFT() would return the complex FFT, here we just want the magnitude spectrum
    od1 = OnsetDetection(method='hfc')
    fft = FFT()  # this gives us a complex FFT
    c2p = CartesianToPolar()  # and this turns it into a pair (magnitude, phase)

    pool = Pool()

    for frame in FrameGenerator(audio, frameSize=1024, hopSize=512):
        mag, phase, = c2p(fft(w(frame)))
        pool.add('features.hfc', od1(mag, phase))
    onsets = Onsets()
    onsets_hfc = onsets(array([pool['features.hfc']]), [1])

    if (onsets_hfc.size >= 1):
        if (onsets_hfc[onsets_hfc.size - 1] > 0.03):
            if (lastOnset < onsets_hfc[onsets_hfc.size - 1]):
                # print onsets_hfc
                onsetCount += 1
                # print "lastOnset" + str(lastOnset)
                # print "newOnset" + str(onsets_hfc[onsets_hfc.size - 1])
                # print audio.size/44100.0
                print "latenz: " + str((audio.size / 44100.0 - lastOnset) * 1000) + " millisekunden"

            lastOnset = onsets_hfc[onsets_hfc.size - 1]
print str(onsetCount) + " Onsets in " + str(time.time() - start) + " Sekunden"

#################### MusicExtractor ##################

### command-line Python Music-extractor
# PATH_MusicExtractor = '/usr/local/bin/essentia_streaming_extractor_music'
# PATH_Buffer_File = '/home/snape6666/Schreibtisch/LichtUndLaessig/Buffer_File.wav'
# PATH_Output_File = '/home/snape6666/Schreibtisch/LichtUndLaessig/output_MusicExtractor.json'
# PATH_config_MusicExtractor = '/home/snape6666/Schreibtisch/LichtUndLaessig/config_MusicExtractor'

### execute MusicExtractor
## check Config-file after changing directory
# os.system(PATH_MusicExtractor + ' ' + PATH_Buffer_File + ' ' +  PATH_Output_File + ' ' +  PATH_config_MusicExtractor)

### open output.json
# with open(PATH_Output_File) as data_file:
#    data = json.load(data_file)

### danceability as string and Float32
# print(data["highlevel"]["danceability"]["value"])
# print(data["highlevel"]["danceability"]["probability"])
### genre_dortmund
## alternative, blues, electronic, folkcountry, funksoulrnb, jazz, pop, raphiphop, rock
# print(data["highlevel"]["genre_dortmund"]["all"])
# print(data["highlevel"]["genre_dortmund"]["probability"])
# print(data["highlevel"]["genre_dortmund"]["value"])

#################### MusicExtractor ##################

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()