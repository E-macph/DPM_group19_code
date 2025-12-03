#!/usr/bin/python3

import sound
import os

os.system("beep -f 440 -l 1000")

NOTE = sound.Sound(duration=1, pitch = "A#4", volume=60)

NOTE.play()
NOTE.wait_done()
