"""General"""
# Duration in milliseconds
Startup_Duration = 1000000
# Own IP address
Mqtt_Address = "192.168.1.103"
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
DMXKannenEnd = 200
DMXKannenStep = 5

ColorMap = [
    # R,G,B
    [255, 0, 0],
    [0, 0, 255],
    [0, 255, 0],
]


"""Orchester"""

# Duration in milliseconds
Orchester_Duration = 1000000

Orchester_Sounds_Folder = "Orchester_Sounds/"


"""Jukebox"""
# Duration in milliseconds
Jukebox_Duration = 1000

# Command audio files
Jukebox_Next_File = "Jukebox_Commands/Next.wav"
Jukebox_Previous_File = "Jukebox_Commands/Previous.wav"
Jukebox_Mode_File = ""

# Music files
Jukebox_Music_Folder = "Jukebox_Music/"


"""Cutsong"""
# Duration in milliseconds
Cutsong_Duration = 1000

# Music files
Cutsong_Music_Folder = ""