# Project File Structure

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

**Generated**: October 06, 2025
