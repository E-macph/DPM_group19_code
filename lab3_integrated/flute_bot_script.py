#!/usr/bin/env python3
"""
ECSE211 Lab 3 - Corrected Initialization Order
"""

# ==============================================================================
# 1. IMPORTS
# ==============================================================================
import time
from utils import sound
from utils.brick import EV3UltrasonicSensor, TouchSensor, Motor, wait_ready_sensors, reset_brick
from utils.sound import Sound

# ==============================================================================
# 2. HARDWARE CONFIGURATION
# ==============================================================================
ULTRASONIC_PORT = 2
DRUM_TOGGLE_PORT = 3
EMERGENCY_STOP_PORT = 4
DRUM_MOTOR_PORT = "A"
DRUM_POWER = 70
BEAT_INTERVAL = 0.5

# ==============================================================================
# 3. INITIALIZATION - **NEW, CORRECT ORDER**
# ==============================================================================

# --- STEP A: Initialize HARDWARE objects first ---
# This "wakes up" the BrickPi hardware interface.
print("Initializing hardware objects...")
us_sensor = EV3UltrasonicSensor(ULTRASONIC_PORT)
drum_toggle_button = TouchSensor(DRUM_TOGGLE_PORT)
emergency_stop_button = TouchSensor(EMERGENCY_STOP_PORT)
drum_motor = Motor(DRUM_MOTOR_PORT)
print("Hardware objects created.")

# --- STEP B: NOW that hardware is awake, initialize SOUND objects ---
print("Initializing sound objects...")
try:
    NOTE_C = sound.Sound(duration=0.5, pitch="A3", volume=95)
    NOTE_D = sound.Sound(duration=0.5, pitch="B4", volume=95)
    NOTE_E = sound.Sound(duration=0.5, pitch="C3", volume=95)
    NOTE_F = sound.Sound(duration=0.5, pitch="D4", volume=95)

    print("Sound objects initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Failed to create sound objects. The error was: {e}")
    exit()

# --- STEP C: Finally, wait for all sensors to be ready ---
print("Waiting for sensors to be ready...")
wait_ready_sensors(True)
print("Hardware ready. Starting main loop.")


# ==============================================================================
# 4. MAIN PROGRAM LOGIC (Unchanged)
# ==============================================================================
drumming_active = False
last_button_state = False
last_beat_time = 0
current_note_object = None

try:
    while True:
        # --- The main loop logic is the same as before ---
        distance_cm = us_sensor.get_cm()
        drum_toggle_pressed = drum_toggle_button.is_pressed()
        emergency_stop_pressed = emergency_stop_button.is_pressed()

        if emergency_stop_pressed:
            print("EMERGENCY STOP")
            break

        if drum_toggle_pressed and not last_button_state:
            drumming_active = not drumming_active
            print(f"Drumming {'ON' if drumming_active else 'OFF'}")
            if not drumming_active: drum_motor.set_power(0)
        last_button_state = drum_toggle_pressed

        if drumming_active and time.time() - last_beat_time > BEAT_INTERVAL:
            drum_motor.set_power(DRUM_POWER); time.sleep(0.08)
            drum_motor.set_power(-DRUM_POWER); time.sleep(0.08)
            drum_motor.set_power(0)
            last_beat_time = time.time()

        
        if distance_cm < 20:
            if 0 < distance_cm < 5:
                NOTE_C.play()
                print("playing C")
            elif 5 <= distance_cm < 10:
                NOTE_D.play()
                print("playing D")
            elif 10 <= distance_cm < 15:
                NOTE_E.play()
                print("playing E")
            elif 15 <= distance_cm < 20:
                NOTE_F.play()
                print("playing F")
            
            time.sleep(0.4)


       
finally:
    print("Cleaning up and resetting hardware...")
    reset_brick()
    print("Program terminated.")