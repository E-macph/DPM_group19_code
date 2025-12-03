import time
import math
import brickpi3
from test_line import get_new_color

BP = brickpi3.BrickPi3()

LEFT_MOTOR = BP.PORT_B
RIGHT_MOTOR = BP.PORT_C
COLOR_PORT = BP.PORT_1

BP.set_sensor_type(COLOR_PORT, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

def sweep_search():
    max_forward = 18  # cm
    angle_step = 15
    sweeps = int(180 / angle_step)
    for i in range(sweeps + 1):
        found = drive_forward_monitor(max_forward)
        if found:
            print("GREEN DETECTED during forward drive!")
            return True

        # Reverse to start (no need to poll here)
        drive_cm(-max_forward)
        # Rotate for next sweep
        rotate_deg(angle_step)

    print("No green detected after full sweep.")
    return False

def drive_forward_monitor(target_cm, speed=150):
    CM_PER_DEG = (math.pi * WHEEL_DIAM) / 360.0

    target_deg = target_cm / CM_PER_DEG

    # Reset encoders to measure progress
    BP.set_motor_position(LEFT_MOTOR, 0)
    BP.set_motor_position(RIGHT_MOTOR, 0)

    BP.set_motor_dps(LEFT_MOTOR, speed)
    BP.set_motor_dps(RIGHT_MOTOR, speed)

    while True:
        try:
            # Poll sensor at high frequency
            if saw_green():
                BP.set_motor_power(LEFT_MOTOR, 0)
                BP.set_motor_power(RIGHT_MOTOR, 0)
                return True

                # Check motor encoder distance
            left_deg = BP.get_motor_encoder(LEFT_MOTOR)
            right_deg = BP.get_motor_encoder(RIGHT_MOTOR)
            avg = (left_deg + right_deg) / 2

            if avg >= target_deg:
                BP.set_motor_power(LEFT_MOTOR, 0)
                BP.set_motor_power(RIGHT_MOTOR, 0)
                return False

        except brickpi3.SensorError:
            pass

        time.sleep(0.01)  # 100 polls/sec


def drive_cm(distance_cm, speed=200):
    WHEEL_DIAM = 5.6
    CM_PER_DEG = (math.pi * WHEEL_DIAM) / 360.0

    target_deg = distance_cm / CM_PER_DEG

    BP.set_motor_position_relative(LEFT_MOTOR, int(target_deg))
    BP.set_motor_position_relative(RIGHT_MOTOR, int(target_deg))
    time.sleep(abs(distance_cm) / 8)


def rotate_deg(angle_deg, speed=150):
    WHEELBASE = 12.0
    WHEEL_DIAM = 5.6
    CM_PER_DEG_WHEEL = (math.pi * WHEEL_DIAM) / 360.0

    arc_len = math.pi * WHEELBASE * (angle_deg / 360.0)
    wheel_deg = arc_len / CM_PER_DEG_WHEEL

    BP.set_motor_position_relative(LEFT_MOTOR, int(wheel_deg))
    BP.set_motor_position_relative(RIGHT_MOTOR, int(-wheel_deg))
    time.sleep(abs(angle_deg) / 60)  # tune depending on speed

def saw_green():
    color = get_new_color()
    if color == "green":
        return True
    else:
        return False


def reset_encoders():
    BP.set_motor_position(LEFT_MOTOR, 0)
    BP.set_motor_position(RIGHT_MOTOR, 0)

try:
    reset_encoders()
    sweep_search()

except:
    BP.reset_all()
