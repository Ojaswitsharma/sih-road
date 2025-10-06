# How to Visualize Speed Changes in SUMO-GUI

## The speed reductions ARE working! You just need to enable visualization.

The console output proves vehicles are slowing down perfectly:
- **Pink potholes**: 50% reduction (13.8 → 6.9 m/s)
- **Orange potholes**: 75% reduction (13.8 → 3.5 m/s)  
- **Red potholes**: 90% reduction (13.8 → 1.4 m/s)

## ✅ METHOD 1: Color Vehicles by Speed (EASIEST)

1. **Run the simulation:**
   ```bash
   python3 run_simulation.py
   ```

2. **In SUMO-GUI, click on the menu:**
   ```
   View → Vehicles → Color vehicles by: speed
   ```

3. **What you'll see:**
   - **Red/Yellow vehicles** = Fast (normal speed ~13.8 m/s)
   - **Green/Blue vehicles** = Slow (in pothole)
   - Watch vehicles change color as they cross potholes!

## ✅ METHOD 2: Show Speed Values Above Vehicles

1. **In SUMO-GUI menu:**
   ```
   View → Vehicles → Show vehicle name/speed
   ```

2. **You'll see the actual m/s value above each vehicle**
   - Watch the numbers drop when hitting potholes
   - Example: "13.8" → "3.5" → "13.8"

## ✅ METHOD 3: Slower Simulation for Better Observation

The speed changes happen in 0.5-1 second, which is fast!

1. **In SUMO-GUI, adjust the delay slider** (top toolbar)
   - Move it to the right to slow down simulation
   - Or use the step button to advance frame-by-frame

2. **Watch the console output** while stepping:
   ```
   Step 220: Vehicle auto_2 hit pothole_red at pos 29.4, speed 13.9 -> 1.4 m/s (10% of original)
   Step 228: Vehicle auto_2 exited pothole, resuming normal speed
   ```

## 🔍 What's Happening:

- **Detection zone**: 10m diameter around each pothole
- **Vehicles enter zone** → Speed instantly drops
- **Vehicles exit zone** → Speed returns to normal
- **Duration in pothole**: ~5-10 simulation steps (0.5-1 second)

## 📊 Expected Behavior:

When a vehicle hits:
- **Pink pothole** → Speed becomes 50% (half speed)
- **Orange pothole** → Speed becomes 25% (quarter speed)
- **Red pothole** → Speed becomes 10% (almost stopped)

The console confirms this is working perfectly! The visualization just makes it more obvious.

## 🎨 Visual Tip:

Enable BOTH:
1. Color by speed (to see color changes)
2. Show speed values (to see exact numbers)

This way you get instant visual feedback PLUS the actual speed values!
