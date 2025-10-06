# 🚗 HOW TO USE THE SIMPLE POTHOLE AVOIDANCE

## Quick Start

```bash
# Run the simulation with GUI
python3 simple_pothole_avoidance.py
```

That's it! The SUMO GUI will open and you'll see:
- **4 vehicle types**: bus (blue), car (cyan), motorbike (red), auto (yellow)
- **Purple potholes**: Small circles on the road
- **Dodging behavior**: Vehicles move laterally to avoid potholes
- **Console output**: Real-time status messages

## What to Watch For

### In the SUMO GUI:
1. **Vehicles approaching potholes** - they slow down
2. **Lateral movement** - vehicles shift left/right to dodge
3. **Hits** - vehicle stops at pothole (purple circle), very slow for 5 seconds
4. **Recovery** - vehicle speeds back up and returns to center

### In the Console:
```
[bus_flow_16.0] ↓ SLOWING for pothole 45.2m ahead
[bus_flow_16.0] ↔ DODGING LEFT (offset: -1.5m) for pothole 32.1m ahead
[bus_flow_16.0] ← Passed pothole, returning to center
[bus_flow_16.0] → Returned to center, resuming normal driving
```

OR if dodge fails:
```
[car_flow_13.0] ↓ SLOWING for pothole 28.3m ahead (can't dodge either way)
[car_flow_13.0] ✗ HIT POTHOLE at (5609.4, 5524.1) - 99% speed loss for 5 seconds!
[car_flow_13.0] ✓ RECOVERED from pothole hit
```

## Files

- **simple_pothole_avoidance.py** - Main controller
- **mymap_few_potholes.obstacles.xml** - 200 potholes (realistic density)
- **mymap.sumocfg** - SUMO configuration
- **mymap.net.xml** - Road network
- **mymap.rou.xml** - 4 vehicle types

## How It Works

1. **Detect**: Scan 80m ahead for potholes
2. **Slow**: Start slowing at 60m
3. **Dodge**: At 40m, move laterally ±1.5m if safe
4. **Return**: After passing, return to center
5. **Hit**: If unavoidable, 99% speed loss for 5 seconds

## The Indian Road Magic ✨

- **Tight lanes**: 3.5m wide, vehicles dodge 1.5m (leaving 0.2m buffer!)
- **Aggressive**: Tries both left AND right dodging
- **Quick**: Dodges even at last moment (2m ahead!)
- **Realistic**: 99% speed loss on hit, 5-second recovery

## Troubleshooting

**No dodging seen?**
- Check console for "DODGING" messages
- Potholes might be unavoidable (too many nearby)
- Try running longer (more vehicles = more dodge attempts)

**Vehicles still hitting?**
- Some hits are unavoidable (clustered potholes)
- This is realistic - not all potholes can be dodged!
- Watch for successful dodges between hits

**GUI not opening?**
- Make sure SUMO is installed: `sumo-gui --version`
- Set SUMO_HOME: `export SUMO_HOME=/usr/share/sumo`
- Check the simulation uses mymap_few_potholes.obstacles.xml (200 potholes)

## Why This Works (vs Previous Attempts)

❌ **Old approach**:
- 1571 potholes (impossible to avoid)
- moveToXY() broken (0.00m movement)
- 3.5m dodge offset (exceeds 3.5m lanes!)
- Complex 381-line controller

✅ **New approach**:
- 200 potholes (realistic density)
- setLateralLanePosition() (WORKS!)
- 1.5m dodge offset (fits 3.5m lanes)
- Simple 400-line controller

---

**Read FINAL_SOLUTION.md for complete technical details!**
