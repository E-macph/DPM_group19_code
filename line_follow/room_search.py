from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor
import brickpi3
import time
import classify
import threading

def room_search():

    RIGHT_WHEEL = Motor("C")
    LEFT_WHEEL = Motor("B")
    POWER_LIMIT = 30
    OFF_POWER = 0
    CORRECT_POWER = 10
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
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.2)
        LEFT_WHEEL.run_for_time(CORRECT_POWER * 0.6, 0.2)
        drop_package()
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER * 0.75, 0.3)
        LEFT_WHEEL.run_for_time(CORRECT_POWER * 0.75, 0.3)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER * 0.75, 0.2)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.75, 0.2)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.2)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.2)

    def continuous_test_function():
        while True:
            time.sleep(0.02)  # Test runs every 1/50 seconds
            color = get_new_color()
            if (color == "orange"):
                package_orientation()
                break

    def main_application_code(): #room search algorithm
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER *0.5, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.1)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.05)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.05)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.05)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.05)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.05)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.05)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.05)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.05)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.05)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.05)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(CORRECT_POWER * 0.5, 0.05)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.05)
        RIGHT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(CORRECT_POWER, 0.1)
        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)

        RIGHT_WHEEL.run_for_time(-CORRECT_POWER, 0.1)
        LEFT_WHEEL.run_for_time(-CORRECT_POWER * 0.5, 0.1)

        color = get_new_color()

        while (color != "black"):
            time.sleep(0.02) #Test runs every 1/50 seconds
            RIGHT_WHEEL.set_power(-CORRECT_POWER * 0.3)
            LEFT_WHEEL.set_power(-CORRECT_POWER)
            color = get_new_color()

        return color

    test_thread = threading.Thread(target=continuous_test_function, daemon=True)
    # daemon=True ensures the thread exits when the main program exits

    # Start the test thread
    test_thread.start()

    # Run the main application code
    main_application_code()

    print("Main application finished.")