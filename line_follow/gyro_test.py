#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor, EV3GyroSensor
import brickpi3
import time
import classify
import room_search
import room_search_1

RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")

QUICK_POWER = 33
CAREFUL_POWER = 23
Quick_SLOW_WHEEL = QUICK_POWER*(0.7)
Careful_SLOW_WHEEL = CAREFUL_POWER*(-0.55)

CORRECT_POWER = 0
CAREFUL_SAMPLING = 0.02
QUICK_SAMPLING = 0.05

C_sens = EV3ColorSensor(1)
T_sens = TouchSensor(2)
U_sens = EV3UltrasonicSensor(3)
G_sens = EV3GyroSensor(4)

wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()

ON_LINE_DRIFT = 1                      # 1 for to the right, 0 for to the left
package_counter = 0
RIGHT_WHEEL.set_limits(100)
LEFT_WHEEL.set_limits(100)

while True:
    try:
        if (T_sens.is_pressed()):
            reset_brick()
            print("emergency stop detected")
            exit()

        time.sleep(0.5)
        def get_new_color():

            time.sleep(0.01)
            r, g, b = C_sens.get_rgb()
            intensity = r + g + b
            color = classify.classify_it(r, g, b, intensity)
            return color
        
        angle = G_sens.get_abs_measure()
        print("\nAngle: ", angle)
        print("US: ", U_sens.get_value())

        time.sleep(3)
        G_sens.set_mode(G_sens.Mode.DPS)
        G_sens.set_mode(G_sens.Mode.ABS)
        

    except Exception as e:
        if (isinstance(e, KeyboardInterrupt)):
            reset_brick()
            break
        else:
            print(e)
            continue
