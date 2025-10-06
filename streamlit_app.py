#!/usr/bin/env python3
"""
Streamlit App for Indian Road Pothole Simulation
Allows users to configure and run SUMO simulations with custom parameters
"""

import streamlit as st
import subprocess
import os
import sys
import time
import threading
import xml.etree.ElementTree as ET
import random
import math

# ============================================================================
# FUNCTION DEFINITIONS (Must be defined before use)
# ============================================================================

def generate_vehicle_types(vtypes_file):
    """Generate vehicle type definitions"""
    with open(vtypes_file, "w") as f:
        f.write("""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <vType id="auto" accel="1.8" decel="4.5" sigma="0.7" length="3.0" minGap="1.2" 
           maxSpeed="13.89" color="1,1,0" vClass="passenger" guiShape="delivery" 
           speedFactor="0.95" speedDev="0.25"/>
    
    <vType id="motorbike" accel="4.0" decel="7.0" sigma="0.8" length="2.0" minGap="0.5" 
           maxSpeed="27.78" color="1,0,0" vClass="passenger" guiShape="motorcycle"
           speedFactor="1.3" speedDev="0.4"/>
    
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.5" 
           maxSpeed="33.33" color="0.9,0.9,0.9" vClass="passenger" guiShape="passenger"
           speedFactor="1.05" speedDev="0.2"/>
    
    <vType id="bus" accel="1.2" decel="3.5" sigma="0.3" length="12.0" minGap="3.5" 
           maxSpeed="22.22" color="0,0,1" vClass="passenger" guiShape="bus"
           speedFactor="0.9" speedDev="0.1"/>
</routes>""")


def generate_potholes(net_file, obstacles_file, potholes_per_road):
    """Generate pothole obstacles"""
    tree = ET.parse(net_file)
    root = tree.getroot()
    edges = [edge for edge in root.findall('.//edge') if edge.get('function') != 'internal']
    
    # Get main roads
    main_roads = []
    for edge in edges:
        lanes = edge.findall('lane')
        if lanes:
            num_lanes = len(lanes)
            speed_limit = float(lanes[0].get('speed', '13.89'))
            if num_lanes >= 2 or speed_limit > 16.0:
                main_roads.append(edge)
    
    pothole_id = 0
    edge_positions = {}
    
    with open(obstacles_file, "w") as f:
        f.write('<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n')
        
        for edge in main_roads:
            edge_id = edge.get('id')
            lanes = edge.findall('lane')
            if not lanes:
                continue
            
            lane = lanes[0]
            length = float(lane.get('length', '50'))
            shape = lane.get('shape')
            
            if not shape or length < 30:
                continue
            
            coords = shape.split()
            num_potholes = min(potholes_per_road, max(2, int(length / 60)))
            edge_positions[edge_id] = []
            
            for p in range(num_potholes):
                attempts = 0
                pos_ratio = None
                
                while attempts < 50:
                    test_ratio = random.uniform(0.2, 0.8)
                    test_pos = length * test_ratio
                    
                    too_close = False
                    for existing_pos in edge_positions[edge_id]:
                        if abs(test_pos - existing_pos) < 60:
                            too_close = True
                            break
                    
                    if not too_close:
                        pos_ratio = test_ratio
                        edge_positions[edge_id].append(test_pos)
                        break
                    
                    attempts += 1
                
                if pos_ratio is None:
                    continue
                
                pos_idx = int(len(coords) * pos_ratio)
                if pos_idx >= len(coords):
                    pos_idx = len(coords) - 1
                
                point = coords[pos_idx]
                x, y = map(float, point.split(','))
                
                # Create circular pothole
                size = random.uniform(0.8, 1.5)
                points = []
                for angle_step in range(12):
                    angle = angle_step * 360 / 12
                    rad = math.radians(angle)
                    px = x + size * math.cos(rad)
                    py = y + size * math.sin(rad)
                    points.append(f"{px:.2f},{py:.2f}")
                
                poly_shape = " ".join(points)
                f.write(f'    <poly id="pothole_{pothole_id}" type="pothole_deep_purple" color="0.5,0,0.5" fill="1" layer="10" shape="{poly_shape}"/>\n')
                
                pos = length * pos_ratio
                f.write(f'    <!-- Pothole {pothole_id}: type=deep_purple, speed_mult=0.01, pos={pos:.2f} -->\n')
                
                pothole_id += 1
        
        f.write('</additional>')
    
    return pothole_id


def generate_trips(net_file, trips_file, vehicles_per_class, simulation_time, spawn_interval):
    """Generate vehicle trips/flows"""
    tree = ET.parse(net_file)
    root = tree.getroot()
    
    # Get suitable edges
    suitable_edges = []
    for edge in root.findall('.//edge'):
        edge_id = edge.get('id')
        if edge_id and not edge_id.startswith(':'):
            lanes = edge.findall('lane')
            if len(lanes) >= 2:
                for lane in lanes:
                    allow = lane.get('allow', '')
                    disallow = lane.get('disallow', '')
                    if 'passenger' in allow or (not disallow or 'passenger' not in disallow):
                        suitable_edges.append(edge_id)
                        break
    
    with open(trips_file, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')
        
        # Add vehicle types
        f.write("""
    <vType id="auto" accel="1.8" decel="4.5" sigma="0.7" length="3.0" minGap="1.2" 
           maxSpeed="13.89" color="1,1,0" vClass="passenger" guiShape="delivery"/>
    <vType id="motorbike" accel="3.5" decel="6.0" sigma="0.6" length="2.0" minGap="0.5" 
           maxSpeed="27.78" color="1,0,0" vClass="passenger" guiShape="motorcycle"/>
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.5" 
           maxSpeed="33.33" color="0,0.9,0.9" vClass="passenger" guiShape="passenger"/>
    <vType id="bus" accel="1.2" decel="3.5" sigma="0.3" length="12.0" minGap="3.5" 
           maxSpeed="22.22" color="0,0,1" vClass="passenger" guiShape="bus"/>
""")
        
        # Generate individual trips (not flows) for consistent numbering
        vehicle_id = 0
        vehicle_types = ["auto", "motorbike", "car", "bus"]
        
        for vtype in vehicle_types:
            # Calculate spawn times evenly distributed across simulation time
            for veh_num in range(vehicles_per_class):
                from_edge = random.choice(suitable_edges)
                to_edge = random.choice(suitable_edges)
                
                attempts = 0
                while to_edge == from_edge and attempts < 10:
                    to_edge = random.choice(suitable_edges)
                    attempts += 1
                
                # Distribute vehicles evenly across simulation time
                if vehicles_per_class > 1:
                    depart_time = (veh_num * simulation_time) / vehicles_per_class
                else:
                    depart_time = 0
                
                # Create trip (duarouter will convert to vehicle with route)
                f.write(f'    <trip id="{vtype}_{veh_num}" type="{vtype}" depart="{depart_time:.1f}" from="{from_edge}" to="{to_edge}" departLane="best" departSpeed="max"/>\n')
                vehicle_id += 1
        
        f.write('</routes>\n')


def generate_gui_settings(gui_settings_file):
    """Generate GUI visualization settings"""
    with open(gui_settings_file, "w") as f:
        f.write("""<viewsettings>
    <scheme name="indian_roads">
        <background backgroundColor="0.85,0.9,0.85" showGrid="0"/>
        <vehicles vehicleQuality="3" vehicleSize.minSize="2.5" vehicleSize.exaggeration="2.0"
                 vehicleName.show="1" vehicleShape.show="1"/>
        <additionals addSize.exaggeration="2.5"/>
        <polys polySize.minSize="2" polySize.exaggeration="2.5" polyName.show="1"/>
    </scheme>
</viewsettings>""")


def generate_sumo_config(sumocfg_file, net_file, rou_file, poly_file, 
                        obstacles_file, gui_settings_file, simulation_time):
    """Generate SUMO configuration file"""
    with open(sumocfg_file, "w") as f:
        f.write(f"""<configuration>
    <input>
        <net-file value="{net_file}"/>
        <route-files value="{rou_file}"/>
        <additional-files value="{poly_file},{obstacles_file}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="{simulation_time}"/>
        <step-length value="0.1"/>
    </time>
    <processing>
        <collision.action value="warn"/>
        <time-to-teleport value="-1"/>
        <ignore-route-errors value="true"/>
    </processing>
    <gui_only>
        <gui-settings-file value="{gui_settings_file}"/>
        <start value="true"/>
        <quit-on-end value="false"/>
        <window-size value="1400,900"/>
    </gui_only>
</configuration>""")


def generate_simulation_files(potholes_per_road, vehicles_per_class, simulation_time, spawn_interval):
    """Generate all SUMO simulation files with custom parameters"""
    
    # File paths
    osm_file = "mymap.osm"
    net_file = "mymap.net.xml"
    poly_file = "mymap.poly.xml"
    trips_file = "mymap.trips.xml"
    rou_file = "mymap.rou.xml"
    sumocfg_file = "mymap.sumocfg"
    vtypes_file = "mymap.vtypes.xml"
    obstacles_file = "mymap.obstacles.xml"
    gui_settings_file = "mymap.gui.xml"
    
    SUMO_HOME = os.environ.get("SUMO_HOME", "/usr/share/sumo")
    
    # Check if OSM file exists
    if not os.path.exists(osm_file):
        st.error(f"❌ OSM file '{osm_file}' not found. Please ensure it exists.")
        return False
    
    try:
        # 1. Convert OSM to SUMO network
        st.write("📍 Converting OSM to SUMO network...")
        subprocess.run([
            "netconvert",
            "--osm-files", osm_file,
            "--output-file", net_file,
            "--geometry.remove",
            "--ramps.guess",
            "--junctions.join",
            "--tls.guess-signals",
            "--tls.discard-simple",
            "--tls.join",
            "--default.lanewidth", "3.5",
            "--default.lanenumber", "2",
            "--default.speed", "13.89"
        ], check=True, capture_output=True)
        
        # 2. Generate polygons
        st.write("🗺️ Generating polygons...")
        subprocess.run([
            "polyconvert",
            "--osm-files", osm_file,
            "--net-file", net_file,
            "--type-file", os.path.join(SUMO_HOME, "data/typemap/osmPolyconvert.typ.xml"),
            "-o", poly_file
        ], check=True, capture_output=True)
        
        # 3. Generate vehicle types
        st.write("🚗 Generating vehicle types...")
        generate_vehicle_types(vtypes_file)
        
        # 4. Generate potholes
        st.write(f"🕳️ Generating {potholes_per_road} potholes per road...")
        pothole_count = generate_potholes(net_file, obstacles_file, potholes_per_road)
        st.write(f"   Created {pothole_count} potholes")
        
        # 5. Generate trips
        st.write(f"🚦 Generating vehicle flows ({vehicles_per_class} per class)...")
        generate_trips(net_file, trips_file, vehicles_per_class, simulation_time, spawn_interval)
        
        # 6. Convert trips to routes
        st.write("🛣️ Converting trips to routes...")
        subprocess.run([
            "duarouter",
            "--net-file", net_file,
            "--route-files", trips_file,
            "--output-file", rou_file,
            "--ignore-errors",
            "--repair",
            "--remove-loops",
            "--no-warnings"
        ], check=True, capture_output=True)
        
        # 7. Generate GUI settings
        generate_gui_settings(gui_settings_file)
        
        # 8. Generate SUMO config
        st.write("⚙️ Writing SUMO configuration...")
        generate_sumo_config(sumocfg_file, net_file, rou_file, poly_file, 
                           obstacles_file, gui_settings_file, simulation_time)
        
        return True
        
    except subprocess.CalledProcessError as e:
        st.error(f"❌ Command failed: {e.cmd}")
        st.error(f"Error output: {e.stderr.decode() if e.stderr else 'No error output'}")
        return False
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return False


def run_simulation_background():
    """Run the simulation with pothole controller in background"""
    st.session_state['simulation_running'] = True
    
    def run():
        try:
            # Run with output capture to show in Streamlit
            result = subprocess.run(
                ["python3", "pothole_controller.py"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                st.session_state['simulation_error'] = result.stderr
            else:
                st.session_state['simulation_success'] = True
        except Exception as e:
            st.session_state['simulation_error'] = str(e)
        finally:
            st.session_state['simulation_running'] = False
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


# ============================================================================
# STREAMLIT UI (After all functions are defined)
# ============================================================================

# Page configuration
st.set_page_config(
    page_title="Indian Road Pothole Simulator",
    page_icon="🚗",
    layout="wide"
)

# Initialize session state
if 'files_generated' not in st.session_state:
    st.session_state['files_generated'] = False
if 'simulation_running' not in st.session_state:
    st.session_state['simulation_running'] = False

# Title and description
st.title("🚗 Indian Road Pothole Simulation")
st.markdown("Configure and run SUMO traffic simulations with potholes on Indian roads")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")

# Input parameters
potholes_per_road = st.sidebar.slider(
    "Potholes per Road",
    min_value=1,
    max_value=10,
    value=6,
    help="Number of potholes to generate on each main road"
)

vehicles_per_class = st.sidebar.slider(
    "Vehicles per Class",
    min_value=1,
    max_value=200,
    value=30,
    help="Number of vehicles for each type (auto, motorbike, car, bus)"
)

simulation_time = st.sidebar.slider(
    "Simulation Time (seconds)",
    min_value=300,
    max_value=7200,
    value=3600,
    step=300,
    help="Total simulation duration"
)

spawn_interval = st.sidebar.slider(
    "Spawn Interval (seconds)",
    min_value=1,
    max_value=30,
    value=5,
    help="Time between vehicle spawns"
)

# Display current configuration
st.sidebar.markdown("---")
st.sidebar.subheader("Current Configuration")
st.sidebar.write(f"🕳️ Potholes: {potholes_per_road} per road")
st.sidebar.write(f"🚗 Vehicles: {vehicles_per_class} per class")
st.sidebar.write(f"⏱️ Duration: {simulation_time}s ({simulation_time/60:.1f} min)")
st.sidebar.write(f"🔄 Spawn: Every {spawn_interval}s")
st.sidebar.write(f"📊 Total vehicles: {vehicles_per_class * 4}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Simulation Control")
    
    # Generate simulation button
    if st.button("🔧 Generate Simulation Files", type="primary"):
        with st.spinner("Generating simulation files..."):
            try:
                # Call the generation function
                success = generate_simulation_files(
                    potholes_per_road,
                    vehicles_per_class,
                    simulation_time,
                    spawn_interval
                )
                
                if success:
                    st.success("✅ Simulation files generated successfully!")
                    st.session_state['files_generated'] = True
                else:
                    st.error("❌ Failed to generate simulation files")
                    st.session_state['files_generated'] = False
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state['files_generated'] = False
    
    # Run simulation button (only enabled after generation)
    if st.session_state.get('files_generated', False):
        if st.button("▶️ Run Simulation", type="primary"):
            st.info("🚀 Starting SUMO simulation...")
            st.markdown("""
            **Note:** The SUMO GUI will open in a **separate window** (cannot be embedded in browser).
            
            **If you see "ModuleNotFoundError: No module named 'traci'":**
            ```bash
            pip install traci
            ```
            
            **To see the simulation:**
            1. The SUMO GUI window will open separately
            2. Watch vehicles slow down at potholes (deep purple circles)
            3. Console output shows real-time speed changes
            4. Close the SUMO window to stop
            """)
            
            # Check if traci is installed
            try:
                import traci
                st.success("✅ TraCI module found")
                # Run simulation in background
                run_simulation_background()
            except ImportError:
                st.error("❌ TraCI module not found. Please install it:")
                st.code("pip install traci", language="bash")
                st.info("After installing, click 'Run Simulation' again")
    else:
        st.button("▶️ Run Simulation", disabled=True, help="Generate files first")

with col2:
    st.subheader("Simulation Info")
    
    # Important note about SUMO GUI
    st.warning("""
    ⚠️ **SUMO GUI runs in a separate window**
    
    Browser security prevents embedding native applications.
    The SUMO window will open outside the browser.
    """)
    
    st.markdown("""
    ### Pothole Types
    🟣 **Deep Purple**: 99% speed reduction
    - Vehicles drop to 1% speed instantly
    - Effect lasts 5 seconds
    - Then gradual recovery
    
    ### Vehicle Types
    🛺 **Auto-rickshaw**: Medium speed, agile
    🏍️ **Motorbike**: Fast, erratic
    🚗 **Car**: Average behavior
    🚌 **Bus**: Slow, less maneuverable
    
    ### First Time Setup
    ```bash
    pip install traci
    ```
    """)

# Simulation status area
st.markdown("---")
st.subheader("Simulation Output")

# Show simulation status
if 'simulation_running' in st.session_state and st.session_state['simulation_running']:
    st.info("🔄 Simulation is running... Check the SUMO GUI window (separate window)")
    st.markdown("""
    **Looking for the SUMO window?**
    - Check your taskbar/dock for a new window
    - It may be behind your browser
    - Look for "SUMO" in window titles
    """)
elif 'simulation_error' in st.session_state:
    st.error("❌ Simulation Error:")
    st.code(st.session_state['simulation_error'])
    if 'traci' in st.session_state['simulation_error']:
        st.info("💡 Solution: Install TraCI module")
        st.code("pip install traci", language="bash")
    # Clear error after showing
    del st.session_state['simulation_error']
elif 'simulation_success' in st.session_state and st.session_state['simulation_success']:
    st.success("✅ Simulation completed successfully!")
    del st.session_state['simulation_success']
else:
    st.info("⏸️ No simulation running")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Indian Road Pothole Simulator | Built with Streamlit & SUMO</p>
</div>
""", unsafe_allow_html=True)
