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

    def get_new_color():
        time.sleep(0.01)
        r, g, b = C_sens.get_rgb()
        intensity = r + g + b
        color = classify.classify_it(r, g, b, intensity)
        return color

    def package_orientation():
        #move foward and right a bit
        #then drop package
        #then back and around package
        print("dropping package")
        time.sleep(0.1)
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER * 0.6)
        time.sleep(0.35)
        RIGHT_WHEEL.set_power(OFF_POWER)
        LEFT_WHEEL.set_power(OFF_POWER)
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

    def move_forward(time):
        for i in range(time):
            RIGHT_WHEEL.set_power(CORRECT_POWER)
            LEFT_WHEEL.set_power(CORRECT_POWER)
            time.sleep(0.01)
            color = get_new_color()
            if (color == "green"):
                package_orientation()
                break

    def move_backward(time):
        for i in range(time):
            RIGHT_WHEEL.set_power(-CORRECT_POWER)
            LEFT_WHEEL.set_power(-CORRECT_POWER)
            time.sleep(0.01)

    def main_application_code():
        RIGHT_WHEEL.set_position_relative(-70)
        LEFT_WHEEL.set_position_relative(70)

        move_forward(40)
        move_backward(40)

        RIGHT_WHEEL.set_position_relative(10)
        LEFT_WHEEL.set_position_relative(-10)

        move_forward(50)
        move_backward(50)

        RIGHT_WHEEL.set_position_relative(10)
        LEFT_WHEEL.set_position_relative(-10)

        move_forward(70)
        move_backward(70)

        RIGHT_WHEEL.set_position_relative(10)
        LEFT_WHEEL.set_position_relative(-10)

        move_forward(60)
        move_backward(60)

        RIGHT_WHEEL.set_position_relative(10)
        LEFT_WHEEL.set_position_relative(-10)

        move_forward(70)
        move_backward(70)

        RIGHT_WHEEL.set_position_relative(10)
        LEFT_WHEEL.set_position_relative(-10)

        move_forward(50)
        move_backward(50)

        RIGHT_WHEEL.set_position_relative(10)
        LEFT_WHEEL.set_position_relative(-10)

        move_forward(40)
        move_backward(40)

        RIGHT_WHEEL.set_power(0)
        LEFT_WHEEL.set_power(0)
        time.sleep(5)

        def back_out():
            first_time = 1
            while (color != "black"):
                if (first_time == 1):
                    RIGHT_WHEEL.set_power(CORRECT_POWER)
                    LEFT_WHEEL.set_power(-CORRECT_POWER)
                    time.sleep(0.3)
                    RIGHT_WHEEL.set_power(-CORRECT_POWER)
                    LEFT_WHEEL.set_power(-CORRECT_POWER)
                    first_time = 0
                    time.sleep(0.7)

                time.sleep(0.01)
                RIGHT_WHEEL.set_power(-CORRECT_POWER)
                LEFT_WHEEL.set_power(-CORRECT_POWER * 0.4)
                color = get_new_color()
            exit


    main_application_code()

    print("Main application finished.")