#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor, EV3GyroSensor
import brickpi3
import time
import classify
import room_search
import room_search_1
import mailroom
import mailroom2

RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")

QUICK_POWER = 35
CAREFUL_POWER = 22
Quick_SLOW_WHEEL = QUICK_POWER*(0.65)
Careful_SLOW_WHEEL = CAREFUL_POWER*(-0.4)

CORRECT_POWER = 0
CAREFUL_SAMPLING = 0.02
QUICK_SAMPLING = 0.05

C_sens = EV3ColorSensor(1)
T_sens = TouchSensor(2)
U_sens = EV3UltrasonicSensor(3)
G_sens = EV3GyroSensor(4)
BASELINE_ANGLE = 0


wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()

ON_LINE_DRIFT = 1                      # 1 for to the right, 0 for to the left
package_counter = 0
RIGHT_WHEEL.set_limits(100)
LEFT_WHEEL.set_limits(100)
ANGLE_COUNTER = 0

def get_out():
            angle1 = G_sens.get_abs_measure()
            wait_time = 0
            while (angle1 + BASELINE_ANGLE < -32 and wait_time < 0.3):
                if (T_sens.is_pressed()):
                    RIGHT_WHEEL.set_power(0)
                    LEFT_WHEEL.set_power(0)
                    reset_brick()
                    print("emergency stop detected in get_out")
                    exit()
                print(color)
                RIGHT_WHEEL.set_power(-15)
                LEFT_WHEEL.set_power(15)
                angle1 = G_sens.get_abs_measure()
                time.sleep(0.01)
                wait_time + 0.01
        
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            time.sleep(0.1)

while True:
    try:
        if (T_sens.is_pressed()):
            reset_brick()
            print("emergency stop detected")
            exit()

        time.sleep(0.005)
        def get_new_color():

            time.sleep(0.005)
            r, g, b = C_sens.get_rgb()
            intensity = r + g + b
            color = classify.classify_it(r, g, b, intensity)
            return color

        def turn_corner():
            print("turning corner")
            global BASELINE_ANGLE
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in turn_corner")
                exit()
            RIGHT_WHEEL.set_power(15)
            LEFT_WHEEL.set_power(15)
            time.sleep(1.7)
            angle = G_sens.get_abs_measure()
            
            while (angle + BASELINE_ANGLE > -85):
                try:
                    if (T_sens.is_pressed()):
                        RIGHT_WHEEL.set_power(0)
                        LEFT_WHEEL.set_power(0)
                        reset_brick()
                        print("emergency stop detected in turn_corner")
                        exit()
                    RIGHT_WHEEL.set_power(20)
                    LEFT_WHEEL.set_power(-20)
                    angle = G_sens.get_abs_measure()
                    
                    time.sleep(0.02)

                except Exception as e:
                    print(e)
            
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            BASELINE_ANGLE = -G_sens.get_abs_measure()
            return
    
        while True:
            color = get_new_color()
            distance = U_sens.get_value()
            
            if (package_counter > 1):
                mailroom2.mailroom2()
                
            if (ANGLE_COUNTER == 0):
                angle = G_sens.get_abs_measure()
                ANGLE_COUNTER = 8
            else:
                ANGLE_COUNTER = ANGLE_COUNTER - 1

            #print(distance, " angle: ", angle+BASELINE_ANGLE) 
            
            if (T_sens.is_pressed()):
                reset_brick()
                print("emergency stop detected")
                exit()

            if ((distance < 89) and (distance > 48) and (angle+BASELINE_ANGLE > -25) and package_counter != 2): #or (distance < 22)):   #add true to test with slow speed
                print("going fast")
                CORRECT_POWER = QUICK_POWER
                SLOW_WHEEL = Quick_SLOW_WHEEL
            else:
                CORRECT_POWER = CAREFUL_POWER
                SLOW_WHEEL = Careful_SLOW_WHEEL
            
            if ((-20 < angle+BASELINE_ANGLE < 15) and (distance < 22)):
                time.sleep(0.05)
                if (U_sens.get_value() < 20):
                    turn_corner()
                    

            if (color == "black"):
                RIGHT_WHEEL.set_power(CORRECT_POWER * 1.3)
                LEFT_WHEEL.set_power(SLOW_WHEEL * 1.3)
                
            if ("white" == color):
                if (True or angle+BASELINE_ANGLE < 20):
 #                   while (color != "black"):  
                        
                    RIGHT_WHEEL.set_power(SLOW_WHEEL*0.5)
                    LEFT_WHEEL.set_power(CORRECT_POWER*0.65)
                    #color = get_new_color()
                    
                    
                else:
                    RIGHT_WHEEL.set_power(CORRECT_POWER)
                    LEFT_WHEEL.set_power(SLOW_WHEEL)
            if (color == "orange"):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.2)
                RIGHT_WHEEL.set_position_relative(100)
                LEFT_WHEEL.set_position_relative(20)

                color = get_new_color()
                if (color == "yellow" and package_counter != 2):
                    RIGHT_WHEEL.set_power(0)
                    LEFT_WHEEL.set_power(0)
                    time.sleep(0.2)
                    package_dropped = package_counter + room_search_1.room_search()
                    print(package_dropped)
                    package_counter = package_counter + package_dropped
                    print("counter", package_counter)
                    get_out()
                    
                elif (color == "red"):
                    RIGHT_WHEEL.set_power(-CORRECT_POWER)
                    LEFT_WHEEL.set_power(CORRECT_POWER)
                    time.sleep(0.6)
                

    except Exception as e:
        if (isinstance(e, KeyboardInterrupt)):
            reset_brick()
            break
        else:
            print(e)
            continue
