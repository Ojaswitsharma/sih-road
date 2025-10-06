# ⚠️ CRITICAL: How to See Speed Reductions in SUMO

## THE PROBLEM

You're probably opening SUMO-GUI **DIRECTLY** instead of running through the **TraCI controller**.

### ❌ WRONG WAY (Speed reductions won't work):
```bash
# This will NOT show speed reductions!
sumo-gui -c mymap.sumocfg
```

### ✅ CORRECT WAY (Speed reductions WILL work):
```bash
# This WILL show speed reductions!
python3 indian_road_simulator.py
# OR
python3 run_simulation.py
# OR
python3 pothole_controller.py
```

## WHY THIS MATTERS

1. **Without TraCI**: Potholes are just visual polygons, no speed control
2. **With TraCI**: Controller monitors vehicles and forces instant speed changes

## HOW TO VERIFY IT'S WORKING

When you run the **CORRECT WAY**, you'll see console output like:

```
Loading pothole data...
Loaded 1573 pothole zones across 1060 lanes
Starting SUMO simulation...

Step 18: Vehicle auto_0 hit pothole_orange at pos 26.6, speed 13.8 -> 3.5 m/s
Step 28: Vehicle auto_0 exited pothole, resuming normal speed
Step 62: Vehicle auto_0 hit pothole_pink at pos 1.2, speed 13.8 -> 6.9 m/s
```

**If you DON'T see these messages, the TraCI controller is NOT running!**

## STEP-BY-STEP VERIFICATION

1. **Close any open SUMO windows**

2. **Delete old files** (to force regeneration):
   ```bash
   rm mymap.net.xml mymap.rou.xml mymap.obstacles.xml
   ```

3. **Run the simulator** (which launches TraCI controller):
   ```bash
   python3 indian_road_simulator.py
   ```

4. **Watch the console** - You MUST see messages like:
   ```
   Step X: Vehicle Y hit pothole_Z at pos..., speed A -> B m/s
   ```

5. **In SUMO GUI**:
   - Find a vehicle approaching a pothole (colored polygon)
   - Right-click → "Show Parameter"
   - Watch speed value drop when vehicle touches pothole

## VISUAL CHECK

In SUMO GUI, enable speed visualization:
1. Click View → Vehicle Visualizations
2. Choose "Speed" or "by speed"
3. Vehicles will change color based on speed
4. You'll SEE them turn blue/green (slow) when hitting red/orange/pink potholes

## STILL NOT WORKING?

Run this diagnostic:

```bash
# Terminal 1: Run controller
python3 pothole_controller.py

# Check if you see:
# - "Loading pothole data..."
# - "Starting SUMO simulation..."
# - "Step X: Vehicle Y hit pothole..."
```

If you don't see "hit pothole" messages, the issue is:
- TraCI not connecting
- Potholes not loaded correctly
- Wrong obstacles.xml file

## COMMON MISTAKES

1. ❌ Opening SUMO directly from file browser
2. ❌ Running `sumo-gui -c mymap.sumocfg` in terminal
3. ❌ Double-clicking mymap.sumocfg
4. ✅ Running `python3 indian_road_simulator.py`
5. ✅ Running `python3 run_simulation.py`

## EMERGENCY FIX

If nothing works, run this complete reset:

```bash
# Clean everything
rm mymap.*.xml

# Regenerate and run
python3 indian_road_simulator.py
```

**Remember: Speed control is done by TraCI controller at runtime, not by XML files!**
