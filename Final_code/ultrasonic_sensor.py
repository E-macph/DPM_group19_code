#!/usr/bin/env python3

"""
This test is used to collect data from the ultrasonic sensor.
It must be run on the robot.
"""

from utils.brick import (
    EV3UltrasonicSensor,
    wait_ready_sensors,
)
from time import sleep


DELAY_SEC = 0.01  # seconds of delay between measurements

print("Program start.\nWaiting for sensors to turn on...")
wait_ready_sensors(
    True
)  # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")


def get_distance_to_wall():
    total_data = 0
    average_data = 0
    for i in range(0, 100): # Get 100 set of data to get the average
        us_data = US_SENSOR.get_value()  # Float value in centimeters 0, capped to 255 cm
        if us_data is not None:  # If None is given, then data collection failed that time
        print(us_data)
        total_data += us_data
        sleep(DELAY_SEC)
    average_data = total_data / 100
    return average_data # Data returned to the main code

