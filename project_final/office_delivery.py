from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, TouchSensor
import time
import color_classifier
import package_dropper
from utils.sound import Sound

NOTE_DROPPED = Sound(duration=0.5, pitch="D", volume=100)

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
        color = color_classifier.classify_it(r, g, b, intensity)
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
        LEFT_WHEEL.set_power(CORRECT_POWER)
        time.sleep(0.7)
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected in package_orientation")
            exit()
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        package_dropper.drop_package()
        NOTE_DROPPED.play()
        NOTE_DROPPED.wait_done()
        goout = 1
        dropped_package = 1
        
        
    def move_forward():
        nonlocal dropped_package
        inYellow = True;
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER)
        time.sleep(0.3)
        while(inYellow):
            if (T_sens.is_pressed()):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                reset_brick()
                print("emergency stop detected in room_search")
                exit()
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(CORRECT_POWER)
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
        left_limiter = 1
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
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected at start of main_application_code")
            exit()
        print("rotating")
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(20)
        time.sleep(0.3)
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected during rotation")
            exit()
        RIGHT_WHEEL.set_power(-20)
        LEFT_WHEEL.set_power(20)
        time.sleep(0.35)
        print("done_rotation")
        counter = 1
        move_forward()
        move_backward(counter)
        
        print("first iteration")
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.1)
        counter = counter + 1
        
        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package

        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.03)
        counter = counter + 1

        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package

        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.12)
        counter = counter + 1

        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package

        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.175)
        counter = counter + 1

        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package

        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.175)
        counter = counter + 1

        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package
        
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.175)
        counter = counter + 1
        
        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package
        
        if (T_sens.is_pressed()):
            RIGHT_WHEEL.set_power(0)
            LEFT_WHEEL.set_power(0)
            reset_brick()
            print("emergency stop detected before sweep turn")
            exit()
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.175)
        counter = counter + 1

        move_forward()
        move_backward(counter)
        if (dropped_package == 1):
            return dropped_package

        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.5)
        return dropped_package

#     def back_out():
#         nonlocal dropped_package
#         color = get_new_color()
#         while (color != "black"):
#             print(color)
#             RIGHT_WHEEL.set_power(-15)
#             LEFT_WHEEL.set_power(15)
#             color = get_new_color()
#             time.sleep(0.01)
#         
#         RIGHT_WHEEL.set_power(0)
#         LEFT_WHEEL.set_power(0)
#         goout = 0
#         raise NameError
        
    
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    time.sleep(0.01)
    main_application_code()

    print("Main application finished.")
    return dropped_package
    
