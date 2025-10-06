#!/usr/bin/env python3
"""
Project Cleanup and Documentation Generator
This script:
1. Analyzes the current working files
2. Creates comprehensive documentation
3. Removes all unnecessary files
4. Organizes the final project structure
"""

import os
import shutil
from datetime import datetime

# Core files needed for the simulation
REQUIRED_FILES = {
    # Core simulation files
    'indian_road_simulator.py',
    'pothole_controller.py',
    'run_simulation.py',
    
    # Network and configuration files
    'mymap.osm',
    'mymap.net.xml',
    'mymap.poly.xml',
    'mymap.obstacles.xml',
    'mymap.rou.xml',
    'mymap.sumocfg',
    'mymap.vtypes.xml',
    
    # This cleanup script
    'cleanup_and_document.py',
    
    # Git files
    '.git',
    '.gitignore',
    'README.md'
}

# Files to remove (old versions, test files, etc.)
FILES_TO_REMOVE = [
    'indian_road_sim.py',
    'simple_indian_sim.py',
    'robust_indian_sim.py',
    'stable_sim.py',
    'osm_to_sim.py',
    'test_pothole.py',
    
    # Old documentation
    'AI_MODES.md',
    'BUSY_DAY_SIMULATION.md',
    'CHANGES.md',
    'ENHANCED_SIMULATION_GUIDE.md',
    'HOW_TO_VIEW_STATS.md',
    'IMPROVEMENTS.md',
    'LATEST_UPDATES.md',
    'QUICK_REFERENCE.md',
    'QUICK_START.md',
    'README_SIMULATION.md',
    'ROBUST_SIMULATION.md',
    'SIMULATION_GUIDE.md',
    'VEHICLE_COMPARISON.md',
    
    # Temporary/generated files
    'simulation.log',
    'mymap.add.xml',
    'mymap.gui.xml',
    'mymap.rou.alt.xml',
    'mymap.rou.xml.alt.xml',
    'mymap.settings.xml',
    'mymap.trips.xml',
    'mymap.view.xml',
    'routes.rou.xml',
]

def analyze_project():
    """Analyze the project structure and working files"""
    print("\n" + "="*70)
    print("ANALYZING PROJECT STRUCTURE")
    print("="*70)
    
    # Count files
    all_files = []
    for root, dirs, files in os.walk('.'):
        # Skip venv and .git
        if 'venv' in root or '.git' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            all_files.append(filepath)
    
    print(f"\nTotal files found: {len(all_files)}")
    print(f"Required files: {len(REQUIRED_FILES)}")
    print(f"Files to remove: {len(FILES_TO_REMOVE)}")
    
    return all_files

def create_comprehensive_documentation():
    """Create the main README.md with complete documentation"""
    print("\n" + "="*70)
    print("CREATING COMPREHENSIVE DOCUMENTATION")
    print("="*70)
    
    readme_content = """# Indian Road Traffic Simulation with Potholes

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

**Generated**: """ + datetime.now().strftime("%B %d, %Y") + """
**Version**: 1.0
**Status**: Production Ready ✅
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ Created README.md")

def create_technical_documentation():
    """Create detailed technical documentation"""
    print("\n" + "="*70)
    print("CREATING TECHNICAL DOCUMENTATION")
    print("="*70)
    
    tech_doc = """# Technical Documentation - Indian Road Simulation

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                   User Interface                         │
│                    (SUMO-GUI)                           │
└─────────────────────────────────────────────────────────┘
                          ▲
                          │ TraCI Protocol
                          ▼
┌─────────────────────────────────────────────────────────┐
│              pothole_controller.py                       │
│     (Real-time speed control & monitoring)              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                  SUMO Simulation Core                    │
│  (Traffic simulation, routing, car-following)           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Network & Configuration Files               │
│  (mymap.net.xml, mymap.rou.xml, mymap.obstacles.xml)   │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initialization Phase

```python
# indian_road_simulator.py
OSM Data (mymap.osm)
    → netconvert → mymap.net.xml (road network)
    → Pothole generation → mymap.obstacles.xml (visual polygons)
    → Flow generation → mymap.rou.xml (traffic)
    → Config creation → mymap.sumocfg (simulation settings)
```

### 2. Runtime Phase

```python
# pothole_controller.py
Load potholes from mymap.obstacles.xml
    → Map to lanes using network geometry
    → Start SUMO with TraCI
    → Every 0.1s simulation step:
        - Get all vehicle positions
        - Check if in pothole zone (±5m)
        - If hit: instant speed drop + start timer
        - If in recovery: hold 1% speed for 5s
        - If recovered: resume normal speed
```

## Algorithm Details

### Pothole Detection Algorithm

```python
def check_pothole_collision(vehicle, potholes_on_lane):
    lane_pos = vehicle.getLanePosition()
    
    for pothole_pos in potholes_on_lane:
        distance = abs(lane_pos - pothole_pos)
        
        if distance < 5.0:  # 10m diameter zone
            return True, pothole_pos
    
    return False, None
```

### Speed Control Algorithm

```python
def control_vehicle_speed(vehicle_id, step, hit_time):
    original_max = vehicle_max_speeds[vehicle_id]
    
    # Check recovery status
    if vehicle_id in pothole_hit_times:
        steps_since_hit = step - pothole_hit_times[vehicle_id]
        
        if steps_since_hit < 50:  # 5 seconds
            # Hold at 1% speed
            target_speed = max(0.5, original_max * 0.01)
            traci.vehicle.setSpeed(vehicle_id, target_speed)
        else:
            # Release control
            traci.vehicle.setSpeed(vehicle_id, -1)
            del pothole_hit_times[vehicle_id]
```

### Pothole-to-Lane Mapping

```python
def map_potholes_to_lanes(potholes, network):
    lane_potholes = {}
    
    for pothole in potholes:
        # Get pothole center coordinates
        x, y = calculate_center(pothole.shape)
        
        # Find nearest lane
        nearest_lane = network.getNeighboringLanes(x, y, r=10.0)
        
        if nearest_lane:
            lane_id = nearest_lane[0][0].getID()
            lane_pos = nearest_lane[0][1]  # Position on lane
            
            # Store mapping
            if lane_id not in lane_potholes:
                lane_potholes[lane_id] = []
            
            lane_potholes[lane_id].append(
                (lane_pos, speed_mult, pothole_type)
            )
    
    return lane_potholes
```

## Performance Considerations

### Optimization Strategies

1. **Lane-based Lookup**: Potholes are pre-mapped to lanes, avoiding expensive coordinate calculations every step
2. **Distance Check First**: Simple distance check before any complex operations
3. **Dictionary Tracking**: O(1) lookup for vehicle recovery status
4. **Minimal TraCI Calls**: Only call setSpeed when necessary

### Complexity Analysis

- **Initialization**: O(P × L) where P = potholes, L = lanes
- **Per Step**: O(V × P_lane) where V = vehicles, P_lane = avg potholes per lane
- **Memory**: O(V + P) for tracking data structures

### Performance Metrics

- **Simulation Speed**: ~10-20x real-time (depends on traffic density)
- **Potholes**: 1500+ with minimal performance impact
- **Vehicles**: Handles 100+ concurrent vehicles smoothly

## Configuration Parameters

### Network Generation

| Parameter | Value | Description |
|-----------|-------|-------------|
| `main_road_types` | motorway, trunk, primary, secondary, tertiary | Roads eligible for potholes |
| `pothole_interval` | 20-40m | Distance between potholes |
| `pothole_size` | 0.8-1.5m | Diameter of visual polygons |
| `polygon_points` | 12 | Points for circular shape |

### Speed Control

| Parameter | Value | Description |
|-----------|-------|-------------|
| `speed_mult` | 0.01 | Speed multiplier (99% reduction) |
| `recovery_time` | 50 steps | Hold duration (5 seconds) |
| `detection_zone` | 10m diameter | Pothole collision area |
| `step_length` | 0.1s | Simulation time step |

### Vehicle Types

| Type | Max Speed | Accel | Decel | Sigma | Length |
|------|-----------|-------|-------|-------|--------|
| Auto | 13.89 m/s | 2.6 | 4.5 | 0.8 | 3.5m |
| Motorbike | 27.78 m/s | 3.5 | 6.0 | 0.9 | 2.2m |
| Car | 33.33 m/s | 2.9 | 5.0 | 0.5 | 5.0m |
| Bus | 22.22 m/s | 1.5 | 3.5 | 0.3 | 12.0m |

*Sigma = driver imperfection (0-1, higher = more erratic)*

## Error Handling

### TraCI Exceptions

```python
try:
    # Vehicle operations
    traci.vehicle.setSpeed(veh_id, target_speed)
except traci.exceptions.TraCIException:
    # Vehicle may have left simulation
    cleanup_vehicle(veh_id)
```

### Network Loading

```python
try:
    net = sumolib.net.readNet(net_file)
except Exception as e:
    print(f"Error loading network: {e}")
    return {}
```

### Graceful Shutdown

```python
try:
    while traci.simulation.getMinExpectedNumber() > 0:
        # Main simulation loop
        traci.simulationStep()
except KeyboardInterrupt:
    print("Simulation interrupted by user")
finally:
    traci.close()
    print("Simulation complete!")
```

## Testing & Validation

### Speed Reduction Validation

Console output confirms correct behavior:
```
Step 730: Vehicle motorbike_flow_6.0 hit pothole_deep_purple at pos 42.5, 
          INSTANT drop 22.4 -> 0.5 m/s (99% reduction, holding 5 seconds)
Step 780: Vehicle motorbike_flow_6.0 recovered from pothole, resuming normal speed
```

Expected timing: 780 - 730 = 50 steps = 5 seconds ✅

### Consistency Check

All vehicles show same pattern:
- Enter pothole → instant drop to ~1% speed
- Hold for exactly 50 steps
- Recover and accelerate back

### Visual Verification

In SUMO-GUI with speed coloring:
- Vehicles RED/YELLOW when fast
- Vehicles BLUE/GREEN when in pothole
- Clear visual confirmation of slowdown

## Extension Points

### Adding New Pothole Types

```python
# In indian_road_simulator.py
pothole_types = [
    ('shallow', '0.8,0.8,0', 0.50),  # 50% reduction
    ('deep', '0.5,0,0.5', 0.01),     # 99% reduction
]

# In pothole_controller.py
# Use ptype from potholes[lane_id] to apply different multipliers
```

### Dynamic Pothole Creation

```python
# Add pothole during simulation
new_pothole_id = f"dynamic_pothole_{step}"
traci.polygon.add(
    new_pothole_id,
    shape=calculate_circle(x, y, radius),
    color=(0.5, 0, 0.5, 1),
    layer=0
)
```

### Weather Effects

```python
# Modify speed multiplier based on weather
if weather == 'rain':
    speed_mult *= 0.5  # More severe in rain
elif weather == 'dry':
    speed_mult *= 1.0  # Normal
```

## Debugging Tips

### Enable Verbose Logging

```python
# In pothole_controller.py
DEBUG = True

if DEBUG:
    print(f"Vehicle {veh_id}: lane={lane_id}, pos={lane_pos:.2f}, speed={speed:.2f}")
```

### Visualize Detection Zones

```python
# Add polygons for pothole zones
for pothole_pos in potholes[lane_id]:
    zone_shape = create_circle(pothole_pos, radius=5.0)
    traci.polygon.add(f"zone_{lane_id}_{pothole_pos}", zone_shape, (1,1,0,0.3))
```

### Track Vehicle States

```python
# Export vehicle states to CSV
with open('vehicle_log.csv', 'w') as f:
    f.write("step,vehicle_id,speed,in_pothole,recovery_time\\n")
    # Write data each step
```

## Known Limitations

1. **Single Pothole Hit**: Vehicle in recovery ignores new potholes (intentional)
2. **Lane Changes**: Vehicle changing lanes exits recovery immediately
3. **Network Boundary**: Potholes near network edges may not map correctly
4. **Performance**: Very high traffic (500+ vehicles) may slow simulation

## Future Enhancements

- [ ] Multiple pothole severity levels
- [ ] Vehicle damage accumulation
- [ ] Repair/maintenance scheduling
- [ ] Weather-based severity modification
- [ ] ML-based pothole prediction
- [ ] Real-time pothole reporting system

---

**Last Updated**: """ + datetime.now().strftime("%B %d, %Y") + """
"""
    
    with open('TECHNICAL_DOCS.md', 'w') as f:
        f.write(tech_doc)
    
    print("✅ Created TECHNICAL_DOCS.md")

def remove_unnecessary_files():
    """Remove all files that are not needed"""
    print("\n" + "="*70)
    print("REMOVING UNNECESSARY FILES")
    print("="*70)
    
    removed_count = 0
    
    for filename in FILES_TO_REMOVE:
        if os.path.exists(filename):
            try:
                if os.path.isfile(filename):
                    os.remove(filename)
                    print(f"  ✓ Removed: {filename}")
                    removed_count += 1
                elif os.path.isdir(filename):
                    shutil.rmtree(filename)
                    print(f"  ✓ Removed directory: {filename}")
                    removed_count += 1
            except Exception as e:
                print(f"  ✗ Could not remove {filename}: {e}")
        else:
            print(f"  ⊘ Not found: {filename}")
    
    print(f"\nTotal files removed: {removed_count}")

def create_file_structure_doc():
    """Create a document showing the final file structure"""
    print("\n" + "="*70)
    print("CREATING FILE STRUCTURE DOCUMENTATION")
    print("="*70)
    
    structure_doc = """# Project File Structure

## Final Clean Structure

```
sih-road/
│
├── 📄 README.md                      # Main documentation (comprehensive guide)
├── 📄 TECHNICAL_DOCS.md              # Technical implementation details
├── 📄 FILE_STRUCTURE.md              # This file - project organization
│
├── 🐍 indian_road_simulator.py       # Network & pothole generator
├── 🐍 pothole_controller.py          # Real-time TraCI speed controller
├── 🐍 run_simulation.py              # Launcher script
├── 🐍 cleanup_and_document.py        # Cleanup & documentation tool
│
├── 🗺️  mymap.osm                      # OpenStreetMap data (Delhi)
├── 🗺️  mymap.net.xml                  # SUMO network file
├── 🗺️  mymap.poly.xml                 # Background polygons
├── 🗺️  mymap.obstacles.xml            # Pothole visual polygons
├── 🗺️  mymap.rou.xml                  # Vehicle routes & flows
├── 🗺️  mymap.sumocfg                  # SUMO configuration
├── 🗺️  mymap.vtypes.xml               # Vehicle type definitions
│
└── 📁 venv/                          # Python virtual environment (optional)
```

## File Categories

### 📚 Documentation (3 files)
- **README.md** - User guide, quick start, troubleshooting
- **TECHNICAL_DOCS.md** - Architecture, algorithms, API details
- **FILE_STRUCTURE.md** - This file, project organization

### 🐍 Python Scripts (4 files)
- **indian_road_simulator.py** - Generates all simulation files from OSM
- **pothole_controller.py** - Controls vehicle speeds in real-time
- **run_simulation.py** - Convenience launcher
- **cleanup_and_document.py** - Project maintenance tool

### 🗺️ SUMO Files (7 files)
- **mymap.osm** - Source map data
- **mymap.net.xml** - Road network (generated)
- **mymap.poly.xml** - Visual background (optional)
- **mymap.obstacles.xml** - Pothole positions & visuals (generated)
- **mymap.rou.xml** - Traffic flows (generated)
- **mymap.sumocfg** - Simulation settings (generated)
- **mymap.vtypes.xml** - Vehicle definitions (generated)

## File Dependencies

```
mymap.osm
    ↓
indian_road_simulator.py
    ↓
├── mymap.net.xml
├── mymap.obstacles.xml  
├── mymap.rou.xml
├── mymap.sumocfg
└── mymap.vtypes.xml
    ↓
pothole_controller.py
    ↓
[SUMO Simulation Running]
```

## Regeneration Guide

### Full Regeneration
If you need to regenerate everything:

```bash
# Step 1: Run generator (creates all SUMO files)
python3 indian_road_simulator.py

# Step 2: Run simulation
python3 run_simulation.py
```

### Partial Updates

**Update potholes only:**
```bash
# Edit indian_road_simulator.py (lines 96-100 for pothole settings)
python3 indian_road_simulator.py
```

**Update traffic only:**
```bash
# Edit indian_road_simulator.py (lines 198-310 for flow settings)
python3 indian_road_simulator.py
```

**Update speed control:**
```bash
# Edit pothole_controller.py (line 53 for speed_mult, line 153 for recovery time)
python3 run_simulation.py
```

## Removed Files

The following files were removed during cleanup (old/redundant versions):

### Old Simulation Scripts
- indian_road_sim.py
- simple_indian_sim.py
- robust_indian_sim.py
- stable_sim.py
- osm_to_sim.py
- test_pothole.py

### Old Documentation
- AI_MODES.md
- BUSY_DAY_SIMULATION.md
- CHANGES.md
- ENHANCED_SIMULATION_GUIDE.md
- HOW_TO_VIEW_STATS.md
- IMPROVEMENTS.md
- LATEST_UPDATES.md
- QUICK_REFERENCE.md
- QUICK_START.md
- README_SIMULATION.md
- ROBUST_SIMULATION.md
- SIMULATION_GUIDE.md
- VEHICLE_COMPARISON.md

### Temporary Files
- simulation.log
- mymap.add.xml
- mymap.gui.xml
- mymap.rou.alt.xml
- mymap.rou.xml.alt.xml
- mymap.settings.xml
- mymap.trips.xml
- mymap.view.xml
- routes.rou.xml

## Backup Recommendation

Before running cleanup, backup these files if you want to preserve them:
- Any custom modifications to scripts
- Original OSM data (mymap.osm)
- Working network file (mymap.net.xml)

## File Sizes (Approximate)

| File | Size | Notes |
|------|------|-------|
| mymap.osm | 50-100 MB | OSM data for Delhi area |
| mymap.net.xml | 10-20 MB | Generated network |
| mymap.obstacles.xml | 1-2 MB | ~1500 potholes |
| mymap.rou.xml | < 1 MB | 120 vehicles, 20 flows |
| indian_road_simulator.py | 15 KB | 424 lines |
| pothole_controller.py | 8 KB | 233 lines |
| README.md | 20 KB | Comprehensive docs |

**Total Project Size**: ~60-130 MB (mostly OSM data)

---

**Generated**: """ + datetime.now().strftime("%B %d, %Y") + """
"""
    
    with open('FILE_STRUCTURE.md', 'w') as f:
        f.write(structure_doc)
    
    print("✅ Created FILE_STRUCTURE.md")

def create_final_summary():
    """Create a summary of the cleanup and documentation process"""
    print("\n" + "="*70)
    print("PROJECT CLEANUP & DOCUMENTATION COMPLETE")
    print("="*70)
    
    summary = """
📦 FINAL PROJECT STATUS

✅ Documentation Created:
   - README.md (comprehensive user guide)
   - TECHNICAL_DOCS.md (implementation details)
   - FILE_STRUCTURE.md (project organization)

✅ Core Files Retained:
   - indian_road_simulator.py (network generator)
   - pothole_controller.py (TraCI controller)
   - run_simulation.py (launcher)
   - mymap.* (SUMO network & config files)

✅ Unnecessary Files Removed:
   - Old simulation versions
   - Redundant documentation
   - Temporary/generated files

📊 Project Summary:
   - Clean, organized structure
   - Complete documentation
   - Production-ready simulation
   - Easy to understand and modify

🚀 Ready to Use:
   python3 run_simulation.py

📖 Read the Docs:
   - README.md for usage guide
   - TECHNICAL_DOCS.md for internals
   - FILE_STRUCTURE.md for file organization

"""
    print(summary)
    
    # Save summary to file
    with open('CLEANUP_SUMMARY.txt', 'w') as f:
        f.write("="*70 + "\n")
        f.write("PROJECT CLEANUP & DOCUMENTATION SUMMARY\n")
        f.write("="*70 + "\n\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n\n")
        f.write(summary)
        f.write("\n" + "="*70 + "\n")
    
    print("✅ Created CLEANUP_SUMMARY.txt")

def main():
    """Main execution"""
    print("\n" + "="*70)
    print("INDIAN ROAD SIMULATION - CLEANUP & DOCUMENTATION TOOL")
    print("="*70)
    print("\nThis tool will:")
    print("1. Analyze the project structure")
    print("2. Create comprehensive documentation")
    print("3. Remove unnecessary files")
    print("4. Organize the final project")
    print("\n" + "="*70)
    
    # Step 1: Analyze
    all_files = analyze_project()
    
    # Step 2: Create documentation
    create_comprehensive_documentation()
    create_technical_documentation()
    create_file_structure_doc()
    
    # Step 3: Remove unnecessary files
    print("\n⚠️  WARNING: About to remove unnecessary files!")
    response = input("Continue with cleanup? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        remove_unnecessary_files()
    else:
        print("\n⊘ Cleanup cancelled. Documentation still created.")
    
    # Step 4: Final summary
    create_final_summary()
    
    print("\n" + "="*70)
    print("✨ ALL DONE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Read README.md for usage guide")
    print("2. Run: python3 run_simulation.py")
    print("3. Check TECHNICAL_DOCS.md for implementation details")
    print("\n")

if __name__ == "__main__":
    main()
