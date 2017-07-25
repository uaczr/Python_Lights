"""General"""
# Duration in milliseconds
Startup_Duration = 1000000
# Own IP address
# Mqtt_Address = "192.168.0.2"
Mqtt_Address = "127.0.0.1"

# MQTT Port
Mqtt_Port = 1883

"""Equipment"""
#DMXNebelmaschine
DMXNebelChannels = [
    # Index, Offstate, Onstate
    [0, 0, 255],
    [1, 0, 255],
    [2, 0, 255]
]

#DMXKanne
DMXKannenStart = 10
DMXKannenEnd = 15
DMXKannenStep = 5

ColorMap = [
    # R,G,B
    [255, 0, 0],
    [0, 0, 255],
    [0, 255, 0],
]

Seilwinde_Lifttime = 1000
Seilwinde_Droptime = 1000

ColorIndexMax = 89
PatternIndexMax = 41
StrobeIndexMax = 3
DimValMax = 255

"""Orchester"""

# Duration in milliseconds
Orchester_Duration = 1*1*1000

Orchester_Sounds_Folder = "Orchester_Sounds/"


"""Jukebox"""
# Duration in milliseconds
Jukebox_Duration = 5*60*1000

# Command audio files
Jukebox_Next_File = "Jukebox_Commands/Next.wav"
Jukebox_Previous_File = "Jukebox_Commands/Previous.wav"
Jukebox_Mode_File = ""

# Music files
Jukebox_Music_Folder = "Jukebox_Music/"


"""Cutsong"""
# Duration in milliseconds
Cutsong_Duration = 1*1*1000


Cutsong_Levels = [
    # mittlere Abspielzeit, Zeit Leuchten -> Musikstop, Zeit Musikstop -> Lose, WinDuration
    [2000, 300, 900, 30000],
    [1000, 200, 600, 40000],
    [500, 200, 500, 60000],
    [300, 200, 300, 80000]
]

# Music files
Cutsong_Music_Folder = "Cutsong_Music/"
Cutsong_Mode_File = "Cutsong_Commands/Start.wav"
Cutsong_Pling_File = "Cutsong_Commands/Pling.wav"
Cutsong_Lose_File = "Cutsong_Command/Lose.wav"
Cutsong_Win_File = "Cutsong_Command/Win.wav"
Cutsong_LevelFinishTime = 5000


"""Noshit"""
Noshit_Music_Folder = "Noshit_Music/"
Noshit_Duration = 1*60*1000


"""Pushallbuttons"""
Pushbuttons_Music_Folder = "Pushbutton_Music/"