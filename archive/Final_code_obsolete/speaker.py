
from utils import sound
from utils.brick import (
    TouchSensor,
    EV3UltrasonicSensor,
    wait_ready_sensors,
    reset_brick,
)
from time import sleep


# Setup 
SOUND = sound.Sound(duration=0.3, pitch="A4", volume=60)
NOTE_1 = sound.Sound(duration=0.03, pitch="A", volume=90)
NOTE_2 = sound.Sound(duration=0.03, pitch="B", volume=90)
NOTE_3 = sound.Sound(duration=0.03, pitch="C", volume=90)
NOTE_4 = sound.Sound(duration=0.03, pitch="D", volume=90)

musics = {
    "delivery": [NOTE_1, NOTE_2],
    "mission_complete": [NOTE_3, NOTE_4, NOTE_1]
}

# name can be "delivery" ot "mission_complete"
def play_music(name):
    # Determine the music to play
    music = musics[name]
    for note in music:
        note.play()
        note.wait_complete()