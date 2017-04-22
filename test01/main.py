#################################################################
# Autor: Simon
# date: 2017-04-05
# Name: main
# Usage: manages all threads
#################################################################

"""import thread
import main_audio as audio
import main_communication as communication
import main_lightControll as lightControll

# Create threads
try:
    thread.start_new_thread(audio.extract_Rhythm, ())
    thread.start_new_thread(audio.extract_all, ())
    thread.start_new_thread(communication.main, ())
    thread.start_new_thread(lightControll.main, ())
except:
    print "Error: unable to start thread"

while 1:
    pass"""