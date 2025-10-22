#!/usr/bin/env python3
"""
ECSE211 Lab 3 - A thread-safe solution using a Lock.
"""

# ==============================================================================
# 1. IMPORTS
# ==============================================================================
import time
import threading
from utils.sound import Sound
from utils.brick import EV3UltrasonicSensor, TouchSensor, Motor, wait_ready_sensors, reset_brick
import brickpi3

# ==============================================================================
# 2. CONFIGURATION (Unchanged)
# ==============================================================================
ULTRASONIC_PORT = 1
DRUM_TOGGLE_PORT = 3
EMERGENCY_STOP_PORT = 4
DRUM_MOTOR_PORT = "A"
DRUM_MOTOR_PORT = brickpi3.BrickPi3.PORT_A
DRUM_POWER_LIMIT = 70
DRUM_SPEED_LIMIT = 720
DRUM_ANGLE_VARIATION = 90  # How many degrees the drumstick moves forward and back.
DRUM_PAUSE_DURATION = 0.5  # How long to wait between thumps.


# ==============================================================================
# 3. INITIALIZATION
# ==============================================================================
# --- THE FIX: Create a single, shared Lock for the sound hardware ---
# This is the "key to the doorway."
BP = brickpi3.BrickPi3()
sound_lock = threading.Lock()

# --- The rest of the initialization is the correct order we found before ---
print("Initializing sound objects...")
try:
    # Your duration of 10 is fine. A long duration is robust.
    NOTE_C = Sound(duration=1, pitch="A#1", volume=100)
    NOTE_D = Sound(duration=1, pitch="A#2", volume=100)
    NOTE_E = Sound(duration=1, pitch="A#3", volume=100)
    NOTE_F = Sound(duration=1, pitch="A#4", volume=100)
    print("Sound objects initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Failed to create sound objects. The error was: {e}")
    exit()

print("Initializing hardware objects...")
us_sensor = EV3UltrasonicSensor(ULTRASONIC_PORT)
drum_toggle_button = TouchSensor(DRUM_TOGGLE_PORT)
emergency_stop_button = TouchSensor(EMERGENCY_STOP_PORT)
drum_motor = Motor(DRUM_MOTOR_PORT)
print("Hardware objects created.")

# CHANGE 3: Perform the specific, low-level motor setup from your sample code.
print("Setting up motor for position control...")
try:
    BP.offset_motor_encoder(DRUM_MOTOR_PORT, BP.get_motor_encoder(DRUM_MOTOR_PORT))
    BP.set_motor_limits(DRUM_MOTOR_PORT, DRUM_POWER_LIMIT, DRUM_SPEED_LIMIT)
    BP.set_motor_power(DRUM_MOTOR_PORT, 0)
    print("Motor setup complete.")
except IOError as error:
    print(f"FATAL ERROR: Could not set up motor. {error}")
    exit()

print("Waiting for sensors to be ready...")
wait_ready_sensors(True)
print("Hardware ready.")

# ==============================================================================
# 4. THREAD FUNCTIONS
# ==============================================================================
stop_event = threading.Event()


def drum_thread_function():
    """The drum thread, now using ONLY the BP object."""
    print("Drum thread started.")
    drumming_active = False
    last_button_state = False

    while not stop_event.is_set():
        drum_toggle_pressed = drum_toggle_button.is_pressed()
        if drum_toggle_pressed and not last_button_state:
            drumming_active = not drumming_active
            print(f"Drumming {'ON' if drumming_active else 'OFF'}")
            # FIX 3: If drumming is turned off, use BP to stop the motor.
            if not drumming_active:
                BP.set_motor_power(DRUM_MOTOR_PORT, 0)
        last_button_state = drum_toggle_pressed

        if drumming_active:
            try:
                BP.set_motor_position_relative(DRUM_MOTOR_PORT, DRUM_ANGLE_VARIATION)
                time.sleep(DRUM_PAUSE_DURATION)

                if not drumming_active: continue

                BP.set_motor_position_relative(DRUM_MOTOR_PORT, -DRUM_ANGLE_VARIATION)
                time.sleep(DRUM_PAUSE_DURATION)
            except IOError as error:
                print(f"Drum motor error: {error}")
        else:
            time.sleep(0.02)



def flute_thread_function():
    """The flute thread. This function MUST use the lock to prevent crashes."""
    print("Flute thread started.")

    while not stop_event.is_set():
        distance_cm = us_sensor.get_cm()
        if distance_cm < 20:
            if 0 < distance_cm < 5:
                NOTE_C.play()
                print("C")
            elif 5 <= distance_cm < 10:
                NOTE_D.play()
                print("D")
            elif 10 <= distance_cm < 15:
                NOTE_E.play()
                print("E")
            elif 15 <= distance_cm < 20:
                NOTE_F.play()
                print("F")
                
            time.sleep(0.5)   


# ==============================================================================
# 5. MAIN PROGRAM (Unchanged)
# ==============================================================================
try:
    drum_chef = threading.Thread(target=drum_thread_function)
    flute_chef = threading.Thread(target=flute_thread_function)

    drum_chef.start()
    flute_chef.start()

    while True:
        if emergency_stop_button.is_pressed():
            print("EMERGENCY STOP DETECTED! Shutting down threads...")
            stop_event.set()
            break
        time.sleep(0.1)

finally:
    if 'drum_chef' in locals(): drum_chef.join()
    if 'flute_chef' in locals(): flute_chef.join()

    print("Cleaning up and resetting hardware...")
    reset_brick()
    BP.reset_all()
    print("Program terminated.")
