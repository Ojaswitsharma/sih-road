#!/usr/bin/env python3
"""
INDIAN ROAD SIMULATION - INSTANT POTHOLE SPEED REDUCTION
========================================================

This simulation now works PERFECTLY with instant speed changes at potholes!

HOW TO RUN:
-----------
    python3 run_simulation.py

WHAT IT DOES:
-------------
✅ Vehicles travel at NORMAL SPEED until touching pothole
✅ Speed drops INSTANTLY when vehicle enters pothole (3m zone)
✅ Speed restores INSTANTLY when vehicle exits pothole
✅ Console shows real-time speed changes

POTHOLE TYPES:
--------------
🟣 PINK:   50% speed reduction (e.g., 20 m/s → 10 m/s)
🟠 ORANGE: 75% speed reduction (e.g., 20 m/s → 5 m/s)
🔴 RED:    90% speed reduction (e.g., 20 m/s → 2 m/s)

VERIFIED WORKING:
-----------------
Step 18: Vehicle auto_0 hit pothole_orange at pos 26.6, speed 13.8 -> 3.5 m/s ✓
Step 28: Vehicle auto_0 exited pothole, resuming normal speed ✓
Step 62: Vehicle auto_0 hit pothole_pink at pos 1.2, speed 13.8 -> 6.9 m/s ✓
Step 71: Vehicle auto_0 exited pothole, resuming normal speed ✓

WHAT WAS FIXED:
---------------
❌ OLD PROBLEM: VSS (Variable Speed Signs) caused vehicles to slow BEFORE potholes
✅ NEW SOLUTION: Removed VSS, using TraCI for direct real-time speed control

STATISTICS:
-----------
• 1573 potholes on main roads only
• 109 vehicles (30 auto, 30 motorbike, 30 car, 19 bus)
• 10 Hz control frequency (0.1s updates)
• Instant speed changes (no lag)

OBSERVATION TIPS:
-----------------
1. Run: python3 run_simulation.py
2. In SUMO GUI: Right-click vehicle → "Show Parameter" → Watch speed
3. In Console: See "Vehicle X hit pothole, speed A -> B m/s"
4. Potholes are colored irregular polygons on roads

FILES:
------
• indian_road_simulator.py  - Setup (network, potholes, vehicles)
• pothole_controller.py     - Real-time speed controller
• run_simulation.py         - This launcher
• FINAL_SOLUTION.md         - Complete documentation

ENJOY THE SIMULATION! 🚗💨
"""

import subprocess
import os

if __name__ == "__main__":
    print(__doc__)
    
    # Check if network exists
    if not os.path.exists("mymap.net.xml"):
        print("\n⏳ First time setup - generating network and potholes...")
        subprocess.run(["python3", "indian_road_simulator.py"])
    else:
        print("\n▶️  Network exists, launching simulation with pothole controller...")
        subprocess.run(["python3", "pothole_controller.py"])
