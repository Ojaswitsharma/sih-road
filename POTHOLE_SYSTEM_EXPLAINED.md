# Pothole System - How It Works

## Problem with Previous Approach

**VSS (Variable Speed Signs) Don't Work for Instant Speed Changes:**
- VSS in SUMO sets a **speed limit**, not a forced deceleration
- Vehicles gradually adjust to new speed limits over distance
- Multiple VSS on same lane create conflicts
- Result: Vehicles slow down **before** potholes and stay slow **after** potholes

## New Solution: TraCI Real-Time Control

### Architecture

1. **indian_road_simulator.py** - Setup script
   - Converts OSM to SUMO network
   - Generates potholes on main roads only
   - Creates vehicle trips (120 vehicles: 30 of each type)
   - Launches `pothole_controller.py`

2. **pothole_controller.py** - Real-time controller (NEW!)
   - Uses TraCI API to control SUMO at runtime
   - Monitors all vehicles every simulation step
   - **Instantly reduces speed** when vehicle touches pothole
   - **Instantly restores speed** when vehicle exits pothole

### How Pothole Speed Reduction Works

```
Normal Speed: Vehicle traveling at 20 m/s
                    |
                    v
[Vehicle] -----> [PINK POTHOLE] 
                    |
                    v
Instant Change: Speed = 20 * 0.50 = 10 m/s (50% reduction)
                    |
                    v
[Vehicle slow] ----> [EXIT POTHOLE]
                    |
                    v
Instant Restore: Speed = -1 (resume normal car-following)
```

### Pothole Types

| Color | Speed Reduction | Multiplier | Example |
|-------|----------------|------------|---------|
| **Pink** | 50% | 0.50 | 20 m/s → 10 m/s |
| **Orange** | 75% | 0.25 | 20 m/s → 5 m/s |
| **Red** | 90% | 0.10 | 20 m/s → 2 m/s |

### Detection Zone

- Pothole zone: **3 meters** (±1.5m from center)
- Vehicle is "in pothole" when: `|vehicle_pos - pothole_pos| < 3.0`
- Speed reduction is **immediate** (applied in 1 simulation step = 0.1 second)

## Running the Simulation

### Method 1: Run Complete Setup
```bash
python indian_road_simulator.py
```

This will:
1. Convert OSM → SUMO network
2. Generate potholes on main roads
3. Create 120 vehicle trips
4. Launch SUMO-GUI with pothole controller

### Method 2: Run Controller Separately
If network already exists:
```bash
python pothole_controller.py
```

## Viewing Pothole Effects

1. **SUMO GUI** will open automatically
2. **Right-click** on any vehicle → "Show Parameter"
3. **Watch speed change** when vehicle hits pothole
4. **Console output** shows:
   ```
   Step 1234: Vehicle auto_5 hit pothole_pink pothole at pos 45.3, speed 18.5 -> 9.2 m/s
   Step 1256: Vehicle auto_5 exited pothole, resuming normal speed
   ```

## Technical Details

### Why TraCI?

TraCI (Traffic Control Interface) is the **only way** to:
- Get instant speed changes in SUMO
- Override normal car-following models
- Apply speed changes based on vehicle position

### Speed Control Commands

```python
# Force vehicle to specific speed
traci.vehicle.setSpeed(veh_id, target_speed)

# Restore normal behavior (car-following)
traci.vehicle.setSpeed(veh_id, -1)  # -1 = automatic
```

### Potholes Are Only on Main Roads

- Main road criteria: **2+ lanes OR speed > 16 m/s**
- 4-6 potholes per main road
- Minimum 60m spacing between potholes
- Total: ~1800-2000 potholes

### Vehicle Types

All vehicles use `vClass="passenger"` for routing:
- **Auto-rickshaw** (yellow): Overtakes, medium distance
- **Motorbike** (red): Erratic, frequent lane changes  
- **Car** (cyan): Average behavior, long distance
- **Bus** (blue): Slow, less maneuverable

## Troubleshooting

### Issue: No speed reduction visible
**Solution:** Check console for pothole hit messages. If none, increase vehicle count or pothole density.

### Issue: TraCI import error
**Solution:** Ensure SUMO_HOME is set:
```bash
export SUMO_HOME=/usr/share/sumo
```

### Issue: Vehicles teleporting
**Solution:** Reduce pothole severity (increase speed multipliers) or increase min speed in controller.

### Issue: Too many console messages
**Solution:** Comment out print statements in `pothole_controller.py` lines 92 and 102.

## Files Generated

- `mymap.net.xml` - SUMO network
- `mymap.rou.xml` - Vehicle routes
- `mymap.obstacles.xml` - Pothole polygons + VSS (visual only)
- `mymap.sumocfg` - SUMO configuration
- `mymap.gui.xml` - GUI visualization settings

## Performance

- **109/120 routes** successfully created (91% success rate)
- **~1900 potholes** on main roads
- **Real-time control** at 10 FPS (0.1s time steps)
- **Instant speed changes** (no gradual deceleration)
