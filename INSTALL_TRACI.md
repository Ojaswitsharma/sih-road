# Installing TraCI for SUMO Simulation

## Quick Install

```bash
pip install traci
```

## If That Doesn't Work

TraCI is part of SUMO, so you can also use it from SUMO_HOME:

```bash
# Add SUMO tools to Python path
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

Or install from SUMO directly:

```bash
# If you have SUMO installed
pip install $SUMO_HOME/tools
```

## Verify Installation

```python
python3 -c "import traci; print('TraCI installed successfully!')"
```

## About SUMO GUI in Streamlit

**Important:** SUMO GUI **cannot** be embedded directly in the Streamlit web interface due to browser security restrictions. 

### Why?

- SUMO GUI is a native desktop application (not web-based)
- Browsers cannot embed native applications for security reasons
- The SUMO window will open **separately** from your browser

### What You'll See

1. **In Streamlit (browser):** Configuration controls and status
2. **Separate window:** SUMO GUI showing the actual simulation

### Alternative: Headless Mode (Future Enhancement)

If you want simulation data in Streamlit without the GUI:

1. Run SUMO in headless mode (no GUI)
2. Collect data via TraCI
3. Display results/charts in Streamlit

This would require modifying `pothole_controller.py` to:
- Use `sumo` instead of `sumo-gui`
- Collect statistics during simulation
- Return data to Streamlit for visualization

## Troubleshooting

### "ModuleNotFoundError: No module named 'traci'"

**Solution 1:** Install via pip
```bash
pip install traci
```

**Solution 2:** Use SUMO's built-in TraCI
```bash
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
```

**Solution 3:** Install in virtual environment
```bash
source venv/bin/activate
pip install traci
```

### "SUMO_HOME not set"

```bash
export SUMO_HOME=/usr/share/sumo
# Add to ~/.bashrc to make permanent
echo 'export SUMO_HOME=/usr/share/sumo' >> ~/.bashrc
```

### "Can't see SUMO window"

The SUMO GUI opens in a **separate window**:
- Check your taskbar/dock
- Look for "SUMO" in window titles
- It may be behind your browser window
- Try Alt+Tab (Windows/Linux) or Cmd+Tab (Mac)

### "Simulation doesn't start"

1. Check that files were generated successfully
2. Verify TraCI is installed: `python3 -c "import traci"`
3. Check console output for errors
4. Ensure SUMO is installed: `which sumo-gui`

## Complete Setup Checklist

- [ ] SUMO installed (`sudo apt-get install sumo sumo-tools`)
- [ ] SUMO_HOME set (`export SUMO_HOME=/usr/share/sumo`)
- [ ] TraCI installed (`pip install traci`)
- [ ] Streamlit installed (`pip install streamlit`)
- [ ] OSM file exists (`mymap.osm`)
- [ ] Run Streamlit app (`streamlit run streamlit_app.py`)

## Running the Simulation

1. **Start Streamlit:** `streamlit run streamlit_app.py`
2. **Configure parameters** in the sidebar
3. **Generate files** - Click "Generate Simulation Files"
4. **Install TraCI** if prompted
5. **Run simulation** - Click "Run Simulation"
6. **Look for SUMO window** - It opens separately!

## Expected Behavior

```
Browser (Streamlit)          Desktop (SUMO GUI)
┌─────────────────┐         ┌─────────────────┐
│ • Sliders       │         │ • Road network  │
│ • Buttons       │         │ • Moving cars   │
│ • Status        │  ←→     │ • Potholes      │
│ • Logs          │         │ • Animation     │
└─────────────────┘         └─────────────────┘
```

Both windows work together:
- **Streamlit:** Control and configuration
- **SUMO GUI:** Visual simulation

This is **normal and expected** - they cannot be combined due to technical limitations.
