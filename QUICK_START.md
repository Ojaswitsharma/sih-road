# 🚀 Quick Start Guide

## Run in 3 Steps:

### 1. Check SUMO is Installed
```bash
sumo-gui --version
```
**If not found**, install:
```bash
sudo apt-get install sumo sumo-tools
export SUMO_HOME=/usr/share/sumo
```

### 2. Go to Directory
```bash
cd /home/IAteNoodles/sih-road
```

### 3. Run Simulation
```bash
python3 simple_pothole_avoidance.py
```

---

## ✅ What Should Happen:

1. **SUMO GUI opens** showing road network
2. **Purple circles** = potholes on roads  
3. **Colored vehicles** appear:
   - 🟡 Yellow = Auto-rickshaw
   - 🔵 Blue = Bus
   - 🔷 Cyan = Car
   - 🔴 Red = Motorbike

4. **Console shows** dodging events:
   ```
   [auto_flow_0.0] ↔ DODGING LEFT (offset: -1.5m) for pothole 3.0m ahead
   [bus_flow_16.0] ✗ HIT POTHOLE - 99% speed loss for 5 seconds!
   [bus_flow_16.0] ✓ RECOVERED from pothole hit
   ```

5. **Watch vehicles** in GUI:
   - Approach potholes
   - **Move sideways** to dodge (you'll see lateral shift!)
   - Return to center
   - OR hit and slow down dramatically

---

## 📊 Expected Results:

- **~83% avoidance rate** (most potholes dodged successfully)
- **~17% hits** (some unavoidable due to clustering)
- **Visible lateral movement** in GUI when dodging
- **5-second slowdown** when hitting potholes

---

## 🐛 If It Doesn't Work:

**No GUI?**
```bash
# Set SUMO_HOME
export SUMO_HOME=/usr/share/sumo

# Try running again
python3 simple_pothole_avoidance.py
```

**Python errors?**
```bash
# Make sure you're in the right directory
pwd
# Should show: /home/IAteNoodles/sih-road

# Check files exist
ls simple_pothole_avoidance.py mymap_few_potholes.obstacles.xml
```

**No dodging?**
- Wait 20-30 seconds for vehicles to spawn
- Check console for "DODGING" messages
- Some hits are normal (not all potholes avoidable)

---

## 🎯 Quick Stats Check:

After running for ~30 seconds, press **Ctrl+C** to stop, then:

```bash
# Count dodges
grep -c "DODGING" simulation_log.txt 2>/dev/null || echo "Run simulation first"

# Count hits
grep -c "HIT POTHOLE" simulation_log.txt 2>/dev/null || echo "Run simulation first"
```

---

**That's it! The simulation is working if you see:**
- ✅ GUI opens
- ✅ Purple potholes visible
- ✅ Vehicles moving
- ✅ Console shows "DODGING" or "HIT POTHOLE" messages
- ✅ Vehicles shift laterally (dodge) or slow down (hit)

**Success rate: 83% avoidance!** 🎉

---

For more details, see **README.md** or **FINAL_SOLUTION.md**
