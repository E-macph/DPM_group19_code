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
    CORRECT_POWER = 20
    speed = 20
    COLOR_SAMPLING = 0.02
    MOTOR_SAMPLING = 0.05

    C_sens = EV3ColorSensor(1)

    wait_ready_sensors(True)
    RIGHT_WHEEL.reset_encoder()
    LEFT_WHEEL.reset_encoder()

    RIGHT_WHEEL.set_limits(power=POWER_LIMIT)
    LEFT_WHEEL.set_limits(power=POWER_LIMIT)

    ON_LINE_DRIFT = 1

    def get_new_color():
        time.sleep(0.1)
        r, g, b = C_sens.get_rgb()
        intensity = r + g + b
        color = classify.classify_it(r, g, b, intensity)
        return color

    def package_orientation():
        #move foward and right a bit
        #then drop package
        #then back and around package
        time.sleep(0.1)
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER * 0.6)
        time.sleep(0.3)
        drop_package.drop_package()
        time.sleep(0.5)
        RIGHT_WHEEL.set_power(-CORRECT_POWER * 0.75)
        LEFT_WHEEL.set_power(CORRECT_POWER * 0.75)
        time.sleep(0.5)
        RIGHT_WHEEL.set_power(-CORRECT_POWER * 0.75)
        LEFT_WHEEL.set_power(-CORRECT_POWER * 0.75)
        time.sleep(0.5)
        RIGHT_WHEEL.set_power(CORRECT_POWER * 0.5)
        LEFT_WHEEL.set_power(CORRECT_POWER)

    def main_application_code(): #room search algorithm
        counter = 0
        color = get_new_color()
        green_color = False
        if (color == "red"):
            back_out()

        while(color == "orange"):
            sleep(0.5)
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(CORRECT_POWER)
            sleep(0.1)
            RIGHT_WHEEL.set_power(OFF_POWER)
            LEFT_WHEEL.set_power(OFF_POWER)
            color = get_new_color()

        while (color == "yellow" and counter < 7):
            color = get_new_color()
            if (color == "green"):
                green_color = True
            RIGHT_WHEEL.set_power(-CORRECT_POWER *0.5)
            LEFT_WHEEL.set_power(CORRECT_POWER * 0.5)
            sleep(0.75)
            color = get_new_color()
            if (color == "green"):
                green_color = True
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(CORRECT_POWER)
            sleep(0.75)
            color = get_new_color()
            if (color == "green"):
                green_color = True
            RIGHT_WHEEL.set_power(-CORRECT_POWER)
            LEFT_WHEEL.set_power(-CORRECT_POWER)
            sleep(0.75)
            color = get_new_color()
            if (color == "green"):
                green_color = True
            counter += 1

        if (green_color == True):
            package_orientation()
            sleep(0.3)
            
        back_out()

    def back_out():
        first_time = 1
        while (color != "black"):
            if (first_time == 1):    
                time.sleep(0.02) #Test runs every 1/50 seconds
                RIGHT_WHEEL.set_power(-CORRECT_POWER)
                LEFT_WHEEL.set_power(-CORRECT_POWER)
                first_time = 0
        
            time.sleep(0.02)
            RIGHT_WHEEL.set_power(-CORRECT_POWER)
            LEFT_WHEEL.set_power(-CORRECT_POWER*0.3)
            
            time.sleep(0.05)
            color = get_new_color()

        exit

    main_application_code()

    print("Main application finished.")
