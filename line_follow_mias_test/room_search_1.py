from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, TouchSensor
import brickpi3
import time
import classify
import drop_package
import sound

NOTE_DROPPED = sound.Sound(duration=0.5, pitch="D", volume=100)

def room_search():
    RIGHT_WHEEL = Motor("C")
    LEFT_WHEEL = Motor("B")
    T_sens = TouchSensor(2)
    
    
    POWER_LIMIT = 30
    OFF_POWER = 0
    CORRECT_POWER = 30
    speed = 20
    COLOR_SAMPLING = 0.02
    MOTOR_SAMPLING = 0.05

    C_sens = EV3ColorSensor(1)

    wait_ready_sensors(True)
    RIGHT_WHEEL.reset_encoder()
    LEFT_WHEEL.reset_encoder()
    goout = 0
    dropped_package = 0
    RIGHT_WHEEL.set_limits(30)
    LEFT_WHEEL.set_limits(30)
    
    def get_new_color():
        time.sleep(0.01)
        r, g, b = C_sens.get_rgb()
        intensity = r + g + b
        color = classify.classify_it(r, g, b, intensity)
        return color
    
    def check_input(input_color):
        counter = 0
        green_counter = 0
        while (counter < 10):
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in check_input")
                exit()
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

    def package_orientation():
        #move foward and right a bit
        #then drop package
        #then back and around package
        nonlocal dropped_package
        print("dropping package")
        if (dropped_package == 1):
            return
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected in package_orientation")
            exit()
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.3)
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected in package_orientation")
            exit()
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER * 1.05)
        time.sleep(0.7)
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected in package_orientation")
            exit()
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        drop_package.drop_package()
        NOTE_DROPPED.play()
        NOTE_DROPPED.wait_done()
        goout = 1
        dropped_package = 1
        
        # Immediately back out after dropping package
        print("Package dropped - backing out of office")
        back_out()
        
        
    def move_forward():
        nonlocal dropped_package
        inYellow = True;
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER * 1.05)
        time.sleep(0.3)
        while(inYellow):
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in room_search")
                exit()
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(CORRECT_POWER * 1.05)
            time.sleep(0.01)
            color = get_new_color()
            if (color == "green" and dropped_package == 0):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.1)
                check_input("green")
            elif (color == "white" or color == "orange"):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.01)
                if (check_input("white") or check_input("orange")):
                    inYellow = False
    
    def move_backward(counter):
        inYellow = True
        left_limiter = 1.05  # Left wheel needs 5% more power to compensate for weight
        right_limiter = 1
        while (True):
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in room_search")
                exit()
            if (counter < 3):
                right_limiter = 0.85
                
            RIGHT_WHEEL.set_power(-CORRECT_POWER * right_limiter)
            LEFT_WHEEL.set_power(-CORRECT_POWER * left_limiter)
            time.sleep(0.01)
            color = get_new_color()
            if (color == "green" and dropped_package == 0):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.1)
                check_input("green")
            elif (color == "orange"):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.01)
                if (check_input("orange")):
                    break

    def main_application_code():
        print("Starting room search - moving forward into office")
        # Move forward deeper into office first
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER * 1.05)
        time.sleep(0.4)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.1)
        
        print("Turning right to start from right side")
        # Turn RIGHT to face right side of office (compensate for left-heavy robot)
        RIGHT_WHEEL.set_power(-20)
        LEFT_WHEEL.set_power(22)  # Left wheel needs more power
        time.sleep(0.25)  # Half the original turn time
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.1)
        
        print("Starting sweep pattern from right to left")
        sweep_count = 0
        
        # Keep sweeping until package is dropped
        while (dropped_package == 0):
            sweep_count = sweep_count + 1
            print(f"Sweep {sweep_count}")
            
            # Move forward until white detected
            move_forward()
            
            # If package dropped during forward, exit
            if (dropped_package == 1):
                return dropped_package
            
            # Move backward until orange detected
            move_backward(sweep_count)
            
            # If package dropped during backward, exit
            if (dropped_package == 1):
                return dropped_package
            
            # Turn LEFT ~15 degrees for next sweep (compensate for weight)
            RIGHT_WHEEL.set_power(21)  # Right wheel needs 5% more power to turn left evenly
            LEFT_WHEEL.set_power(-20)
            time.sleep(0.12)  # Increased from 0.08 for 15 degree turn
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            time.sleep(0.05)
            
            # Safety limit: stop after 12 sweeps to avoid infinite loop
            if (sweep_count >= 12):
                print("Reached maximum sweeps without finding package")
                break

        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.5)
        return dropped_package

    def back_out():
        nonlocal dropped_package
        print("Backing out to find black line")
        
        # Back up straight until we see orange (doorway)
        found_orange = False
        orange_checks = 0
        while not found_orange and orange_checks < 500:
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in back_out")
                exit()
            
            # Back up with weight compensation
            RIGHT_WHEEL.set_power(-25)
            LEFT_WHEEL.set_power(-26)  # 5% more for left-heavy
            time.sleep(0.01)
            
            color = get_new_color()
            if color == "orange":
                found_orange = True
            orange_checks += 1
        
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.2)
        print("Found orange doorway - turning left to find black line")
        
        # Turn left while looking for black line
        black_checks = 0
        found_black = False
        while not found_black and black_checks < 200:
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in back_out")
                exit()
            
            # Turn left with weight compensation
            RIGHT_WHEEL.set_power(-18)
            LEFT_WHEEL.set_power(19)  # 5% compensation
            time.sleep(0.01)
            
            color = get_new_color()
            if color == "black":
                found_black = True
            black_checks += 1
        
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.1)
        
        if found_black:
            print("Found black line - adjusting orientation")
            # Turn a bit more left to align with corridor direction
            for i in range(30):
                if (T_sens.is_pressed()):
                    RIGHT_WHEEL.set_power(0)
                    LEFT_WHEEL.set_power(0)
                    reset_brick()
                    print("emergency stop detected in back_out")
                    exit()
                RIGHT_WHEEL.set_power(-15)
                LEFT_WHEEL.set_power(16)
                time.sleep(0.01)
            
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            time.sleep(0.1)
            print("Aligned with corridor - exiting room_search")
        else:
            print("Could not find black line - exiting anyway")
        
    
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    time.sleep(0.01)
    main_application_code()

    print("Main application finished.")
    return dropped_package
    
