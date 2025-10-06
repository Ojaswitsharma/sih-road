# Indian Road Traffic Simulation - Complete Guide

## ✅ What's Working Now

### Vehicles (400 Total - 100 of Each Type)
1. **🛺 Auto-rickshaws (Yellow)** - Rash driving, frequent overtaking
   - High speed factor (1.3x)
   - Low cooperation (0.2)
   - High lane change aggression (3.0)
   - Impatient (0.8)

2. **🏍️ Motorcycles (Red)** - Erratic lane changes, variable speed
   - Very high speed factor (1.5x) 
   - Almost no cooperation (0.1)
   - Extremely aggressive lane changes (4.0)
   - Maximum impatience (1.0)

3. **🚗 Cars (Gray)** - Normal speed, stable driving
   - Normal speed factor (1.0x)
   - Balanced cooperation (1.0)
   - Standard lane changing (1.0)
   - Low impatience (0.3)

4. **🚌 Buses (Blue)** - Slow, stable, less maneuverable
   - Low speed factor (0.8x)
   - High cooperation (1.5)
   - Minimal lane changes (0.3)
   - Very patient (0.1)

### Obstacles
- **5,892 Potholes** with **99% speed reduction** (vehicles slow to 1% speed!)
  - Dark gray color (highly visible)
  - Spread across all lanes
  - 20-30 per road
  - Variable sizes (mostly small)

- **4 Barricades** (Yellow with black stripes)
  - Block specific lanes
  - Force vehicles to change lanes
  - Highly visible
  - Layer 100-101 (always on top)

## 🎯 How to See Vehicle Stats

### Method 1: Right-Click on Vehicle
1. Right-click any vehicle in the simulation
2. Click **"Show Parameter"**
3. You'll see a window with:
   - **Type** (auto/motorcycle/car/bus)
   - **Current Speed** (km/h)
   - **Desired Speed** (target speed)
   - **Position** (x, y coordinates)
   - **Lane** (current lane ID)
   - **Route** (planned path)
   - **Waiting Time** (seconds stopped)
   - **CO2 Emissions** (mg)

### Method 2: Enable Name Display
1. **Edit → Edit Visualization** (or press F9)
2. Click on **"Vehicles"** tab
3. Check ☑ **"Show vehicle name"**
4. Adjust **"vehicle name size"** slider to 60-100
5. Click **"Recenter View"** button
6. Click **"OK"**

Now you'll see vehicle IDs above each vehicle (e.g., "auto_5", "motorcycle_23")

### Method 3: Color by Speed
1. **Edit → Edit Visualization**
2. **Vehicles** tab
3. **"Color vehicles by:"** dropdown → Select **"speed"**
4. Vehicles will change color based on speed:
   - **Dark Red/Purple** = Stopped or very slow (in potholes!)
   - **Orange/Yellow** = Medium speed
   - **Green/Cyan** = Fast/Normal speed

### Method 4: Track Individual Vehicle
1. Right-click vehicle → **"Start Tracking"**
2. Camera follows the vehicle
3. Bottom panel shows real-time stats
4. Press **ESC** to stop tracking

### Method 5: Select Vehicle to See Details
1. Right-click vehicle → **"Select Vehicle"**
2. Vehicle highlighted in bright color
3. **Bottom panel** shows continuous stats:
   - Current speed
   - Acceleration
   - Position
   - Lane
   - Route progress

## 🚦 How to See the Simulation Better

### Best View Settings
1. **Zoom**: Use mouse wheel or +/- keys
2. **Pan**: Right-click and drag
3. **Recenter**: Press **Home** key

### To See Potholes Clearly
1. **Edit → Edit Visualization**
2. **"Polygons"** tab
3. Check ☑ **"Show polygon names"**
4. Increase **"polygon size exaggeration"** to 2-3
5. You'll see dark gray irregular shapes (potholes)

### To See Barricades
1. Look for **yellow rectangles with black diagonal stripes**
2. They're on layer 100-101 (always visible)
3. Usually in the middle of roads
4. Watch vehicles swerve around them!

## 🏃 How to Run the Simulation

### Start Fresh
```bash
python3 indian_road_sim.py
```

### What You'll See
- SUMO GUI opens automatically
- 400 vehicles spawn gradually (5 second intervals)
- Vehicles slow down drastically when hitting potholes
- Vehicles change lanes to avoid barricades
- Motorcycles and autos drive aggressively
- Buses stay slow and steady

## 📊 Live Simulation Stats

### During Simulation
- **Top menu**: Shows simulation time
- **Status bar**: Shows number of vehicles running
- **Right panel**: Click vehicle for individual stats

### Vehicle Behavior to Watch
1. **Potholes**: Vehicles suddenly slow to ~1% speed (almost stopped)
2. **Barricades**: Vehicles switch lanes when approaching
3. **Overtaking**: Autos and motorcycles frequently change lanes
4. **Lane Weaving**: Motorcycles zigzag through traffic
5. **Speed Variation**: Motorcycles have erratic speeds

## 🎮 Keyboard Shortcuts

- **Space**: Pause/Resume
- **S**: Step forward one timestep
- **A**: Toggle auto-run
- **L**: Show/Hide lane numbers
- **T**: Track selected vehicle
- **ESC**: Stop tracking
- **Ctrl+A**: Select all vehicles
- **Ctrl+I**: Show vehicle info panel
- **F9**: Open visualization settings
- **Home**: Recenter view

## 🔧 Simulation Details

### Files Created
- `mymap.net.xml` - Road network
- `mymap.poly.xml` - Building polygons
- `mymap.rou.xml` - Vehicle routes
- `mymap.add.xml` - Barricades & potholes
- `mymap.sumocfg` - SUMO configuration
- `mymap.settings.xml` - GUI visualization settings

### Current Settings
- **Simulation time**: 1 hour (3600 seconds)
- **Vehicle spawn**: Every 5 seconds
- **Pothole speed reduction**: 99% (0.01x speed)
- **Vehicle exaggeration**: 2x size (easier to see)

## 🐛 Troubleshooting

### "I don't see vehicle speeds"
- Right-click vehicle → Show Parameter
- Or enable "Show vehicle name" in visualization settings

### "Potholes aren't slowing vehicles"
- They are! Watch the speed color change to dark red/purple
- Right-click vehicle in pothole area to see speed drop

### "I don't see barricades"
- Look for yellow rectangles with black stripes
- Zoom in closer
- Only 4 barricades created (to avoid overwhelming the map)

### "Too many vehicles/lag"
- Edit `indian_road_sim.py`
- Change line: `("auto", 100),` to `("auto", 50),`
- Reduce all vehicle counts

## 📈 Next Steps

To modify the simulation:
1. Edit `indian_road_sim.py`
2. Change vehicle counts (line ~200)
3. Adjust pothole count (line ~100)
4. Modify speed reduction (line ~160: `* 0.01` = 99% reduction)
5. Re-run: `python3 indian_road_sim.py`
