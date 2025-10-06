# How to View Vehicle Stats in SUMO GUI

## Vehicle Speed and Stats Display

After running the simulation, follow these steps IN THE SUMO GUI to see vehicle speeds:

### Method 1: Enable Speed Display in Visualization Settings
1. **Open SUMO GUI** (it should open automatically)
2. **Go to Edit → Edit Visualization**
3. **Click on "Vehicles" tab**
4. **Check the following boxes:**
   - ☑ "Show vehicle name"
   - ☑ "Show vehicle as"
   - ☑ "Show vehicle text parameter"
5. **In "vehicle text parameter" field, type:** `speed`
6. **Adjust "Size" sliders:**
   - Vehicle size: 3.0
   - Text size: 70-100
7. **Click "OK"**

### Method 2: Right-Click Individual Vehicles
1. **Right-click on any vehicle** in the simulation
2. **Select "Show Parameter"**
3. You'll see a window with:
   - Current speed (km/h)
   - Position
   - Acceleration
   - Route info
   - Waiting time
   - CO2 emissions

### Method 3: Vehicle Selection
1. **Right-click a vehicle** → **"Select Transport"**
2. The vehicle will be highlighted
3. **Bottom panel shows real-time stats:**
   - Speed
   - Position
   - Lane
   - Route progress

### Method 4: Color Vehicles by Speed
1. **Edit → Edit Visualization**
2. **Vehicles tab**
3. **Color vehicles by:** Dropdown → Select **"speed"**
4. Vehicles will change color based on their current speed:
   - **Red** = Stopped/Very slow
   - **Yellow** = Medium speed
   - **Green** = Fast/Maximum speed

## Current Simulation Stats

### Vehicles
- **120 total vehicles** (30 of each type)
  - 30 Auto-rickshaws (Yellow)
  - 30 Motorcycles (Red)
  - 30 Cars (White/Gray)
  - 30 Buses/Trucks (Blue)

### Obstacles
- **3,000-5,000 potholes** (15-25 per road, 200 roads)
  - 70% Small (0.3-1.0m)
  - 20% Medium (1.0-2.5m)
  - 10% Large (2.5-5.0m)
  - Speed reduction: 30% of normal speed
  - **Spread across ALL lanes** (vehicles can't avoid them)

- **50 Barricades** (Yellow-black striped)
- **20 Speed Breakers** (Orange)
- **30 Roadside Obstacles** (Vendors, debris)

### Speed Behavior
When vehicles hit potholes, you'll see:
- **Speed drops to 30%** of their normal speed
- **Visible in real-time** if you enable speed display
- **All lanes affected** - no way to avoid potholes

### Vehicle Stats Available
For each vehicle, you can track:
- **Speed** (current km/h)
- **Acceleration** (m/s²)
- **Position** (x, y coordinates)
- **Waiting time** (seconds)
- **Time loss** (total delay)
- **CO2 emissions** (mg)
- **Route completion** (%)

## Quick Access Commands
- **Space**: Pause/Resume simulation
- **S**: Step forward one frame
- **T**: Track vehicle (select vehicle first)
- **L**: Show/Hide vehicle routes
- **Ctrl + I**: Show vehicle info panel
