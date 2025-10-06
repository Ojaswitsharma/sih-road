# 🚗 Indian Road Pothole Simulator - Streamlit Web App

A web-based interface for configuring and running SUMO traffic simulations with potholes on Indian roads. Configure parameters with sliders, generate simulation files with one click, and visualize traffic behavior around potholes.

![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SUMO](https://img.shields.io/badge/SUMO-Traffic_Simulation-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Parameters](#-parameters)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Documentation](#-documentation)

---

## ✨ Features

### Interactive Configuration
- 🎛️ **Slider controls** for all simulation parameters
- 🕳️ **Potholes per road**: 1-10 (adjustable)
- 🚗 **Vehicles per class**: 1-200 (adjustable)
- ⏱️ **Simulation time**: 5 min - 2 hours
- 🔄 **Spawn interval**: 1-30 seconds

### One-Click Operations
- 🔧 **Generate simulation files** dynamically based on parameters
- ▶️ **Launch SUMO GUI** with one button click
- 📊 **Real-time status** updates and error handling

### Simulation Features
- 🟣 **Pothole effects**: 99% speed reduction for 5 seconds
- 🛺 **4 vehicle types**: Auto-rickshaw, Motorbike, Car, Bus
- 📈 **Consistent vehicle IDs**: Predictable naming (e.g., `auto_0`, `auto_1`)
- 🎯 **Even distribution**: Vehicles spawn evenly across simulation time

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install streamlit traci

# Install SUMO (Ubuntu/Debian)
sudo apt-get install sumo sumo-tools

# Set SUMO_HOME
export SUMO_HOME=/usr/share/sumo
```

Or use the automated script:

```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### 2. Run the App

```bash
# Option 1: Use the launch script
chmod +x run_streamlit.sh
./run_streamlit.sh

# Option 2: Direct command
streamlit run streamlit_app.py
```

### 3. Use the Interface

1. **Browser opens** at `http://localhost:8501`
2. **Adjust parameters** using sliders in the sidebar
3. **Click "Generate Simulation Files"**
4. **Click "Run Simulation"**
5. **SUMO GUI opens** in a separate window

---

## 📦 Installation

### Prerequisites

- **Python 3.7+**
- **SUMO** (Simulation of Urban MObility)
- **pip** (Python package manager)

### Step-by-Step Installation

#### 1. Install SUMO

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```

**macOS:**
```bash
brew install sumo
```

**Windows:**
Download from [SUMO Downloads](https://sumo.dlr.de/docs/Downloads.php)

#### 2. Set SUMO_HOME

**Linux/macOS:**
```bash
export SUMO_HOME=/usr/share/sumo
# Make permanent
echo 'export SUMO_HOME=/usr/share/sumo' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
```cmd
setx SUMO_HOME "C:\Program Files (x86)\Eclipse\Sumo"
```

#### 3. Install Python Packages

```bash
# Install Streamlit
pip install streamlit

# Install TraCI (SUMO Python API)
pip install traci
```

#### 4. Verify Installation

```bash
# Check SUMO
sumo-gui --version

# Check Python packages
python3 -c "import streamlit; import traci; print('All packages installed!')"
```

---

## 🎮 Usage

### Starting the App

```bash
streamlit run streamlit_app.py
```

Your browser will automatically open to `http://localhost:8501`

### Configuring Parameters

**Sidebar Controls:**

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| **Potholes per Road** | 1-10 | 6 | Number of potholes on each main road |
| **Vehicles per Class** | 1-200 | 30 | Vehicles for each type (×4 types) |
| **Simulation Time** | 300-7200s | 3600s | Total simulation duration |
| **Spawn Interval** | 1-30s | 5s | Time between vehicle spawns |

### Generating Simulation

1. **Adjust sliders** to your desired values
2. **Click "🔧 Generate Simulation Files"**
3. **Wait for success message** (usually 10-30 seconds)
4. **Files created:**
   - `mymap.net.xml` - Road network
   - `mymap.rou.xml` - Vehicle routes
   - `mymap.obstacles.xml` - Pothole definitions
   - `mymap.sumocfg` - SUMO configuration

### Running Simulation

1. **Click "▶️ Run Simulation"**
2. **SUMO GUI opens** in a separate window
3. **Watch the simulation:**
   - 🟣 Purple circles = Potholes
   - 🛺 Yellow = Auto-rickshaws
   - 🏍️ Red = Motorbikes
   - 🚗 Cyan = Cars
   - 🚌 Blue = Buses
4. **Console shows** real-time pothole hits
5. **Close SUMO window** to stop

---

## 🎛️ Parameters

### Potholes per Road

**Effect:** Controls pothole density on main roads

- **1-3**: Sparse (occasional slowdowns)
- **4-6**: Medium (realistic Indian roads)
- **7-10**: Dense (frequent disruptions)

**Example:**
- 3 potholes/road × 45 main roads = ~135 total potholes

### Vehicles per Class

**Effect:** Number of each vehicle type spawned

- **1-10**: Light traffic (easy to observe individual vehicles)
- **11-50**: Medium traffic (realistic flow)
- **51-200**: Heavy traffic (congestion scenarios)

**Vehicle Types:**
- Auto-rickshaw (🛺)
- Motorbike (🏍️)
- Car (🚗)
- Bus (🚌)

**Total vehicles** = Vehicles per class × 4

**Example:**
- 30 vehicles/class = 120 total vehicles

### Simulation Time

**Effect:** How long the simulation runs

- **300s (5 min)**: Quick test
- **1800s (30 min)**: Short analysis
- **3600s (1 hour)**: Standard run
- **7200s (2 hours)**: Extended study

**Note:** Vehicles spawn evenly across this time

### Spawn Interval

**Effect:** Time between vehicle spawns (legacy parameter, now uses even distribution)

- Vehicles are distributed evenly across simulation time
- With 10 vehicles and 1000s simulation: one every 100s

---

## 🔧 How It Works

### Architecture

```
┌─────────────────────────────────────────┐
│     Streamlit Web Interface             │
│  (Browser: http://localhost:8501)      │
│                                         │
│  • Parameter sliders                   │
│  • Generate button                     │
│  • Run button                          │
│  • Status display                      │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     File Generation Pipeline            │
│                                         │
│  1. netconvert → Network from OSM      │
│  2. polyconvert → Buildings/areas      │
│  3. generate_potholes() → Obstacles    │
│  4. generate_trips() → Vehicle trips   │
│  5. duarouter → Calculate routes       │
│  6. generate_config() → SUMO config    │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     SUMO Simulation (Separate Window)   │
│                                         │
│  • Visual road network                 │
│  • Animated vehicles                   │
│  • Pothole polygons                    │
│  • Real-time traffic flow              │
└─────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│     TraCI Controller                    │
│     (pothole_controller.py)             │
│                                         │
│  • Monitor vehicle positions (10 Hz)   │
│  • Detect pothole hits (±5m zone)      │
│  • Apply speed reduction (99%)         │
│  • Hold for 5 seconds                  │
│  • Allow recovery                      │
└─────────────────────────────────────────┘
```

### Pothole Behavior

1. **Detection**: Vehicle enters 5m radius around pothole
2. **Impact**: Speed drops to 1% instantly (99% reduction)
3. **Duration**: Effect lasts 5 seconds
4. **Recovery**: Vehicle gradually accelerates back to normal speed

**Example:**
```
Vehicle traveling at 13.8 m/s
→ Hits pothole
→ Speed drops to 0.14 m/s (99% reduction)
→ Holds for 5 seconds
→ Recovers to normal speed
```

### Vehicle Naming

Vehicles have consistent, predictable IDs:

**Format:** `{type}_{number}`

**Examples:**
- `auto_0`, `auto_1`, `auto_2`
- `motorbike_0`, `motorbike_1`
- `car_0`, `car_1`
- `bus_0`, `bus_1`

**No more random IDs** like `auto0.0`, `auto4.2`, etc.

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'traci'"

**Solution:**
```bash
pip install traci
```

Or use SUMO's built-in TraCI:
```bash
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

### "SUMO_HOME not set"

**Solution:**
```bash
export SUMO_HOME=/usr/share/sumo
echo 'export SUMO_HOME=/usr/share/sumo' >> ~/.bashrc
```

### "Can't see SUMO window"

**Reason:** SUMO GUI opens in a **separate window**, not in the browser.

**Solution:**
- Check your taskbar/dock
- Look for "SUMO" in window titles
- Try Alt+Tab (Windows/Linux) or Cmd+Tab (Mac)
- Window may be behind your browser

### "mymap.osm not found"

**Solution:**
- Ensure `mymap.osm` exists in the same directory
- Download or create an OSM file for your area
- Place it in the project root directory

### "Port already in use"

**Solution:**
```bash
# Use a different port
streamlit run streamlit_app.py --server.port 8502
```

### "Command failed: netconvert"

**Solution:**
- Verify SUMO is installed: `which netconvert`
- Check SUMO_HOME is set: `echo $SUMO_HOME`
- Reinstall SUMO if necessary

### "No vehicles appear"

**Possible causes:**
1. **Simulation time too short** - Increase simulation time
2. **Routes not found** - Check console for routing errors
3. **Network issues** - Verify `mymap.net.xml` was generated

**Solution:**
- Try with default parameters first
- Check console output for errors
- Regenerate files

---

## ❓ FAQ

### Can SUMO GUI be embedded in the browser?

**No.** SUMO GUI is a native desktop application and cannot be embedded in a web browser due to security restrictions. It will always open in a separate window.

### Why do I need both Streamlit and SUMO GUI?

- **Streamlit (browser):** Configuration and control interface
- **SUMO GUI (separate window):** Visual simulation display

They work together but cannot be combined.

### How many vehicles should I use?

**Recommendations:**
- **Testing:** 1-10 vehicles per class (4-40 total)
- **Demonstration:** 20-50 vehicles per class (80-200 total)
- **Research:** 30-100 vehicles per class (120-400 total)

**Note:** More vehicles = slower simulation

### Can I run without the GUI?

Yes! Modify `pothole_controller.py` to use `sumo` instead of `sumo-gui` for headless mode. This is useful for:
- Batch processing
- Server environments
- Data collection without visualization

### How accurate is the pothole simulation?

The simulation models:
- ✅ Instant speed reduction (realistic)
- ✅ Recovery time (5 seconds)
- ✅ Vehicle-specific behavior
- ⚠️ Simplified physics (not a full vehicle dynamics model)

**Best for:** Traffic flow analysis, behavior studies, demonstrations

### Can I export simulation data?

Currently, data is shown in the console. To export:
1. Modify `pothole_controller.py` to write to CSV/JSON
2. Collect statistics during simulation
3. Save to file for analysis

### What OSM file should I use?

- **Included:** `mymap.osm` (if provided)
- **Custom:** Export from [OpenStreetMap](https://www.openstreetmap.org/)
- **Requirements:** Must include roads suitable for vehicles

---

## 📚 Documentation

### Quick References

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page cheat sheet
- **[STREAMLIT_QUICKSTART.md](STREAMLIT_QUICKSTART.md)** - 3-step quick start
- **[INSTALL_TRACI.md](INSTALL_TRACI.md)** - TraCI installation guide

### Detailed Guides

- **[STREAMLIT_README.md](STREAMLIT_README.md)** - Complete documentation
- **[STREAMLIT_ARCHITECTURE.md](STREAMLIT_ARCHITECTURE.md)** - Technical details
- **[BEFORE_AFTER_COMPARISON.md](BEFORE_AFTER_COMPARISON.md)** - CLI vs Streamlit

### Index

- **[STREAMLIT_INDEX.md](STREAMLIT_INDEX.md)** - Master documentation index

---

## 🎯 Example Workflows

### Quick Test (5 minutes)

```bash
# 1. Start app
streamlit run streamlit_app.py

# 2. Set parameters
Potholes: 3
Vehicles: 5 per class
Time: 300s (5 min)

# 3. Generate & Run
Click "Generate" → Click "Run"

# 4. Observe
Watch 20 vehicles navigate 3 potholes/road
```

### Research Study (1 hour)

```bash
# 1. Start app
streamlit run streamlit_app.py

# 2. Set parameters
Potholes: 6
Vehicles: 50 per class
Time: 3600s (1 hour)

# 3. Generate & Run
Click "Generate" → Click "Run"

# 4. Collect data
Monitor console for pothole hit statistics
```

### Demonstration (30 minutes)

```bash
# 1. Start app
streamlit run streamlit_app.py

# 2. Set parameters
Potholes: 8
Vehicles: 30 per class
Time: 1800s (30 min)

# 3. Generate & Run
Click "Generate" → Click "Run"

# 4. Present
Show SUMO GUI to audience
Explain pothole effects in real-time
```

---

## 🤝 Contributing

Suggestions for improvements:
1. Add data export functionality
2. Implement headless mode with Streamlit charts
3. Add more vehicle types
4. Customize pothole severity levels
5. Add traffic light control

---

## 📄 License

This project uses:
- **SUMO:** Eclipse Public License 2.0
- **Streamlit:** Apache License 2.0

---

## 🙏 Acknowledgments

- **SUMO Team** - Traffic simulation platform
- **Streamlit** - Web app framework
- **OpenStreetMap** - Map data

---

## 📞 Support

**Issues?**
1. Check [Troubleshooting](#-troubleshooting) section
2. Review [FAQ](#-faq)
3. Read detailed documentation files
4. Check console output for errors

**Resources:**
- SUMO Documentation: https://sumo.dlr.de/docs/
- Streamlit Documentation: https://docs.streamlit.io/
- TraCI Tutorial: https://sumo.dlr.de/docs/TraCI.html

---

## 🚀 Getting Started Checklist

- [ ] Install SUMO
- [ ] Set SUMO_HOME environment variable
- [ ] Install Python packages (streamlit, traci)
- [ ] Verify `mymap.osm` exists
- [ ] Run `streamlit run streamlit_app.py`
- [ ] Configure parameters in sidebar
- [ ] Generate simulation files
- [ ] Run simulation
- [ ] Look for SUMO GUI window (separate from browser!)

---

**Ready to simulate! 🚗💨**

*For detailed information, see the documentation files in the project directory.*
