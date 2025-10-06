# Technical Documentation - Indian Road Simulation

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
    f.write("step,vehicle_id,speed,in_pothole,recovery_time\n")
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

**Last Updated**: October 06, 2025
