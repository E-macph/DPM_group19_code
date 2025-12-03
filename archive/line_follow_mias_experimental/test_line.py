#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor, EV3GyroSensor
import brickpi3
import time
import classify
import room_search
import room_search_1
import mailroom

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
            print("Exiting office - backing up to doorway")
            
            # Step 1: Back up straight until we see orange (doorway)
            found_orange = False
            while not found_orange:
                if (T_sens.is_pressed()):
                    RIGHT_WHEEL.set_power(0)
                    LEFT_WHEEL.set_power(0)
                    reset_brick()
                    print("emergency stop detected in get_out")
                    exit()
                
                # Back up with weight compensation
                RIGHT_WHEEL.set_power(-20)
                LEFT_WHEEL.set_power(-21)  # 5% more for left-heavy robot
                time.sleep(0.01)
                
                r, g, b = C_sens.get_rgb()
                intensity = r + g + b
                color = classify.classify_it(r, g, b, intensity)
                
                if color == "orange":
                    # Verify it's actually orange
                    time.sleep(0.05)
                    r, g, b = C_sens.get_rgb()
                    intensity = r + g + b
                    color = classify.classify_it(r, g, b, intensity)
                    if color == "orange":
                        found_orange = True
            
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            time.sleep(0.1)
            print("Found orange doorway - turning to align with corridor")
            
            # Step 2: Turn left to face the corridor
            angle1 = G_sens.get_abs_measure()
            turn_timeout = 0
            while (angle1 + BASELINE_ANGLE < -15) and turn_timeout < 100:
                if (T_sens.is_pressed()):
                    RIGHT_WHEEL.set_power(0)
                    LEFT_WHEEL.set_power(0)
                    reset_brick()
                    print("emergency stop detected in get_out")
                    exit()
                
                RIGHT_WHEEL.set_power(-18)
                LEFT_WHEEL.set_power(19)  # 5% compensation
                angle1 = G_sens.get_abs_measure()
                time.sleep(0.01)
                turn_timeout += 1
        
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            time.sleep(0.1)
            print("Aligned - resuming line following")

while True:
    try:
        if (T_sens.is_pressed()):
            reset_brick()
            print("emergency stop detected")
            exit()

        time.sleep(0.005)
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
            
            if (package_counter == 2):
                mailroom.mailroom()
                
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

            # Speed control logic based on package counter
            if (package_counter == 2):
                # After 2 packages delivered, heading to mail room
                # Go FAST in safe straight sections (blue zones in photo)
                # Go SLOW near rooms/corners (red zone in photo)
                if ((80 < distance < 100) or (40 < distance < 60)) and (angle+BASELINE_ANGLE > -25):
                    # Blue zones: straight corridors away from corners
                    print("going fast - mail room search mode")
                    CORRECT_POWER = QUICK_POWER
                    SLOW_WHEEL = Quick_SLOW_WHEEL
                else:
                    # Red zone and everything else: near rooms, corners, or turning
                    CORRECT_POWER = CAREFUL_POWER
                    SLOW_WHEEL = Careful_SLOW_WHEEL
            else:
                # Normal delivery mode (0 or 1 packages)
                if ((distance < 89) and (distance > 48) and (angle+BASELINE_ANGLE > -25)):
                    print("going fast")
                    CORRECT_POWER = QUICK_POWER
                    SLOW_WHEEL = Quick_SLOW_WHEEL
                else:
                    CORRECT_POWER = CAREFUL_POWER
                    SLOW_WHEEL = Careful_SLOW_WHEEL
            
            if ((-20 < angle+BASELINE_ANGLE < 15) and (distance < 22)):
                time.sleep(0.05)
                if (U_sens.get_value() < 22):
                    turn_corner()
                    

            if (color == "black"):
                RIGHT_WHEEL.set_power(CORRECT_POWER * 1.40)
                LEFT_WHEEL.set_power(SLOW_WHEEL * 1.30)
                
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
                if (package_counter == 2):
                    # Heading to mail room - orange means we're at mail room entrance
                    print("Found orange - checking for blue mail room")
                    RIGHT_WHEEL.set_power(0)
                    LEFT_WHEEL.set_power(0)
                    time.sleep(0.2)
                    # Move forward to check what's inside
                    RIGHT_WHEEL.set_position_relative(80)
                    LEFT_WHEEL.set_position_relative(80)
                    time.sleep(0.5)
                    
                    color = get_new_color()
                    if (color == "blue"):
                        # Found mail room!
                        print("Found blue mail room - mission complete!")
                        mailroom.mailroom()
                    else:
                        # Not the mail room, back up and continue
                        print("Not mail room, continuing search")
                        RIGHT_WHEEL.set_power(-25)
                        LEFT_WHEEL.set_power(-26)
                        time.sleep(0.8)
                        RIGHT_WHEEL.set_power(0)
                        LEFT_WHEEL.set_power(0)
                else:
                    # Normal delivery mode
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
                        package_dropped = room_search_1.room_search()
                        print(package_dropped)
                        package_counter = package_counter + package_dropped
                        print("Back from room_search - resuming line following")
                        RIGHT_WHEEL.set_power(0)
                        LEFT_WHEEL.set_power(0)
                        
                    elif (color == "red"):
                        RIGHT_WHEEL.set_power(-CORRECT_POWER)
                        LEFT_WHEEL.set_power(CORRECT_POWER)
                        time.sleep(0.6)
            
            if (color == "blue" and package_counter == 2):
                # Found blue tile while line following - this is mail room
                print("Detected blue tile on path - entering mail room")
                mailroom.mailroom()
                

    except Exception as e:
        if (isinstance(e, KeyboardInterrupt)):
            reset_brick()
            break
        else:
            print(e)
            continue
