# 🚗 Pothole Avoidance Simulation - Quick Start Guide

## ✅ How to Run the Simulation

### **Option 1: Run with the Script (Easiest)**

```bash
./RUN_SIMULATION.sh
```

This will:
- ✓ Launch SUMO with graphical interface
- ✓ Show vehicles avoiding potholes in real-time
- ✓ Display console messages for swerving and hits

### **Option 2: Run Manually**

```bash
python3 pothole_swerve_controller.py --config mymap.sumocfg
```

### **Option 3: Regenerate Everything and Run**

```bash
# Regenerate the entire simulation from scratch
python3 indian_road_simulator.py --regenerate

# Then run it
./RUN_SIMULATION.sh
```

---

## 🎯 What You'll See

### In the SUMO GUI:
- **Pink/Purple polygons** = Potholes on the road
- **Vehicles** = Moving cars, buses, motorbikes, autos
- **Watch for**: Vehicles swerving left/right to avoid potholes!

### In the Console Output:
```
⬇ Step 1090: car_flow_10.0 SLOWING to 8.0 m/s - pothole at 79.1m
↔ Step 1095: car_flow_10.0 SWERVED 5.0m LEFT - avoiding pothole at 68.2m
↩ Step 1175: car_flow_10.0 RETURNED to center
⚠ Step 1129: car_flow_13.0 HIT pothole_deep_purple at 0.3m - FORCED to 0.5 m/s
✓ Step 1179: car_flow_13.0 RECOVERED from pothole
```

### Controls in SUMO GUI:
- **▶️ Play button** - Start simulation
- **⏸️ Pause button** - Pause to observe
- **Speed slider** - Adjust simulation speed (slower = easier to see swerving)
- **🔍 Zoom** - Mouse wheel to zoom in/out

---

## 🧠 How the System Works

### 1. **Detection Phase** (100m ahead)
- Vehicles scan their lane for potholes
- Calculate distance to nearest pothole

### 2. **Slowdown Phase** (80m away)
- Vehicle reduces speed to 8 m/s
- Prepares for avoidance maneuver

### 3. **Swerve Phase** (50-70m away)
- Vehicle moves **5-6 meters laterally** (left or right)
- Uses perpendicular offset from lane centerline
- Stays swerved for 8 seconds

### 4. **Return Phase** (after 8 seconds)
- Vehicle returns to lane center
- Restores normal speed

### 5. **Pothole Hit** (if avoidance fails)
- **INSTANT slowdown to 0.5 m/s** (forced!)
- Vehicle stuck at low speed for 5 seconds
- Then recovers to normal speed

---

## 📊 System Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Detection Distance | 100m | How far ahead vehicles look |
| Slowdown Distance | 80m | When to start slowing down |
| Swerve Distance | 50-70m | When to swerve laterally |
| Swerve Offset | 5-6m | How far to move sideways |
| Pothole Hit Radius | 3m | Distance to trigger "hit" |
| Pothole Speed | 0.5 m/s | Forced speed when hitting |
| Recovery Time | 5 seconds | Stuck in pothole duration |
| Swerve Duration | 8 seconds | Time before returning to center |

---

## 🔧 Troubleshooting

### "Vehicles are ignoring potholes!"
✓ Make sure you're running `pothole_swerve_controller.py` (not the old controller)
✓ Check that potholes are loaded: Look for "✓ Loaded X potholes" message

### "I don't see any swerving!"
✓ Slow down the simulation in SUMO GUI (use the speed slider)
✓ Zoom in to see lateral movement better
✓ Check console for "↔ SWERVED" messages

### "Simulation won't start!"
✓ Make sure SUMO is installed: `which sumo-gui`
✓ Set SUMO_HOME: `export SUMO_HOME=/usr/share/sumo`
✓ Check Python packages: `pip3 install traci sumolib`

---

## 📁 Important Files

- `RUN_SIMULATION.sh` - Main run script
- `pothole_swerve_controller.py` - Swerve avoidance controller
- `indian_road_simulator.py` - Full simulation generator
- `mymap.sumocfg` - SUMO configuration
- `mymap.obstacles.xml` - Pothole locations

---

## 🎨 Customization

### Change Swerve Distance
Edit `pothole_swerve_controller.py`:
```python
SWERVE_OFFSET = 5.0  # Change this value (meters)
```

### Change Detection Distance
```python
DETECTION_DISTANCE = 100.0  # Change this value (meters)
```

### Change Pothole Severity
```python
POTHOLE_SPEED = 0.5  # Lower = more severe slowdown
```

---

## 📈 Expected Behavior

### Success Rate:
- ~60-80% of potholes avoided through swerving
- ~20-40% still result in hits (realistic for dense road conditions)

### Why Some Hits Still Occur:
1. Multiple nearby potholes (can't avoid all)
2. Road width limitations
3. Traffic density (can't swerve if blocked)
4. Realistic behavior (not 100% perfect like real driving)

---

## 🚀 Quick Commands

```bash
# Run simulation
./RUN_SIMULATION.sh

# Regenerate everything
python3 indian_road_simulator.py --regenerate

# Run for specific duration
python3 indian_road_simulator.py --duration 300

# See detailed output
python3 pothole_swerve_controller.py --config mymap.sumocfg 2>&1 | grep -E "(HIT|SWERVED)"
```

---

**Enjoy the simulation! Watch vehicles smartly avoid potholes! 🚗💨**
