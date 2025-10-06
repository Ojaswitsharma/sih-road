# 🚗 Indian Road Simulation - Quick Reference

## Run Simulation
```bash
python3 indian_road_sim.py
```

## See Vehicle Stats (3 Easy Ways)

### 1. Right-Click Method (BEST)
- Right-click any vehicle → **"Show Parameter"**
- See: Type, Speed, Position, Lane, Route, etc.

### 2. Enable Names
- Press **F9**
- Vehicles tab → Check **"Show vehicle name"**
- Increase text size to 60-100

### 3. Color by Speed
- Press **F9**
- Vehicles tab → **"Color vehicles by: speed"**
- Red = Slow/Stopped (in potholes!)
- Green = Fast

## What You Have Now

✅ **400 Vehicles** (100 each)
- 🛺 Yellow Autos (rash, overtaking)
- 🏍️ Red Motorcycles (erratic, fast)
- 🚗 Gray Cars (normal)
- 🚌 Blue Buses (slow, stable)

✅ **5,892 Potholes** 
- Dark gray color
- **99% speed reduction** (vehicles almost stop!)
- All lanes affected

✅ **4 Barricades**
- Yellow with black stripes
- Block lanes → vehicles must change lanes

## Keyboard Shortcuts
- **Space** = Pause/Resume
- **F9** = Visualization settings
- **T** = Track vehicle (select first)
- **L** = Show lane numbers
- **Home** = Recenter view
- **ESC** = Stop tracking

## Watch For
1. **Potholes**: Vehicles turn dark red and almost stop
2. **Lane Changes**: Motorcycles zigzag constantly
3. **Overtaking**: Autos frequently switch lanes
4. **Barricades**: Vehicles swerve around yellow blocks

## Stats Display Location
- **Right-click vehicle** → Bottom panel shows live stats
- **Track vehicle** → Camera follows + live stats
- **Vehicle name** → Shows ID above vehicle
