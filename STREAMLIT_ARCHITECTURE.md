# Streamlit App Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB INTERFACE                  │
│                     (streamlit_app.py)                      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Sidebar    │  │  Main Area   │  │  Status Log  │    │
│  │              │  │              │  │              │    │
│  │ • Potholes   │  │ • Generate   │  │ • Real-time  │    │
│  │ • Vehicles   │  │   Button     │  │   Updates    │    │
│  │ • Time       │  │ • Run Button │  │ • Errors     │    │
│  │ • Interval   │  │ • Info Panel │  │ • Success    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              FILE GENERATION PIPELINE                       │
│                                                             │
│  1. netconvert    → mymap.net.xml     (Road network)       │
│  2. polyconvert   → mymap.poly.xml    (Buildings/areas)    │
│  3. generate      → mymap.obstacles.xml (Potholes)         │
│  4. generate      → mymap.trips.xml   (Vehicle flows)      │
│  5. duarouter     → mymap.rou.xml     (Routes)             │
│  6. generate      → mymap.sumocfg     (Configuration)      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  SUMO SIMULATION                            │
│                                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │              SUMO GUI (Separate Window)          │     │
│  │                                                  │     │
│  │  • Visual representation of roads               │     │
│  │  • Vehicles moving                              │     │
│  │  • Purple pothole circles                       │     │
│  │  • Real-time animation                          │     │
│  └──────────────────────────────────────────────────┘     │
│                            │                               │
│                            ▼                               │
│  ┌──────────────────────────────────────────────────┐     │
│  │         TraCI Controller                         │     │
│  │      (pothole_controller.py)                     │     │
│  │                                                  │     │
│  │  • Monitor vehicle positions (10 Hz)            │     │
│  │  • Detect pothole hits                          │     │
│  │  • Apply speed reduction (99%)                  │     │
│  │  • Hold for 5 seconds                           │     │
│  │  • Allow recovery                               │     │
│  └──────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Input (Streamlit)
    │
    ├─ Potholes per road: 6
    ├─ Vehicles per class: 30
    ├─ Simulation time: 3600s
    └─ Spawn interval: 5s
    │
    ▼
Parameter Processing
    │
    ├─ Calculate total vehicles: 30 × 4 = 120
    ├─ Calculate flow period: 3600 / 30 = 120s
    ├─ Determine pothole positions
    └─ Generate edge selections
    │
    ▼
File Generation
    │
    ├─ Network: OSM → SUMO network
    ├─ Potholes: Random positions on main roads
    ├─ Vehicles: Flow definitions for 4 types
    └─ Config: Combine all settings
    │
    ▼
Simulation Execution
    │
    ├─ SUMO loads network
    ├─ TraCI connects
    ├─ Vehicles spawn
    └─ Pothole detection active
    │
    ▼
Real-time Control Loop (10 Hz)
    │
    ├─ Get all vehicle IDs
    ├─ For each vehicle:
    │   ├─ Get position (lane, lane_pos)
    │   ├─ Check if near pothole (±5m)
    │   ├─ If hit: Apply 99% reduction
    │   ├─ If in recovery: Hold speed
    │   └─ If recovered: Resume normal
    └─ Log events to console
```

## Component Interaction

### 1. Streamlit App (streamlit_app.py)

**Responsibilities:**
- User interface and parameter collection
- File generation orchestration
- Subprocess management
- Status reporting

**Key Functions:**
```python
generate_simulation_files()  # Creates all SUMO files
generate_vehicle_types()     # Vehicle definitions
generate_potholes()          # Pothole placement
generate_trips()             # Vehicle flows
run_simulation_background()  # Launch SUMO
```

### 2. Pothole Controller (pothole_controller.py)

**Responsibilities:**
- Real-time vehicle monitoring
- Pothole hit detection
- Speed manipulation
- Recovery timing

**Key Functions:**
```python
load_potholes()      # Parse obstacles.xml
run_simulation()     # Main TraCI loop
# Speed control logic in main loop
```

### 3. SUMO Components

**Network (mymap.net.xml):**
- Road geometry
- Lane definitions
- Junction logic
- Speed limits

**Routes (mymap.rou.xml):**
- Vehicle types
- Flow definitions
- Departure times
- Origin-destination pairs

**Obstacles (mymap.obstacles.xml):**
- Pothole polygons (visual)
- Pothole metadata (comments)
- Position information

## Parameter Impact

### Potholes per Road
```
1-3:   Light pothole density
4-6:   Medium density (realistic)
7-10:  Heavy density (stress test)
```

### Vehicles per Class
```
10-30:   Light traffic
31-100:  Medium traffic
101-200: Heavy traffic (may slow simulation)
```

### Simulation Time
```
300s:   Quick test (5 min)
1800s:  Short run (30 min)
3600s:  Standard (1 hour)
7200s:  Long run (2 hours)
```

### Spawn Interval
```
1-2s:   Very frequent (dense traffic)
3-5s:   Normal frequency
6-10s:  Sparse traffic
11-30s: Very sparse
```

## Performance Considerations

### CPU Usage
- Streamlit: Low (just UI)
- SUMO: Medium-High (depends on vehicles)
- TraCI: Low (10 Hz polling)

### Memory Usage
- Network: ~10-50 MB
- Vehicles: ~1 KB per vehicle
- GUI: ~100-200 MB

### Bottlenecks
1. **Vehicle count**: More vehicles = slower simulation
2. **Network size**: Larger maps = more processing
3. **GUI rendering**: Visual quality affects performance

## Extending the System

### Add New Vehicle Type
1. Edit `generate_vehicle_types()` in streamlit_app.py
2. Add vType definition with parameters
3. Add to flow generation loop
4. Update UI to show new type

### Modify Pothole Behavior
1. Edit `pothole_controller.py`
2. Change speed_mult value (0.01 = 99% reduction)
3. Adjust RECOVERY_TIME (50 steps = 5 seconds)
4. Modify detection zone (±5m)

### Add New Parameters
1. Add slider in Streamlit sidebar
2. Pass to generation functions
3. Use in file generation
4. Update documentation

### Export Simulation Data
1. Add TraCI data collection in controller
2. Write to CSV/JSON during simulation
3. Add download button in Streamlit
4. Process data for analysis

## File Dependencies

```
streamlit_app.py
    ├─ Requires: mymap.osm (input)
    ├─ Generates: mymap.net.xml
    ├─ Generates: mymap.poly.xml
    ├─ Generates: mymap.obstacles.xml
    ├─ Generates: mymap.trips.xml
    ├─ Generates: mymap.rou.xml
    ├─ Generates: mymap.sumocfg
    └─ Calls: pothole_controller.py

pothole_controller.py
    ├─ Reads: mymap.obstacles.xml
    ├─ Reads: mymap.net.xml
    ├─ Reads: mymap.sumocfg
    └─ Controls: SUMO via TraCI
```

## Error Handling

### Generation Errors
- OSM file missing → Clear error message
- SUMO tools not found → Installation instructions
- Invalid parameters → Validation before generation

### Runtime Errors
- TraCI connection lost → Graceful shutdown
- Vehicle disappeared → Skip and continue
- Pothole parsing error → Log and skip

### User Errors
- No files generated → Disable run button
- Simulation already running → Prevent duplicate launch
- Invalid configuration → Show warnings

---

This architecture allows for:
- ✅ Easy parameter adjustment
- ✅ Reproducible simulations
- ✅ Real-time control
- ✅ Extensibility
- ✅ Error recovery
