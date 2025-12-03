#!/usr/bin/python3
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor, EV3GyroSensor
import brickpi3
import time
import classify
import room_search
import room_search_1

# --- SETUP ---
RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")

QUICK_POWER = 33
CAREFUL_POWER = 23
Quick_SLOW_WHEEL = QUICK_POWER*(0.7)
Careful_SLOW_WHEEL = CAREFUL_POWER*(-0.4)

CORRECT_POWER = 0

C_sens = EV3ColorSensor(1)
T_sens = TouchSensor(2)
U_sens = EV3UltrasonicSensor(3)
G_sens = EV3GyroSensor(4)

# Initialize global variable here
BASELINE_ANGLE = 0 

wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()

ON_LINE_DRIFT = 1                      
package_counter = 0
RIGHT_WHEEL.set_limits(100)
LEFT_WHEEL.set_limits(100)

# --- FUNCTIONS DEFINED OUTSIDE THE LOOP ---

def get_new_color():
    time.sleep(0.01)
    r, g, b = C_sens.get_rgb()
    intensity = r + g + b
    color = classify.classify_it(r, g, b, intensity)
    return color

def turn_corner():
    print("turning corner")
    # Tell Python to use the variable defined at the top of the file
    global BASELINE_ANGLE 
    
    RIGHT_WHEEL.set_power(15)
    LEFT_WHEEL.set_power(15)
    time.sleep(2.5)
    
    angle = G_sens.get_abs_measure()
    
    # Your logic here:
    # If angle is -85 and Baseline is 0, sum is -85 (> -90) -> Continue Turning
    # If angle is -95 and Baseline is 0, sum is -95 (< -90) -> Stop Turning
    while (angle + BASELINE_ANGLE > -90):
        try:
            RIGHT_WHEEL.set_power(25)
            LEFT_WHEEL.set_power(-25)
            angle = G_sens.get_abs_measure()
            time.sleep(0.05)
        except Exception as e:
            print(e)
        
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    
    # Update the baseline so the next straight line is "0" again
    BASELINE_ANGLE += 90 
    return

# --- MAIN LOOP ---

while True:
    try:
        if (T_sens.is_pressed()):
            reset_brick()
            print("emergency stop detected")
            exit()

        time.sleep(0.01)

        # Loop logic starts here
        color = get_new_color()
        distance = U_sens.get_value()
        angle = G_sens.get_abs_measure()

        # Use the calculated relative angle for printing
        relative_angle = angle + BASELINE_ANGLE
        print(distance, " rel_angle: ", relative_angle) 
        
        # Logic using relative angle
        if ((distance < 81.9) and (distance > 45) and (relative_angle > -20) and package_counter != 2):
            print("going fast")
            CORRECT_POWER = QUICK_POWER
            SLOW_WHEEL = Quick_SLOW_WHEEL
        else:
            CORRECT_POWER = CAREFUL_POWER
            SLOW_WHEEL = Careful_SLOW_WHEEL
        
        # Turn logic using relative angle
        if ((-20 < relative_angle < 15) and (distance < 20)):
                turn_corner()
                # BASELINE_ANGLE is updated inside the function now

        if (color == "black"):
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(SLOW_WHEEL)
            
        if ("white" == color):
            RIGHT_WHEEL.set_power(SLOW_WHEEL)
            LEFT_WHEEL.set_power(CORRECT_POWER)

        if (color == "orange"):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            time.sleep(0.6)
            RIGHT_WHEEL.set_position_relative(100)
            LEFT_WHEEL.set_position_relative(70)

            color = get_new_color()
            if (color == "yellow" and package_counter != 2):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.2)
                package_counter = package_counter + room_search_1.room_search()
                
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
