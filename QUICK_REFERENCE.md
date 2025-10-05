# Quick Reference - Indian Road Simulation

## 🎯 Run Simulation
```bash
python3 osm_to_sim.py
```

## 🚗 Vehicle Colors & Characteristics

| Vehicle | Color | Speed | Size | Behavior |
|---------|-------|-------|------|----------|
| **Auto-rickshaw** | 🟡 Yellow | 50 km/h | 3m | Weaves through traffic |
| **Motorcycle** | 🔴 Red | 100 km/h | 2m | Very aggressive |
| **Car** | ⚪ White/Gray | 120 km/h | 5m | Rule-following |
| **Bus/Truck** | 🔵 Blue | 80 km/h | 12m | Stays in lane ✅ NO U-TURNS |

## 🛣️ Road Obstacles

### Visible Potholes 🕳️
- **Colors**: Dark Brown, Gray, Dark Gray, Muddy Brown
- **Shapes**: Circle, Oval, Irregular
- **Size**: 1.5m - 3.5m
- **Count**: 12
- **Effect**: 50% speed reduction

### Barricades 🚧
- **Color**: 🟠 Orange
- **Size**: 4m x 1.6m
- **Count**: 8
- **Type**: Construction zones

### Speed Breakers 🐌
- **Color**: 🟡 Yellow
- **Size**: 6m x 0.8m
- **Count**: 5

### Roadside Obstacles 🛒
- 🟢 Green: Street vendors
- ⚫ Gray: Parked vehicles
- 🟤 Brown: Debris/construction

## 🔧 Key Settings

### Routing (Fixed U-turns)
- Minimum trip: **300m**
- Maximum trip: **3000m**
- Algorithm: **A***
- Loop removal: **Enabled**

### Traffic Mix
- 40% Motorcycles
- 30% Cars
- 20% Auto-rickshaws
- 10% Buses/Trucks

### Simulation
- Duration: **1 hour**
- Vehicle spawn: **Every 2 seconds**
- Step length: **0.1s**
- Rerouting: **30% vehicles**

## 👀 How to View in SUMO GUI

### See Potholes
1. Zoom in to road level
2. Look for colored irregular shapes
3. Watch vehicles slow down

### Verify Bus Fix
1. Select blue vehicle
2. Follow its route
3. Should drive straight (min 300m)

### Change View
- **Edit** → **Edit Visualization**
- Load scheme: **indian_roads**

## 📊 What Makes It Indian

✅ 70% two/three-wheelers
✅ Visible potholes on roads
✅ Construction barricades
✅ Speed breakers
✅ Roadside vendors/parking
✅ Aggressive motorcycles
✅ Mixed traffic speeds
✅ Realistic congestion

## 🐛 Quick Fixes

**Can't see potholes?**
→ Zoom in closer, look for brown/gray shapes

**Buses still U-turning?**
→ Check min-distance is 300m in script

**Simulation slow?**
→ Reduce vehicles (increase `-p` to 5)

**No obstacles?**
→ Check mymap.obstacles.xml was generated

## 📁 Generated Files

✅ mymap.vtypes.xml - Vehicle types
✅ mymap.obstacles.xml - All obstacles
✅ mymap.view.xml - Visualization
✅ mymap.sumocfg - Config
✅ mymap.rou.xml - Routes

---

**Enjoy your realistic Indian road simulation! 🇮🇳**
