

def init():
    #Zeit wird durch time.time() bestimt
    global predicted_beat_time = 0#Zeit des nächsten Beat in time.time() Zeit
    global beat_strength = 0.0f #Stärke des Beat
    global mood = [] #Möglichkeiten ["happy","sad","..."]
    global genre = "" #Möglichkeiten ["Electric","Rock","..."]
    global beat_period = 0.0f #1/bpm
