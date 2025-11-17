from utils.brick import Motor
from utils.brick import TouchSensor, wait_ready_sensors
import time

package_drop_motor = Motor("A")

package_drop_motor.set_limits(power=70, dps=270)

def drop_package():
    package_drop_motor.set_position_relative(45)
    time.sleep(0.5)
    package_drop_motor.set_position_relative(-45)
    time.sleep(0.5)


