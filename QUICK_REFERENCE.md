# 🚀 Quick Reference Card

## Start the App

```bash
./run_streamlit.sh
```
or
```bash
streamlit run streamlit_app.py
```

Opens at: **http://localhost:8501**

---

## Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| **Potholes per road** | 1-10 | 6 | More = denser potholes |
| **Vehicles per class** | 10-200 | 30 | More = heavier traffic |
| **Simulation time** | 300-7200s | 3600s | Longer = more data |
| **Spawn interval** | 1-30s | 5s | Lower = denser traffic |

---

## Workflow

1. **Adjust sliders** → Set your parameters
2. **Click "Generate"** → Creates SUMO files
3. **Click "Run"** → Launches simulation
4. **Watch SUMO GUI** → See vehicles and potholes
5. **Close SUMO** → Stop simulation

---

## What You See

### In Browser (Streamlit)
- 🎛️ Parameter controls
- 📊 Current configuration
- ✅ Status messages
- 📝 Simulation info

### In SUMO Window
- 🟣 **Purple circles** = Potholes
- 🛺 **Yellow** = Auto-rickshaws
- 🏍️ **Red** = Motorbikes
- 🚗 **Cyan** = Cars
- 🚌 **Blue** = Buses

### In Console
```
Vehicle hit pothole → Speed drops 99%
After 5 seconds → Speed recovers
```

---

## Quick Configs

### Light Test (Fast)
- Potholes: **3**
- Vehicles: **20**
- Time: **600s** (10 min)
- Interval: **10s**

### Standard (Default)
- Potholes: **6**
- Vehicles: **30**
- Time: **3600s** (1 hour)
- Interval: **5s**

### Heavy (Stress Test)
- Potholes: **10**
- Vehicles: **100**
- Time: **7200s** (2 hours)
- Interval: **2s**

---

## Keyboard Shortcuts (SUMO GUI)

| Key | Action |
|-----|--------|
| **Space** | Pause/Resume |
| **+/-** | Zoom in/out |
| **Mouse wheel** | Zoom |
| **Right-click vehicle** | Show info |
| **Ctrl+Q** | Quit |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **SUMO not found** | `sudo apt-get install sumo sumo-tools` |
| **Streamlit not found** | `pip install streamlit` |
| **Port in use** | `streamlit run streamlit_app.py --server.port 8502` |
| **OSM missing** | Ensure `mymap.osm` exists |
| **Can't generate** | Check console for errors |

---

## Files Generated

- `mymap.net.xml` - Road network
- `mymap.rou.xml` - Vehicle routes
- `mymap.obstacles.xml` - Potholes
- `mymap.sumocfg` - Configuration
- `mymap.poly.xml` - Polygons

---

## Tips

✅ Start with defaults first
✅ Increase parameters gradually
✅ Watch console for pothole hits
✅ Zoom in to see potholes
✅ Right-click vehicles for details

---

## Documentation

- **STREAMLIT_QUICKSTART.md** - Getting started
- **STREAMLIT_README.md** - Full documentation
- **STREAMLIT_ARCHITECTURE.md** - Technical details
- **BEFORE_AFTER_COMPARISON.md** - Why Streamlit?

---

## Support

1. Check error messages in UI
2. Look at console output
3. Verify SUMO_HOME is set
4. Read documentation files

---

## One-Liner Summary

**Drag sliders → Click Generate → Click Run → Watch simulation! 🚗💨**
