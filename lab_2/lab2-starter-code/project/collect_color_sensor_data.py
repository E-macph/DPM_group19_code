#!/usr/bin/env python3
# """ This test is used to collect data from the color sensor. It must be run on the robot. """
# Add your imports here, if any

import utils
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY_SEC = 0.01
COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
Color_Sensor = EV3ColorSensor(1)
Touch_sensor = TouchSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

def collect_color_sensor_data():
    "Collect color sensor data."
    try:
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while not Touch_sensor.is_pressed():
            pass  # do nothing while waiting for first button press #
        print("Touch sensor pressed")
        sleep(1)
        print("Starting to collect Color distance samples")

        while Touch_sensor.is_pressed():
            color_data = Color_Sensor.get_value(1)  # Float value in centimeters 0, capped to 255 cm

            if color_data is not None:  # If None is given, then data collection failed that time
                print(color_data)
                output_file.write(f"{color_data}\n")
            sleep(DELAY_SEC)

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        print("Done collecting color distance samples")
        output_file.close()
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    collect_color_sensor_data()
