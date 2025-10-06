# Indian Road Traffic Simulation with Potholes

## 📋 Overview

A realistic SUMO-based traffic simulation for Indian roads featuring:
- **4 vehicle types** with distinct Indian driving behaviors
- **Deep purple potholes** causing instant 99% speed reduction
- **5-second recovery time** before vehicles return to normal speed
- **Real-time TraCI control** for accurate speed management

## 🚗 Vehicle Types

| Vehicle | Speed | Behavior |
|---------|-------|----------|
| **Auto** | ~14 m/s | Overtakes at medium distance, aggressive in traffic |
| **Motorbike** | ~28 m/s | Erratic speed/lane changes, short following distance |
| **Car** | ~33 m/s | Average behavior, long-distance travel |
| **Bus** | ~22 m/s | Slow, careful, long-distance routes |

## 🕳️ Pothole Behavior

### Speed Reduction Mechanism
1. **Instant Drop**: Vehicle speed drops to **1% of original speed** the moment it hits a pothole
2. **Hold Duration**: Speed stays at 1% for exactly **5 seconds (50 simulation steps)**
3. **Recovery**: After 5 seconds, vehicle accelerates back to normal speed

### Examples
- Bus at 22 m/s hits pothole → **instantly drops to 0.22 m/s** → holds 5 seconds → accelerates back to 22 m/s
- Car at 33 m/s hits pothole → **instantly drops to 0.33 m/s** → holds 5 seconds → accelerates back to 33 m/s
- Motorbike at 28 m/s hits pothole → **instantly drops to 0.28 m/s** → holds 5 seconds → accelerates back to 28 m/s

### Visual Appearance
- **Color**: Deep Purple (RGB: 0.5, 0, 0.5)
- **Shape**: Perfect circles (12-point polygons)
- **Size**: 0.8-1.5 meter diameter
- **Distribution**: Placed on all main roads across the network

## 📁 Project Structure

```
sih-road/
├── indian_road_simulator.py    # Main setup script - generates network & potholes
├── pothole_controller.py        # TraCI controller - manages vehicle speeds
├── run_simulation.py            # Launcher script - starts everything
├── mymap.osm                    # OpenStreetMap data (Delhi road network)
├── mymap.net.xml                # SUMO network file
├── mymap.poly.xml               # Polygon definitions (background)
├── mymap.obstacles.xml          # Pothole visual polygons
├── mymap.rou.xml                # Vehicle routes and flows
├── mymap.sumocfg               # SUMO configuration
├── mymap.vtypes.xml            # Vehicle type definitions
└── README.md                    # This documentation
```

## 🚀 Quick Start

### Prerequisites
- **SUMO** (Simulation of Urban Mobility) - Install from: https://sumo.dlr.de/docs/Installing/index.html
- **Python 3.x** with TraCI library (included with SUMO)
- **SUMO_HOME** environment variable set

### Installation

1. **Check SUMO installation**:
   ```bash
   echo $SUMO_HOME
   # Should output: /usr/share/sumo (or your SUMO installation path)
   ```

2. **Verify Python TraCI**:
   ```bash
   python3 -c "import traci; print('TraCI OK')"
   ```

### Running the Simulation

#### Step 1: Generate Simulation Files (if needed)
```bash
python3 indian_road_simulator.py
```
This creates:
- Network files from OSM data
- ~1500+ deep purple potholes on main roads
- Continuous vehicle flows (~90 vehicles/hour for 2 hours)

#### Step 2: Run the Simulation
```bash
python3 run_simulation.py
```
Or directly:
```bash
python3 pothole_controller.py
```

The SUMO GUI will open showing:
- Traffic moving through Delhi road network
- Deep purple circular potholes
- Vehicles instantly slowing down when hitting potholes
- Console output showing each pothole interaction

### Console Output Example
```
Step 730: Vehicle motorbike_flow_6.0 hit pothole_deep_purple at pos 42.5, INSTANT drop 22.4 -> 0.5 m/s (99% reduction, holding 5 seconds)
Step 780: Vehicle motorbike_flow_6.0 recovered from pothole, resuming normal speed
Step 925: Vehicle car_flow_10.0 hit pothole_deep_purple at pos 19.8, INSTANT drop 28.1 -> 0.5 m/s (99% reduction, holding 5 seconds)
Step 975: Vehicle car_flow_10.0 recovered from pothole, resuming normal speed
```

## 🎨 Visualization Tips

### See Speed Changes in SUMO-GUI
1. **Color by Speed**:
   - Go to: `View` → `Vehicles` → `Color vehicles by: speed`
   - Fast vehicles = Red/Yellow
   - Slow vehicles (in potholes) = Blue/Green

2. **Show Vehicle Names**:
   - Go to: `View` → `Vehicles` → `Show vehicle name`

3. **Adjust Simulation Speed**:
   - Use delay slider in GUI (bottom right)
   - Or press `D` to increase delay, `d` to decrease

4. **Zoom to Potholes**:
   - Deep purple circles are clearly visible
   - Zoom in to see vehicles stopping on them

## 🔧 Technical Details

### How It Works

#### 1. Network Generation (`indian_road_simulator.py`)
- Converts OSM data to SUMO network using `netconvert`
- Identifies 1978 main roads (motorway, trunk, primary, secondary, tertiary)
- Generates ~1500 deep purple circular potholes as visual polygons
- Creates continuous vehicle flows throughout simulation period

#### 2. TraCI Speed Control (`pothole_controller.py`)
- Loads pothole positions from `mymap.obstacles.xml`
- Maps potholes to road lanes using network geometry
- Monitors all vehicles every 0.1 seconds (simulation step)
- Detects pothole hits within 10m diameter zone (±5m from center)
- Applies instant speed reduction: `target_speed = original_max_speed * 0.01`
- Tracks hit time and enforces 5-second hold (50 steps)
- Restores normal speed after recovery period

#### 3. Key Variables
- `speed_mult = 0.01` → 99% reduction (1% of original speed)
- `RECOVERY_TIME = 50` → 5 seconds at 0.1s/step
- `pothole_zone = ±5.0m` → 10m diameter detection area
- `simulation_time = 7200s` → 2-hour simulation period

### Why TraCI Instead of VSS?

**Variable Speed Signs (VSS) failed** because:
- They set speed *limits*, not instant speed changes
- Vehicles gradually adjust to new limits
- Cannot force immediate speed drops

**TraCI solution** works because:
- Direct control over vehicle speed via `traci.vehicle.setSpeed()`
- Instant speed changes every simulation step
- Timer-based recovery mechanism
- Accurate 5-second hold duration

## 📊 Simulation Parameters

### Network Statistics
- **Nodes**: 5087
- **Edges**: 10168
- **Main Roads**: 1978
- **Potholes**: ~1500-1600
- **Route Success**: 91% (109/120 vehicles routed)

### Traffic Configuration
- **Vehicle Types**: 4 (auto, motorbike, car, bus)
- **Flow Rate**: ~90 vehicles/hour
- **Simulation Duration**: 7200 seconds (2 hours)
- **Flows**: 20 continuous flows (5 per vehicle type)

### Pothole Settings
- **Type**: Single uniform type (deep_purple)
- **Color**: RGB (0.5, 0, 0.5)
- **Size**: 0.8-1.5m diameter
- **Shape**: Circular (12-point polygon)
- **Speed Multiplier**: 0.01 (99% reduction)
- **Recovery Time**: 5 seconds

## 🐛 Troubleshooting

### Problem: Simulation ends too quickly
**Solution**: The simulation runs for 2 hours (7200s). If it ends earlier, check:
- Are vehicles successfully routed? (Check console output)
- Is the route file (`mymap.rou.xml`) generated correctly?

### Problem: No speed changes visible in GUI
**Solution**: 
- Speed changes ARE happening (check console output)
- Enable speed coloring: `View → Vehicles → Color by: speed`
- Vehicles turn blue/green when slowed in potholes
- Slow down simulation to see better: increase delay slider

### Problem: "Connection closed by SUMO"
**Solution**: Normal behavior when:
- All vehicles completed their routes
- Simulation reached end time
- User closed SUMO-GUI window

### Problem: Potholes not visible
**Solution**:
- Load additional files in SUMO: check `mymap.sumocfg` includes `mymap.obstacles.xml`
- Zoom in - potholes are small (0.8-1.5m)
- Look for deep purple circular shapes

### Problem: Import error for TraCI
**Solution**:
```bash
# Set SUMO_HOME
export SUMO_HOME=/usr/share/sumo  # or your installation path
# Add to ~/.bashrc or ~/.config/fish/config.fish for persistence
```

## 📝 Customization

### Change Pothole Color
Edit `indian_road_simulator.py`, line ~98:
```python
pothole_types = [
    ('deep_purple', '0.5,0,0.5', 0.01)  # Change RGB values here
]
```

### Adjust Speed Reduction
Edit `pothole_controller.py`, line ~53:
```python
speed_mult = 0.01  # Change to 0.05 for 95% reduction, 0.10 for 90%, etc.
```

### Change Recovery Time
Edit `pothole_controller.py`, line ~153:
```python
RECOVERY_TIME = 50  # Change to 30 for 3 seconds, 100 for 10 seconds, etc.
```

### Add More Vehicles
Edit `indian_road_simulator.py`, line ~200:
```python
for i in range(5):  # Change 5 to higher number for more flows per type
```

### Change Pothole Size
Edit `indian_road_simulator.py`, line ~172:
```python
size = random.uniform(0.8, 1.5)  # Change range for larger/smaller potholes
```

## 📚 Files Explained

### Core Python Scripts

**`indian_road_simulator.py`** (424 lines)
- Main setup and generation script
- Converts OSM → SUMO network
- Generates pothole polygons (visual only)
- Creates vehicle types and flows
- Configures SUMO simulation

**`pothole_controller.py`** (233 lines)
- TraCI-based real-time controller
- Loads pothole positions from XML
- Maps potholes to lanes
- Monitors vehicles every step
- Enforces 99% speed drop + 5s recovery

**`run_simulation.py`** (39 lines)
- Simple launcher script
- Checks if network exists
- Runs pothole_controller.py

### SUMO Configuration Files

**`mymap.osm`**
- OpenStreetMap XML data
- Contains Delhi road network
- Source for network generation

**`mymap.net.xml`**
- SUMO network file (generated)
- Contains nodes, edges, lanes, connections
- Used by SUMO for routing

**`mymap.obstacles.xml`**
- Pothole visual polygons
- Deep purple circular shapes
- Contains position coordinates

**`mymap.rou.xml`**
- Vehicle routes and flows
- Defines when/where vehicles spawn
- 20 continuous flows

**`mymap.sumocfg`**
- SUMO configuration file
- Lists all input files
- Sets simulation parameters

**`mymap.vtypes.xml`**
- Vehicle type definitions
- Speed, acceleration, size, etc.
- 4 types: auto, motorbike, car, bus

## 🎯 Project Goals Achieved

✅ **Indian road simulation** with realistic traffic
✅ **4 vehicle types** with distinct behaviors
✅ **Pothole speed reduction** - instant 99% drop
✅ **5-second recovery time** - vehicles slow, hold, then accelerate
✅ **Visual potholes** - deep purple circles clearly visible
✅ **TraCI control** - accurate real-time speed management
✅ **Continuous traffic** - 2-hour simulation with ongoing flows
✅ **Consistent behavior** - all potholes behave identically

## 📄 License

This project is created for educational and simulation purposes.

## 🙏 Credits

- **SUMO**: Eclipse SUMO - Simulation of Urban Mobility
- **OSM**: OpenStreetMap contributors for Delhi road data
- **TraCI**: Traffic Control Interface for real-time simulation control

---

**Generated**: October 06, 2025
**Version**: 1.0
**Status**: Production Ready ✅
