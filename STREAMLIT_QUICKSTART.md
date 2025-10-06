# 🚀 Streamlit App - Quick Start Guide

## What Was Created

I've created a **Streamlit web interface** for your SUMO simulation with these features:

### ✨ Features
- 🎛️ **Interactive sliders** to configure:
  - Number of potholes per road (1-10)
  - Vehicles per class (10-200)
  - Simulation time (5 min - 2 hours)
  - Spawn interval (1-30 seconds)
- 🔧 **One-click file generation** with custom parameters
- ▶️ **Launch SUMO GUI** directly from the web interface
- 📊 **Real-time status** and simulation info

## 📁 New Files Created

1. **streamlit_app.py** - Main Streamlit application
2. **requirements_streamlit.txt** - Python dependencies
3. **run_streamlit.sh** - Quick launch script
4. **STREAMLIT_README.md** - Detailed documentation

## 🚀 How to Run

### Option 1: Using the Launch Script (Recommended)

```bash
# Make script executable (if not already)
chmod +x run_streamlit.sh

# Run the app
./run_streamlit.sh
```

### Option 2: Direct Command

```bash
# Install Streamlit (first time only)
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

## 📖 Usage Steps

1. **Start the app** - Your browser will open at `http://localhost:8501`

2. **Configure parameters** using the sidebar sliders:
   - Potholes per road
   - Vehicles per class
   - Simulation time
   - Spawn interval

3. **Generate files** - Click "🔧 Generate Simulation Files"
   - Wait for success message
   - All SUMO files will be created with your parameters

4. **Run simulation** - Click "▶️ Run Simulation"
   - SUMO GUI will open in a separate window
   - Watch vehicles slow down at potholes (purple circles)
   - Console shows real-time speed changes

5. **Stop simulation** - Close the SUMO GUI window

## 🎮 What You'll See

### In the Streamlit Interface:
- Parameter controls in the sidebar
- Current configuration summary
- Simulation status and logs
- Vehicle and pothole information

### In the SUMO GUI (separate window):
- 🟣 **Purple circles** = Potholes (99% speed reduction)
- 🛺 **Yellow** = Auto-rickshaws
- 🏍️ **Red** = Motorbikes
- 🚗 **Cyan** = Cars
- 🚌 **Blue** = Buses

### In the Console:
```
Step 18: Vehicle auto_0 hit deep_purple pothole at pos 26.6, INSTANT drop 13.8 -> 0.1 m/s
Step 68: Vehicle auto_0 recovered from pothole, resuming normal speed
```

## ⚙️ Technical Details

### How It Works:
1. Streamlit generates SUMO files dynamically based on your parameters
2. Calls `netconvert`, `polyconvert`, and `duarouter` to create the network
3. Generates potholes as polygons with metadata
4. Creates vehicle flows with your specified counts
5. Launches `pothole_controller.py` which uses TraCI to:
   - Monitor vehicle positions in real-time
   - Detect pothole hits
   - Apply instant 99% speed reduction
   - Hold for 5 seconds, then allow recovery

### Files Generated Each Time:
- `mymap.net.xml` - Road network
- `mymap.rou.xml` - Vehicle routes
- `mymap.obstacles.xml` - Pothole definitions
- `mymap.sumocfg` - SUMO configuration
- `mymap.gui.xml` - Visualization settings

## 🔧 Troubleshooting

### "SUMO not found"
```bash
# Install SUMO
sudo apt-get install sumo sumo-tools

# Set environment variable
export SUMO_HOME=/usr/share/sumo
```

### "Port already in use"
```bash
# Use a different port
streamlit run streamlit_app.py --server.port 8502
```

### "mymap.osm not found"
Make sure you're running from the directory containing `mymap.osm`

### Simulation doesn't start
- Check the Streamlit interface for error messages
- Verify files were generated successfully
- Look at console output for details

## 💡 Tips

1. **Start with defaults** - Use the default values first to test
2. **Increase gradually** - Add more vehicles/potholes incrementally
3. **Watch the console** - Real-time pothole hits are logged there
4. **Zoom in SUMO** - Use mouse wheel to see potholes clearly
5. **Right-click vehicles** - In SUMO to see their parameters

## 📊 Example Configurations

### Light Traffic Test
- Potholes: 3 per road
- Vehicles: 20 per class
- Time: 600s (10 min)
- Interval: 10s

### Medium Traffic (Default)
- Potholes: 6 per road
- Vehicles: 30 per class
- Time: 3600s (1 hour)
- Interval: 5s

### Heavy Traffic
- Potholes: 8 per road
- Vehicles: 100 per class
- Time: 7200s (2 hours)
- Interval: 2s

## 🎯 Next Steps

1. Try the default configuration first
2. Experiment with different parameter combinations
3. Watch how vehicles react to potholes
4. Adjust parameters to match your research needs
5. Export data or screenshots from SUMO as needed

## 📚 More Information

- See **STREAMLIT_README.md** for detailed documentation
- See **HOW_TO_RUN.md** for original simulation instructions
- SUMO docs: https://sumo.dlr.de/docs/

---

**Enjoy your interactive simulation! 🚗💨**
