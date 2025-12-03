from utils.brick import Motor
from utils.brick import TouchSensor, wait_ready_sensors, reset_brick
import time

package_drop_motor = Motor("A")
T_sens = TouchSensor(2)

package_drop_motor.set_limits(power=70, dps=270)

def drop_package():
    if (T_sens.is_pressed()):
        reset_brick()
        print("emergency stop detected during package drop")
        exit()
    package_drop_motor.set_position_relative(55)
    time.sleep(2)
    if (T_sens.is_pressed()):
        reset_brick()
        print("emergency stop detected during package drop")
        exit()
    package_drop_motor.set_position_relative(-55)
    time.sleep(0.5)