#!/usr/bin/python3
"""
Test file to demonstrate package drop and backout motion
Run this standalone to see the robot movements without being on the track
"""
from utils.brick import Motor, reset_brick, wait_ready_sensors, TouchSensor
import time

# Initialize motors and sensors
RIGHT_WHEEL = Motor("C")
LEFT_WHEEL = Motor("B")
T_sens = TouchSensor(2)

wait_ready_sensors(True)

RIGHT_WHEEL.reset_encoder()
LEFT_WHEEL.reset_encoder()
RIGHT_WHEEL.set_limits(30)
LEFT_WHEEL.set_limits(30)

CORRECT_POWER = 30

print("="*50)
print("BACKOUT MOTION TEST")
print("="*50)
print("\nThis will simulate:")
print("1. Moving forward (simulating approach to package)")
print("2. Stopping and waiting (simulating package drop)")
print("3. Backing up straight (finding doorway)")
print("4. Turning left (finding black line)")
print("\nPress touch sensor at any time to stop")
print("\nStarting in 3 seconds...")
time.sleep(3)

try:
    # Step 1: Move forward (simulating sweep into office)
    print("\n[1] Moving forward to 'package location'...")
    for i in range(70):
        if T_sens.is_pressed():
            raise KeyboardInterrupt
        RIGHT_WHEEL.set_power(CORRECT_POWER)
        LEFT_WHEEL.set_power(CORRECT_POWER * 1.05)  # Weight compensation
        time.sleep(0.01)
    
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    time.sleep(0.5)
    
    # Step 2: Simulate package drop
    print("[2] 'Dropping package' (pausing for 2 seconds)...")
    time.sleep(2)
    print("    Package dropped!")
    time.sleep(0.5)
    
    # Step 3: Back up straight
    print("[3] Backing up straight to 'doorway' (3 seconds)...")
    for i in range(300):
        if T_sens.is_pressed():
            raise KeyboardInterrupt
        RIGHT_WHEEL.set_power(-25)
        LEFT_WHEEL.set_power(-26)  # Weight compensation
        time.sleep(0.01)
    
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    time.sleep(0.5)
    print("    Reached 'orange doorway'")
    
    # Step 4: Turn left to find black line
    print("[4] Turning left to find 'black line' (2 seconds)...")
    for i in range(200):
        if T_sens.is_pressed():
            raise KeyboardInterrupt
        RIGHT_WHEEL.set_power(-18)
        LEFT_WHEEL.set_power(19)  # Weight compensation
        time.sleep(0.01)
    
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    time.sleep(0.5)
    print("    Found 'black line'")
    
    print("\n" + "="*50)
    print("BACKOUT TEST COMPLETE!")
    print("="*50)
    print("\nRobot should now be:")
    print("- Out of the 'office'")
    print("- Turned to face the 'corridor'")
    print("- Ready to resume line following")
    
except KeyboardInterrupt:
    print("\n\nEmergency stop detected!")
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    reset_brick()
    print("Motors stopped and brick reset")

except Exception as e:
    print(f"\n\nError occurred: {e}")
    RIGHT_WHEEL.set_power(0)
    LEFT_WHEEL.set_power(0)
    reset_brick()
    print("Motors stopped and brick reset")
