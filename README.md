# DPM Group 19 - Smart Courier Robot

**ECSE 211 Design Principles and Methods - Fall 2025**

## Project Overview

Autonomous mail delivery robot that navigates building corridors, identifies delivery zones using color recognition, delivers packages to offices with recipients present, avoids restricted areas, and returns to the mail room upon mission completion.

---

## 🚀 Running the Robot

**Main Entry Point:** `project_final/line_follower.py`

Run this file on the robot to start the courier mission.

---

## 📁 Directory Structure

### **`project_final/`** - Production Code
Contains the final, working code for the Smart Courier Robot.

- **`line_follower.py`** - Main entry point. Controls line-following with gyro-assisted turns, ultrasonic-based speed switching, and orange doorway detection.
- **`color_classifier.py`** - RGB sensor data → color name classification using Euclidean distance.
- **`office_delivery.py`** - Office entry routine. Searches for green recipient sticker, drops package if found, handles red restricted-room detection.
- **`package_dropper.py`** - Physical package drop mechanism using motor A.
- **`return_to_mailroom.py`** - Detects blue mail room tile and plays mission-complete sound.
- **`utils/`** - Hardware abstraction layer (motors, sensors, sound playback).

---

### **`archive/`** - Historical Development Versions
Old code versions preserved for reference. **Do not use for the robot.**

- **`line_follow_prefinal/`** - Pre-final version without emergency stops in all functions.
- **`line_follow_mias_experimental/`** - Experimental branch used for parallel development and testing different fixes.
- **`Final_code_obsolete/`** - Early obsolete implementation.

---

### **Lab Code** (Reference Only)
- **`lab_2/`** - Lab 2 starter code and submissions.
- **`lab3_flute/`** - Lab 3: Ultrasonic-based flute simulator.
- **`lab3_integrated/`** - Lab 3: Drum + flute integrated multithreaded system.
- **`lab3_motor/`** - Lab 3: Motor testing scripts.

---

## 🎯 Mission Specifications

### **Environment:**
- 1.2m × 1.2m grid with black line paths
- Color-coded zones:
  - **Yellow tiles** = Offices (potential delivery zones)
  - **Blue tile** = Mail room (mission end)
  - **Orange strips** = Doorways (24cm width)
  - **Green stickers** = Package recipients (2.5cm × 2.5cm)
  - **Red stickers** = Restricted areas (meetings in progress)

### **Robot Behavior:**
1. Start at bottom-left corner
2. Follow black line with gyro-assisted corner turns
3. Detect orange doorways → check tile color
4. **Yellow + Green sticker** → Enter office, drop package, play delivery sound
5. **Yellow + Red sticker** → Back up, avoid office, continue route
6. **Blue tile** (after 2 deliveries) → Play mission-complete sound, terminate
7. Emergency stop via touch sensor (port 2) at any time

### **Hardware:**
- **Motors:** Port B (left wheel), Port C (right wheel), Port A (package dropper)
- **Sensors:**
  - Port 1: EV3 Color Sensor
  - Port 2: Touch Sensor (emergency stop)
  - Port 3: EV3 Ultrasonic Sensor (distance-based speed control)
  - Port 4: EV3 Gyro Sensor (corner detection & heading tracking)

---

## 🛠️ Key Features

- **Gyro-Assisted Navigation:** Detects 90° corner turns and resets heading baseline to prevent drift.
- **Adaptive Speed Control:** Fast mode in long corridors (ultrasonic range 48-89cm, gyro angle ±25°), slow mode near walls/turns.
- **Emergency Stop:** Touch sensor immediately halts all motors and exits program safely.
- **Package Tracking:** Counts successful deliveries, only enters offices before 2 packages delivered.
- **Sound Feedback:** Plays delivery confirmation tone at each drop-off, mission-complete tone at mail room.

---

## 📋 Development Notes

- All Vim swap files (`.swp`, `.swo`, `.swn`) and Python cache (`__pycache__/`) are gitignored.
- The gyro sensor requires manual offset tracking—`BASELINE_ANGLE` is adjusted after each corner turn since the BrickPi3 doesn't natively zero the EV3 gyro.
- Color classification thresholds are tuned for the specific lighting conditions of the test environment.

---

## 👥 Team

**Group 19** - McGill Smart Logistics  
ECSE 211 - Fall 2025
