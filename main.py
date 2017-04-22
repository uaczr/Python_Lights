#! /bin/bash
#################################################################
# Autor: Simon
# date: 2017-04-05
# Name: main
# Usage: manages all threads
#################################################################

from threading import Thread
from musicextraction import extract_rythm_worker, extract_all_worker
from music2light import music2light_worker

# Create threads
'''
Workerfunktionen keine Methoden!!!
Music2Light -> music2light_worker (Christoph)
ExtractRythm -> extract_rythm_worker (Simon)
ExtractAll -> extract_all_worker (Simon)
'''

if __name__ == "__main__":



    thread_music2light = Thread(target=music2light_worker) args=(arg1,arg2, )
    thread_extract_rythm = Thread(target=extract_rythm_worker ) #args=(arg1,arg2, )
    thread_extract_all = Thread(target=extract_all_worker) #args=(arg1,arg2, )
    try:
        thread_music2light.start()
        thread_extract_rythm.start()
        thread_extract_all.start()
    except:
        print "Error: unable to start thread"

    thread_music2light.join()
    thread_extract_rythm.stop()
    thread_extract_all.stop()
