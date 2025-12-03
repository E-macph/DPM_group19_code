from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor
import brickpi3
import time
import classify
import drop_package
def room_search():
    RIGHT_WHEEL = Motor("C")
    LEFT_WHEEL = Motor("B")
    
    
    POWER_LIMIT = 30
    OFF_POWER = 0
    CORRECT_POWER = 25
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
            color = get_new_color()
            if (color != input_color):
                green_counter = green_counter -1
            counter= counter +1
            green_counter = green_counter + 1
            time.sleep(0.04)
            
        if (green_counter >= 7):
            if (input_color == "green"):
                package_orientation()
            elif (input_color == "white"):
                print("saw white")
                return True


    def package_orientation():
        #move foward and right a bit
        #then drop package
        #then back and around package
        nonlocal dropped_package
        print("dropping package")
        if (dropped_package == 1):
            return
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.3)
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER)
        time.sleep(0.7)
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        drop_package.drop_package()
        time.sleep(1)
        RIGHT_WHEEL.set_power(-CORRECT_POWER)
        LEFT_WHEEL.set_power(-CORRECT_POWER)
        time.sleep(0.7)
        goout = 1
        dropped_package = 1
        

    def move_forward(move_time):
        nonlocal dropped_package
        for i in range(move_time):
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(CORRECT_POWER)
            time.sleep(0.01)
            color = get_new_color()
            if (color == "green" and dropped_package == 0):
                RIGHT_WHEEL.set_power(0)
                LEFT_WHEEL.set_power(0)
                time.sleep(0.1)
                check_input("green")
            elif (False and color == "white" and check_input("white")):
                print("should break")
                #break
                #package_orientation()
                #break

    def move_backward(move_time):
        for i in range(move_time):
            RIGHT_WHEEL.set_power(-CORRECT_POWER)
            LEFT_WHEEL.set_power(-CORRECT_POWER)
            time.sleep(0.01)

    def main_application_code():
        print("rotating")
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(20)
        time.sleep(0.3)
        RIGHT_WHEEL.set_power(-20)
        LEFT_WHEEL.set_power(20)
        time.sleep(0.35)
        print("done_rotation")
        
        move_forward(50)
        move_backward(100)
        
        print("first iteration")
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.275)

        move_forward(70)
        move_backward(140)
        #if (goout == 1):
            #back_out()

        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.275)

        move_forward(90)
        move_backward(190)
        #if (goout == 1):
            #back_out()

        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.275)

        move_forward(90)
        move_backward(200)
        #f (goout == 1):
            #back_out()

        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.275)

        move_forward(90)
        move_backward(190)
        #if (goout ==1):
            #back_out()

        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.275)

        move_forward(85)
        move_backward(150)
        #if (goout == 1):
            #back_outset_power
        
        RIGHT_WHEEL.set_power(20)
        LEFT_WHEEL.set_power(-20)
        time.sleep(0.275)
        
        move_forward(75)
        move_backward(140)
        #if (goout == 1):
            #back_out()

        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(0.5)
        back_out()

    def back_out():
        color = get_new_color()
        RIGHT_WHEEL.set_power(-15)
        LEFT_WHEEL.set_power(-15)
        time.sleep(2)
        while (color != "black"):
            print(color)
            RIGHT_WHEEL.set_power(-20)
            LEFT_WHEEL.set_power(20)
            color = get_new_color()
            time.sleep(0.01)
        
        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        goout = 0
        return dropped_package
        exit

    main_application_code()

    print("Main application finished.")
    

