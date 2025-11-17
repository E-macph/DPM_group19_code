#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor
import brickpi3
import time
import classify
import room_search

RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")

QUICK_POWER = 33
CAREFUL_POWER = 21
Quick_SLOW_WHEEL = QUICK_POWER*(0.6)
Careful_SLOW_WHEEL = CAREFUL_POWER*(-0.35)

CORRECT_POWER = 0
CAREFUL_SAMPLING = 0.02
QUICK_SAMPLING = 0.05

C_sens = EV3ColorSensor(1)
T_sens = TouchSensor(2)
U_sens = EV3UltrasonicSensor(3)

wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()

ON_LINE_DRIFT = 1                      # 1 for to the right, 0 for to the left

while True:
    try:
        if (T_sens.is_pressed()):
            reset_brick()
            exit

        time.sleep(0.01)
        def get_new_color():

            time.sleep(0.02)
            r, g, b = C_sens.get_rgb()
            intensity = r + g + b
            color = classify.classify_it(r, g, b, intensity)
            return color
        while True:
            
            color = get_new_color()
            distance = U_sens.get_value()
            if ((37.4 < distance < 46.2) or (95.4 > distance > 83.8) or (distance < 22)):
                CORRECT_POWER = CAREFUL_POWER
                SLOW_WHEEL = Careful_SLOW_WHEEL
            else:
                CORRECT_POWER = QUICK_POWER
                SLOW_WHEEL = Quick_SLOW_WHEEL

            if (color == "black"):
                RIGHT_WHEEL.set_power(CORRECT_POWER)
                LEFT_WHEEL.set_power(SLOW_WHEEL)
                
            if ("white" == color):
                RIGHT_WHEEL.set_power(SLOW_WHEEL)
                LEFT_WHEEL.set_power(CORRECT_POWER)

            if (color == "orange"):
                time.sleep(0.1)
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(1)
                RIGHT_WHEEL.set_position_relative(250)
                LEFT_WHEEL.set_position_relative(250)

                color = get_new_color()
                if (color == "yellow"):
                    room_search.room_search()


    except Exception as e:
        if (isinstance(e, KeyboardInterrupt)):
            reset_brick()
            break
        else:
            print(e)
            continue
