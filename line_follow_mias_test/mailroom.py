#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor, EV3GyroSensor
import brickpi3
import time
import classify
import room_search
import room_search_1
import sound

DELI_NOTE = sound.Sound(duration=1, pitch="C", volume=100)
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

RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")
wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()


def mailroom():
    print("in mailroom")
    RIGHT_WHEEL.set_limits(30)
    LEFT_WHEEL.set_limits(30)
    QUICK_POWER = 35
    CAREFUL_POWER = 22
    Quick_SLOW_WHEEL = QUICK_POWER*(0.65)
    Careful_SLOW_WHEEL = CAREFUL_POWER*(-0.4)
    ON_LINE_DRIFT = 1                      # 1 for to the right, 0 for to the left
    package_counter = 0
    ANGLE_COUNTER = 0
    while True:
        try:
            if (T_sens.is_pressed()):
                reset_brick()
                print("emergency stop detected")
                exit()

            time.sleep(0.005)
            
            def check_input(input_color):
                counter = 0
                green_counter = 0
                while (counter < 10):
                    color = get_new_color()
                    if (color != input_color):
                        green_counter = green_counter -1
                    counter = counter +1
                    green_counter = green_counter + 1
                    time.sleep(0.01)
                    
                if (green_counter >= 7):
                    if (input_color == "green"):
                        package_orientation()
                    elif (input_color == "white"):
                        print("saw white")
                        return True
                    elif (input_color == "orange"):
                        return True
                else:
                    return False
                    
            def get_new_color():

                time.sleep(0.008)
                r, g, b = C_sens.get_rgb()
                intensity = r + g + b
                color = classify.classify_it(r, g, b, intensity)
                return color

            def turn_corner():
                print("turning corner")
                global BASELINE_ANGLE
                RIGHT_WHEEL.set_power(15)
                LEFT_WHEEL.set_power(15)
                time.sleep(1.5)
                angle = G_sens.get_abs_measure()
                
                while (angle + BASELINE_ANGLE > -85):
                    try:
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
                if (ANGLE_COUNTER == 0):
                    angle = G_sens.get_abs_measure()
                    ANGLE_COUNTER = 8
                else:
                    ANGLE_COUNTER = ANGLE_COUNTER - 1

                print(distance, " angle: ", angle + BASELINE_ANGLE) 
                
                if (T_sens.is_pressed()):
                    reset_brick()
                    print("emergency stop detected")
                    exit()

                if (False and not((distance < 89) and (distance > 48) and (angle+BASELINE_ANGLE > -25))): #or (distance < 22)):   #add true to test with slow speed
                    print("going fast")
                    CORRECT_POWER = QUICK_POWER
                    SLOW_WHEEL = Quick_SLOW_WHEEL
                else:
                    CORRECT_POWER = CAREFUL_POWER
                    SLOW_WHEEL = Careful_SLOW_WHEEL
                
                if ((-20 < angle+BASELINE_ANGLE < 15) and (distance < 22)and False):
                    time.sleep(0.05)
                    if (U_sens.get_value() < 22):
                        turn_corner()
                        

                if (color == "black"):
                    RIGHT_WHEEL.set_power(CORRECT_POWER * 1.25)
                    LEFT_WHEEL.set_power(SLOW_WHEEL * 1.15)
                    
                if ("white" == color):
                    if (True or angle+BASELINE_ANGLE < 20):
     #                   while (color != "black"):  
                            
                        RIGHT_WHEEL.set_power(SLOW_WHEEL*0.7)
                        LEFT_WHEEL.set_power(CORRECT_POWER*0.7)
                        #color = get_new_color()
                        
                        
                    else:
                        RIGHT_WHEEL.set_power(CORRECT_POWER)
                        LEFT_WHEEL.set_power(SLOW_WHEEL)
                        
                if (color == "blue"):
                    RIGHT_WHEEL.set_power(CORRECT_POWER)
                    LEFT_WHEEL.set_power(-CORRECT_POWER)
                    time.sleep(0.5)
                    
                if (color == "orange"):
                    if (check_input("orange")):
                        RIGHT_WHEEL.set_power(0)
                        LEFT_WHEEL.set_power(0)
                        time.sleep(0.2)
                        RIGHT_WHEEL.set_power(30)
                        LEFT_WHEEL.set_power(30)
                        time.sleep(0.4)
                        color = get_new_color()
                        if (color == "blue"):
                            if (check_input("blue")):
                                RIGHT_WHEEL.set_power(0)
                                LEFT_WHEEL.set_power(0)
                                DELI_NOTE.play()
                                DELI_NOTE.wait_done()
                                time.sleep(15)
                                print("stopped in mail room")
                        elif (color == "red"):
                            RIGHT_WHEEL.set_power(-30)
                            LEFT_WHEEL.set_power(-30)
                            time.sleep(0.4)
                            RIGHT_WHEEL.set_power(-30)
                            LEFT_WHEEL.set_power(30)
                            time.sleep(0.3)
                        

                    color = get_new_color()
                    if (color == "yellow"):
                        RIGHT_WHEEL.set_power(0)
                        LEFT_WHEEL.set_power(0)
                        time.sleep(0.2)
                        RIGHT_WHEEL.set_power(-30)
                        LEFT_WHEEL.set_power(30)
                        time.sleep(0.3)
                        
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

