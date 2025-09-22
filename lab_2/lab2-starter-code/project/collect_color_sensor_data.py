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
        color_data = 0
        print("Touch sensor pressed")
        sleep(1)
        print("Starting to collect Color distance samples")

        while color_data < 10:
            print("in color data list")
            if Touch_sensor.is_pressed():
                print("1")
                rgb_list = Color_Sensor.get_rgb()  # Float value in centimeters 0, capped to 255 cm
                print("2")
                sleep(0.5)
                print(rgb_list)
                print("3")

                if rgb_list is not None:  # If None is given, then data collection failed that time
                    print(rgb_list)
                    output_file.append(f"{rgb_list}\n")
                    color_data += 1
                    rgb_list = None

                sleep(DELAY_SEC)



    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print("Exception caught" + BaseException)
        pass
    finally:
        print("Done collecting color distance samples")
        output_file.close()
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()

if __name__ == "__main__":
    collect_color_sensor_data()
