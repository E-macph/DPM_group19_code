#!/usr/bin/python3
#from utils import brick
from utils.brick import Motor, reset_brick, wait_ready_sensors, EV3ColorSensor, EV3UltrasonicSensor, TouchSensor, EV3GyroSensor
import brickpi3
import time
import classify
import room_search
import room_search_1
import mailroom
import mailroom2

RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")

QUICK_POWER = 35
CAREFUL_POWER = 22
Quick_SLOW_WHEEL = QUICK_POWER*(0.65)
Careful_SLOW_WHEEL = CAREFUL_POWER*(-0.4)

CORRECT_POWER = 0
CAREFUL_SAMPLING = 0.02
QUICK_SAMPLING = 0.05

C_sens = EV3ColorSensor(1)
T_sens = TouchSensor(2)
U_sens = EV3UltrasonicSensor(3)
G_sens = EV3GyroSensor(4)
BASELINE_ANGLE = 0


wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()

ON_LINE_DRIFT = 1                      # 1 for to the right, 0 for to the left
package_counter = 0
ANGLE_COUNTER = 0

mailroom2.mailroom2()