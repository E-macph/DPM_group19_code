#!/usr/bin/env python3

"""
This test is used to collect data from the ultrasonic sensor.
It must be run on the robot.
"""

from utils import sound
from utils.brick import (
    TouchSensor,
    EV3UltrasonicSensor,
    wait_ready_sensors,
    reset_brick,
)
from time import sleep


DELAY_SEC = 0.01  # seconds of delay between measurements
US_SENSOR_DATA_FILE = "../data_analysis/us_sensor.csv"
SOUND = sound.Sound(duration=0.3, pitch="A4", volume=60)

print("Program start.\nWaiting for sensors to turn on...")

# Flute part of the program
US_SENSOR = EV3UltrasonicSensor(2)
NOTE_1 = sound.Sound(duration=0.03, pitch="A", volume=90)
NOTE_2 = sound.Sound(duration=0.03, pitch="B", volume=90)
NOTE_3 = sound.Sound(duration=0.03, pitch="C", volume=90)
NOTE_4 = sound.Sound(duration=0.03, pitch="D", volume=90)


# Test with touch sensors
TOUCH_SENSOR = TouchSensor(1)

wait_ready_sensors(
    True
)  # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")


def flute():
    us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
    if us_data is not None:  # If None is given, then data collection failed that time
        print(us_data)
        if us_data < 5.0:
            NOTE_1.play()
            NOTE_1.wait_done()
        elif 5.0 <= us_data < 10.0:
            NOTE_2.play()
            NOTE_2.wait_done()
        elif 10.0 <= us_data < 15.0:
            NOTE_3.play()
            NOTE_3.wait_done()
        elif 15.0 <= us_data < 20.0:
            NOTE_4.play()
            NOTE_4.wait_done()
        else:
            pass
    sleep(DELAY_SEC)


def play_flute():
    "Collect continuous data from the ultrasonic sensor for the flute"
    try:
        while not TOUCH_SENSOR.is_pressed():
            pass  # do nothing while waiting for first button press
        print("Touch sensor pressed")
        sleep(1)
        while not TOUCH_SENSOR.is_pressed():
            print("Flute playing")
            flute()
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    play_flute()