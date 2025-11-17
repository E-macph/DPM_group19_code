#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor
import brickpi3
import time
import classify
RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")
POWER_LIMIT = 30
OFF_POWER = 0
CORRECT_POWER = 10
speed = 20
COLOR_SAMPLING = 0.02
MOTOR_SAMPLING = 0.05


BP = brickpi3.BrickPi3()
C_sens = EV3ColorSensor(1)

wait_ready_sensors(True)
RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()

RIGHT_WHEEL.set_limits(power=POWER_LIMIT)
LEFT_WHEEL.set_limits(power=POWER_LIMIT)

ON_LINE_DRIFT = 1                      # 1 for to the right, 0 for to the left


    



while True:
    try:
        

        r, g, b = C_sens.get_rgb()
        i = r+g+b
        time.sleep(0.5)
        print("\nR: ", r/i, "\nG: ", g/i, "\nB: ", b/i, "\nI: ", i)
        
        
        print(classify.classify_it(r, g, b, i))
        time.sleep(2)
        



    except Exception as e:
        if (isinstance(e, KeyboardInterrupt)):
            reset_brick()
            break
        else:
            print(e)
            continue
