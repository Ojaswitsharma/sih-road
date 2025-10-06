# Indian Road Traffic Simulation - User Guide

## Overview
This simulation accurately models Indian road conditions using SUMO (Simulation of Urban Mobility).

## Features

### Vehicle Types (4 types, 50 each = 200 total)
1. **Auto-rickshaw** (Yellow)
   - Overtakes frequently
   - Medium distance trips
   - Medium speed (~50 km/h max)
   
2. **Motorbike** (Red)
   - Erratic speed changes
   - Frequent lane changes
   - Short distance trips
   - Fast and impatient

3. **Car** (Gray)
   - Average behavior
   - Long distance trips
   - Standard speed

4. **Bus** (Blue)
   - Slow moving
   - Long distance trips
   - Less maneuverable

### Potholes
- **~10,000+ potholes** across all roads
- **Main roads**: 4-10 potholes (more severe)
- **Local roads**: 2-6 potholes

#### Pothole Types:
- **Pink**: 50% speed reduction
- **Orange**: 75% speed reduction  
- **Red**: 90% speed reduction

### Road Coverage
- Main roads (highways, arterial): More potholes, more severe
- Local roads: Fewer potholes, less severe
- Minimum 30m spacing between potholes

## How to Run

```bash
python indian_road_simulator.py
```

The script will:
1. Convert OSM map to SUMO network
2. Generate potholes on all roads
3. Create vehicle routes
4. Launch SUMO GUI

## Viewing Vehicle Stats

**Right-click on any vehicle** in SUMO GUI to see:
- Current speed
- Maximum speed
- Speed reduction percentage
- Reason for slowdown
- Expected time to destination

## Understanding Speed Behavior

### How Potholes Work:
1. **Approach**: Vehicle sees reduced speed limit ahead
2. **Deceleration**: Vehicle begins slowing down
3. **Pothole Zone**: Vehicle maintains reduced speed (50%/75%/90% of normal)
4. **Exit**: Vehicle gradually accelerates back to normal speed

### Important Notes:
- Vehicles don't stop instantly at potholes
- They decelerate naturally based on their decel parameter
- Different vehicle types react differently:
  - Motorcycles: Quick decel (7.0 m/s²)
  - Buses: Slow decel (3.5 m/s²)
  
## Simulation Settings

- **Duration**: 2 hours (7200 seconds)
- **Step length**: 0.1 seconds (high precision)
- **Vehicles**: 200 total (50 per type)
- **Departure interval**: Every 5 seconds with randomness

## Tips for Best Results

1. **Zoom in** to see pothole colors clearly
2. **Follow vehicles** to observe speed changes
3. **Use right-click** to get detailed stats
4. **Watch main roads** for more pothole interactions
5. **Slow down simulation speed** in SUMO to observe behavior

## Known Limitations

- Some vehicle routes may not be generated if network is disconnected
- VSS (Variable Speed Signs) require vehicles to obey speed limits
- Vehicles need distance to decelerate - they won't stop instantly

## Troubleshooting

### Few vehicles appearing?
- Network may be disconnected - normal for real OSM data
- Check route generation output for success count

### Potholes not slowing vehicles?
- Vehicles need time/distance to decelerate
- Watch speed gradually decrease as they approach
- Some vehicles may already be slow due to traffic

### Speed not decreasing?
- Check if vehicle is actually over a pothole (zoom in)
- Verify pothole has correct color (pink/orange/red)
- Vehicle may be accelerating after passing previous pothole

## File Outputs

- `mymap.net.xml` - Road network
- `mymap.rou.xml` - Vehicle routes
- `mymap.obstacles.xml` - Potholes and speed zones
- `mymap.poly.xml` - Map polygons
- `mymap.sumocfg` - Simulation configuration

## Customization

Edit `indian_road_simulator.py`:

```python
# Increase vehicles
vehicles_per_type = 100  # Line ~240

# Change simulation time
SIMULATION_TIME = 10800  # 3 hours

# Adjust pothole density
# Main roads: int(length / 30)  # Line ~123
# Local roads: int(length / 50)  # Line ~125
```

## Statistics Summary

After running, you'll see:
```
Total vehicles: 200
Simulation time: 7200 seconds (120.0 minutes)
Vehicle types: auto, motorbike, car, bus (50 each)
Potholes: On ALL roads (pink=50%, orange=75%, red=90% speed reduction)
```

Routes created will vary based on network connectivity (typically 30-80 routes).
