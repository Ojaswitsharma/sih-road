# Indian Road Pothole Simulator - Streamlit Interface

A web-based interface for configuring and running SUMO traffic simulations with potholes on Indian roads.

## Features

- 🎛️ **Interactive Controls**: Adjust simulation parameters via sliders
- 🕳️ **Configurable Potholes**: Set number of potholes per road (1-10)
- 🚗 **Vehicle Classes**: Configure vehicles per class (10-200)
- ⏱️ **Flexible Duration**: Set simulation time (5 min - 2 hours)
- 🔄 **Spawn Control**: Adjust vehicle spawn intervals (1-30 seconds)
- 📊 **Real-time Monitoring**: View simulation status and logs

## Installation

### Prerequisites

1. **SUMO** (Simulation of Urban MObility)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install sumo sumo-tools sumo-doc
   
   # Set SUMO_HOME environment variable
   export SUMO_HOME=/usr/share/sumo
   ```

2. **Python 3.7+** with pip

3. **Streamlit**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

## Usage

### 1. Start the Streamlit App

```bash
streamlit run streamlit_app.py
```

This will open your browser at `http://localhost:8501`

### 2. Configure Parameters

Use the sidebar to adjust:
- **Potholes per Road**: Number of potholes on each main road
- **Vehicles per Class**: How many vehicles of each type (auto, motorbike, car, bus)
- **Simulation Time**: Total duration in seconds
- **Spawn Interval**: Time between vehicle spawns

### 3. Generate Simulation

Click **"🔧 Generate Simulation Files"** to create all necessary SUMO files with your parameters.

### 4. Run Simulation

Click **"▶️ Run Simulation"** to launch the SUMO GUI with pothole detection.

## How It Works

### Simulation Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Potholes per Road | 1-10 | 6 | Number of potholes on each main road |
| Vehicles per Class | 10-200 | 30 | Vehicles for each type (×4 types) |
| Simulation Time | 300-7200s | 3600s | Total simulation duration |
| Spawn Interval | 1-30s | 5s | Time between vehicle spawns |

### Vehicle Types

- 🛺 **Auto-rickshaw**: Medium speed, agile, yellow
- 🏍️ **Motorbike**: Fast, erratic, red
- 🚗 **Car**: Average behavior, cyan
- 🚌 **Bus**: Slow, less maneuverable, blue

### Pothole Behavior

- 🟣 **Deep Purple Potholes**: 99% speed reduction
- Vehicles drop to 1% of their speed instantly when hitting a pothole
- Effect lasts for 5 seconds
- Then vehicles gradually recover to normal speed

## File Structure

```
.
├── streamlit_app.py           # Main Streamlit application
├── requirements_streamlit.txt # Python dependencies
├── pothole_controller.py      # SUMO TraCI controller
├── mymap.osm                  # OpenStreetMap data (required)
└── Generated files:
    ├── mymap.net.xml          # SUMO network
    ├── mymap.rou.xml          # Vehicle routes
    ├── mymap.obstacles.xml    # Pothole definitions
    └── mymap.sumocfg          # SUMO configuration
```

## Troubleshooting

### SUMO not found
```bash
# Check if SUMO is installed
which sumo

# Set SUMO_HOME if needed
export SUMO_HOME=/usr/share/sumo
```

### OSM file missing
Ensure `mymap.osm` exists in the same directory as the Streamlit app.

### Port already in use
```bash
# Run on a different port
streamlit run streamlit_app.py --server.port 8502
```

### Simulation doesn't start
- Check that all files were generated successfully
- Verify SUMO_HOME is set correctly
- Look for error messages in the Streamlit interface

## Advanced Usage

### Running from Command Line

You can still run simulations without Streamlit:

```bash
# Generate with default parameters
python3 indian_road_simulator.py

# Run with pothole controller
python3 pothole_controller.py
```

### Customizing Vehicle Behavior

Edit the vehicle type definitions in `streamlit_app.py` in the `generate_vehicle_types()` function to adjust:
- Acceleration/deceleration
- Max speed
- Lane changing behavior
- Colors and shapes

### Modifying Pothole Effects

Edit `pothole_controller.py` to change:
- Speed reduction percentage (currently 99%)
- Recovery time (currently 5 seconds)
- Detection zone size (currently 5m radius)

## Tips

1. **Start Small**: Begin with fewer vehicles and shorter simulation times to test
2. **Watch Console**: The terminal shows real-time pothole hit events
3. **SUMO GUI**: Right-click vehicles to see their parameters and speed
4. **Performance**: More vehicles = slower simulation. Adjust based on your system
5. **Potholes**: Purple circles on roads - zoom in to see them clearly

## Known Limitations

- SUMO GUI opens in a separate window (cannot be embedded directly in browser)
- Simulation must be stopped manually by closing SUMO window
- Large simulations (>500 vehicles) may slow down on older hardware

## Support

For issues or questions:
1. Check the console output for error messages
2. Verify all prerequisites are installed
3. Ensure `mymap.osm` file exists and is valid
4. Check SUMO documentation: https://sumo.dlr.de/docs/

## License

This project uses SUMO (Eclipse Public License 2.0) and Streamlit (Apache License 2.0).
