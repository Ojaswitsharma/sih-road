import os
import subprocess
import xml.etree.ElementTree as ET
import random
import math

# --- SETTINGS ---
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

# Simulation parameters
SIMULATION_TIME = 7200  # 2 hours for longer simulation
NUM_VEHICLES_PER_TYPE = 100  # Increased from 25 to 100
POTHOLES_PER_ROAD = 6  # Increased from 4
POTHOLE_ZONE_LENGTH = 8  # meters (increased from 5)
DEPARTURE_INTERVAL = 5  # seconds between vehicle spawns (reduced from 10)
r
# --- 1. Convert OSM to SUMO network ---
print("Converting OSM to SUMO network...")
subprocess.run([
    "netconvert",
    "--osm-files", osm_file,
    "--type-files", os.path.join(SUMO_HOME, "data/typemap/osmNetconvert.typ.xml"),
    "--output-file", net_file,
    "--geometry.remove", "--ramps.guess", "--junctions.join",
    "--tls.guess-signals", "--tls.discard-simple", "--tls.join", "--tls.default-type", "actuated", "-v"
])

# --- 2. Generate polygons (optional) ---
print("Generating polygons...")
subprocess.run([
    "polyconvert",
    "--osm-files", osm_file,
    "--net-file", net_file,
    "--type-file", os.path.join(SUMO_HOME, "data/typemap/osmPolyconvert.typ.xml"),
    "-o", poly_file
])

# --- 2.5. Generate vehicle types with improved Indian road characteristics ---
print("Generating vehicle types...")
with open(vtypes_file, "w") as f:
    f.write(f"""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <!-- Auto-rickshaw: overtakes, medium distance, medium speed -->
    <vType id="auto" accel="1.8" decel="4.5" sigma="0.7" length="3.0" minGap="1.2" 
           maxSpeed="13.89" color="1,1,0" vClass="passenger" guiShape="delivery" 
           speedFactor="0.95" speedDev="0.25" lcStrategic="2.0" lcCooperative="0.4"
           lcSpeedGain="2.5" lcKeepRight="0.2" lcAssertive="1.5"/>
    
    <!-- Motorbike: erratic speed, frequent lane changes, short distance, fast -->
    <vType id="motorbike" accel="4.0" decel="7.0" sigma="0.8" length="2.0" minGap="0.5" 
           maxSpeed="27.78" color="1,0,0" vClass="passenger" guiShape="motorcycle"
           speedFactor="1.3" speedDev="0.4" lcStrategic="3.0" lcCooperative="0.2"
           lcSpeedGain="4.0" lcKeepRight="0.1" lcAssertive="2.0" impatience="1.0"/>
    
    <!-- Car: average behavior, long distance -->
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.5" 
           maxSpeed="33.33" color="0.9,0.9,0.9" vClass="passenger" guiShape="passenger"
           speedFactor="1.05" speedDev="0.2" lcStrategic="1.0" lcCooperative="1.0"
           lcSpeedGain="1.0" lcKeepRight="0.5" lcAssertive="1.0"/>
    
    <!-- Bus: slow, long distance, less maneuverable -->
    <vType id="bus" accel="1.2" decel="3.5" sigma="0.3" length="12.0" minGap="3.5" 
           maxSpeed="22.22" color="0,0,1" vClass="passenger" guiShape="bus"
           speedFactor="0.9" speedDev="0.1" lcStrategic="0.5" lcCooperative="1.5"
           lcSpeedGain="0.5" lcKeepRight="0.8" lcAssertive="0.5"/>
</routes>""")

# --- 2.6. Generate potholes by MODIFYING NETWORK LANES directly ---
print("Generating potholes on main roads by modifying lane speeds...")

tree = ET.parse(net_file)
root = tree.getroot()
edges = [edge for edge in root.findall('.//edge') if edge.get('function') != 'internal']

# Get ONLY main roads (multi-lane or high speed)
main_roads = []
for edge in edges:
    if edge.findall('lane'):
        lanes = edge.findall('lane')
        num_lanes = len(lanes)
        lane = lanes[0]
        speed_limit = float(lane.get('speed', '13.89'))
        
        # Main road criteria: 2+ lanes OR speed > 16 m/s
        if num_lanes >= 2 or speed_limit > 16.0:
            main_roads.append(edge)

print(f"Found {len(main_roads)} main roads for potholes")

# Pothole types - we'll create visual polygons only, speed reduction via lane area detectors
pothole_types = [
    ("pink", "1,0.4,0.7", 0.50),    # Pink: 50% speed reduction
    ("orange", "1,0.5,0", 0.25),    # Orange: 75% speed reduction (25% of original)
    ("red", "1,0,0", 0.10)          # Red: 90% speed reduction (10% of original)
]

# Open obstacles file for polygons AND lane area detectors
with open(obstacles_file, "w") as f:
    f.write(f"""<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n""")
    
    pothole_id = 0
    edge_positions = {}
    
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
        
        # 4-6 potholes per main road based on length  
        num_potholes = min(6, max(4, int(length / 60)))
        
        edge_positions[edge_id] = []
        
        for p in range(num_potholes):
            # Find a position that's not too close to other potholes
            attempts = 0
            pos_ratio = None
            
            while attempts < 50:
                test_ratio = random.uniform(0.2, 0.8)
                test_pos = length * test_ratio
                
                # Check minimum 60m spacing between potholes
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
            
            # Get coordinate for visualization
            pos_idx = int(len(coords) * pos_ratio)
            if pos_idx >= len(coords):
                pos_idx = len(coords) - 1
                
            point = coords[pos_idx]
            x, y = map(float, point.split(','))
            
            # Random pothole type with weighted distribution
            ptype_name, ptype_color, speed_multiplier = random.choices(
                pothole_types, 
                weights=[50, 35, 15]  # More pink, fewer red
            )[0]
            
            # Create irregular pothole polygon for visualization
            size = random.uniform(1.2, 3.0)
            points = []
            for angle_step in range(8):
                angle = (angle_step * 360 / 8) + random.uniform(-20, 20)
                rad = math.radians(angle)
                radius = size * random.uniform(0.6, 1.4)
                px = x + radius * math.cos(rad)
                py = y + radius * math.sin(rad)
                points.append(f"{px:.2f},{py:.2f}")
            
            poly_shape = " ".join(points)
            f.write(f"    <poly id=\"pothole_{pothole_id}\" type=\"pothole_{ptype_name}\" color=\"{ptype_color}\" fill=\"1\" layer=\"10\" shape=\"{poly_shape}\"/>\n")
            
            # Store pothole metadata as comment for TraCI controller to read
            pos = length * pos_ratio
            f.write(f"    <!-- Pothole {pothole_id}: type={ptype_name}, speed_mult={speed_multiplier}, pos={pos:.2f} -->\n")
            
            # DO NOT CREATE VSS - it interferes with TraCI control!
            # TraCI controller will handle speed reduction dynamically
            
            pothole_id += 1
    
    print(f"Generated {pothole_id} potholes on main roads (visual only, speed control via TraCI)")
    f.write("</additional>")

# --- 3. Generate trips - USING PROVEN APPROACH FROM osm_to_sim.py ---
print("Generating trips with vehicle types...")

# Get suitable edges for trips - PRIORITIZE MULTI-LANE ROADS FOR BETTER CONNECTIVITY
suitable_trip_edges = []
for edge in root.findall('.//edge'):
    edge_id = edge.get('id')
    # Skip internal edges
    if edge_id and not edge_id.startswith(':'):
        lanes = edge.findall('lane')
        # ONLY use edges with 2+ lanes (main roads are better connected)
        if len(lanes) >= 2:
            # Check if any lane allows passenger vehicles
            for lane in lanes:
                allow = lane.get('allow', '')
                disallow = lane.get('disallow', '')
                # Good edges allow passenger or don't disallow all vehicles
                if 'passenger' in allow or (not disallow or 'passenger' not in disallow):
                    suitable_trip_edges.append(edge_id)
                    break

# Fallback if we don't have enough multi-lane edges
if len(suitable_trip_edges) < 50:
    print(f"Warning: Only {len(suitable_trip_edges)} multi-lane edges, using all suitable edges")
    suitable_trip_edges = []
    for edge in root.findall('.//edge'):
        edge_id = edge.get('id')
        if edge_id and not edge_id.startswith(':'):
            lanes = edge.findall('lane')
            if lanes:
                for lane in lanes:
                    allow = lane.get('allow', '')
                    disallow = lane.get('disallow', '')
                    if 'passenger' in allow or (not disallow or 'passenger' not in disallow):
                        suitable_trip_edges.append(edge_id)
                        break

print(f"Found {len(suitable_trip_edges)} suitable edges for trips")

# Create trips with embedded vehicle type definitions
with open(trips_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')
    
    # Add vehicle type definitions directly in route file
    f.write("""
    <!-- Auto-rickshaw: overtakes, medium distance -->
    <vType id="auto" accel="1.8" decel="4.5" sigma="0.7" length="3.0" minGap="1.2" 
           maxSpeed="13.89" color="1,1,0" vClass="passenger" guiShape="delivery" 
           speedFactor="0.9" speedDev="0.2" lcStrategic="1.5" lcCooperative="0.5"
           lcSpeedGain="2.0" lcKeepRight="0.3"/>
    
    <!-- Motorbike: erratic, lane changes, short distance -->
    <vType id="motorbike" accel="3.5" decel="6.0" sigma="0.6" length="2.0" minGap="0.5" 
           maxSpeed="27.78" color="1,0,0" vClass="passenger" guiShape="motorcycle"
           speedFactor="1.2" speedDev="0.3" lcStrategic="2.0" lcCooperative="0.3"
           lcSpeedGain="3.0" lcKeepRight="0.1"/>
    
    <!-- Car: average, long distance -->
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.5" 
           maxSpeed="33.33" color="0,0.9,0.9" vClass="passenger" guiShape="passenger"
           speedFactor="1.0" speedDev="0.15" lcStrategic="1.0" lcCooperative="1.0"
           lcSpeedGain="1.0" lcKeepRight="0.5"/>
    
    <!-- Bus: slow, long distance (using passenger vClass for routing) -->
    <vType id="bus" accel="1.2" decel="3.5" sigma="0.3" length="12.0" minGap="3.5" 
           maxSpeed="22.22" color="0,0,1" vClass="passenger" guiShape="bus"
           speedFactor="0.85" speedDev="0.1" lcStrategic="0.5" lcCooperative="1.5"
           lcSpeedGain="0.5" lcKeepRight="0.8"/>
    
""")
    
    vehicle_id = 0
    vehicle_types = [
        ("auto", 30),
        ("motorbike", 30),
        ("car", 30),
        ("bus", 30)
    ]
    
    for vtype, count in vehicle_types:
        for i in range(count):
            # Ensure minimum distance between start and end
            attempts = 0
            while attempts < 10:
                from_edge = random.choice(suitable_trip_edges)
                to_edge = random.choice(suitable_trip_edges)
                # Ensure different start and end
                if to_edge != from_edge:
                    break
                attempts += 1
            
            depart_time = vehicle_id * 10  # Stagger departures by 10 seconds
            f.write(f'    <trip id="{vtype}_{i}" type="{vtype}" depart="{depart_time}" from="{from_edge}" to="{to_edge}" departLane="best" departSpeed="max"/>\n')
            vehicle_id += 1
    
    f.write('</routes>\n')

print(f"Created 120 trips (30 of each type)")

# --- 4. Convert trips to routes with robust settings ---
print("Converting trips to routes...")
result = subprocess.run([
    "duarouter",
    "-n", net_file,
    "-t", trips_file,
    "-o", rou_file,
    "--ignore-errors",
    "--repair",
    "--remove-loops",
    "--routing-algorithm", "astar",
    "--weights.random-factor", "1.5",
    "--max-alternatives", "3",
    "--randomize-flows",
    "--no-warnings"
], capture_output=True, text=True)

if result.returncode != 0:
    print(f"Warning: duarouter had issues: {result.stderr}")
else:
    print("Routes generated successfully")
    # Check how many routes were created
    try:
        route_tree = ET.parse(rou_file)
        route_root = route_tree.getroot()
        routes = route_root.findall('.//vehicle')
        print(f"Successfully created {len(routes)} valid routes")
    except Exception as e:
        print(f"Could not count routes: {e}")

# --- 5. Create enhanced GUI settings for better visualization ---
print("Creating GUI settings for better visualization...")
with open(gui_settings_file, "w") as f:
    f.write("""<viewsettings>
    <scheme name="indian_roads">
        <background backgroundColor="0.85,0.9,0.85" showGrid="0"/>
        <edges laneEdgeMode="1" scaleMode="0" laneShowBorders="1" 
               edgeName.show="0" streetName.show="1" edgeData.show="0"
               edgeColorMode="0" edgeWidthMode="0"/>
        <vehicles vehicleQuality="3" vehicleSize.minSize="2.5" vehicleSize.exaggeration="2.0"
                 vehicleName.show="1" vehicleName.size="60" vehicleName.color="0,0,0"
                 vehicleColorMode="0" vehicleShape.show="1"
                 vehicleText.show="1" vehicleText.size="50" vehicleText.color="255,0,0"
                 showBlinker="1" drawMinGap="1" showBTRange="0"
                 showRouteIndex="0" scaleLength="1" drawLaneChangePreference="1"/>
        <persons personQuality="2" personSize.minSize="1" personSize.exaggeration="1"/>
        <junctions junctionMode="1" drawLinkTLIndex="0" drawLinkJunctionIndex="0"
                   junctionName.show="0" internalJunctionName.show="0" tlsPhaseIndex.show="1"/>
        <additionals addMode="0" addSize.exaggeration="2.5" addName.show="1" addFullName.show="1"/>
        <pois poiSize.minSize="1" poiSize.exaggeration="2" poiName.show="0"/>
        <polys polySize.minSize="2" polySize.exaggeration="2.5" polyName.show="1"/>
        <legend showSizeLegend="1"/>
        <opengl antialiase="1" dither="1"/>
    </scheme>
</viewsettings>""")

# --- 6. Write comprehensive SUMO configuration ---
print("Writing SUMO configuration...")
with open(sumocfg_file, "w") as f:
    f.write(f"""<configuration>
    <input>
        <net-file value="{net_file}"/>
        <route-files value="{rou_file}"/>
        <additional-files value="{poly_file},{obstacles_file}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="{SIMULATION_TIME}"/>
        <step-length value="0.1"/>
    </time>
    <processing>
        <collision.action value="warn"/>
        <collision.mingap-factor value="0.1"/>
        <collision.check-junctions value="true"/>
        <time-to-teleport value="-1"/>
        <time-to-teleport.highways value="-1"/>
        <max-depart-delay value="900"/>
        <ignore-route-errors value="true"/>
        <lateral-resolution value="0.8"/>
        <default.speeddev value="0.2"/>
        <default.emergencydecel value="9"/>
    </processing>
    <routing>
        <device.rerouting.probability value="0.4"/>
        <device.rerouting.period value="300"/>
        <device.rerouting.adaptation-steps value="180"/>
        <device.rerouting.adaptation-interval value="10"/>
    </routing>
    <report>
        <verbose value="true"/>
        <duration-log.statistics value="true"/>
        <no-step-log value="true"/>
    </report>
    <gui_only>
        <gui-settings-file value="{gui_settings_file}"/>
        <start value="true"/>
        <quit-on-end value="false"/>
        <game value="false"/>
        <tracker-interval value="1"/>
        <window-size value="1400,900"/>
    </gui_only>
</configuration>""")

print("\n" + "="*60)
print("SIMULATION SETUP COMPLETE")
print("="*60)
print(f"Total vehicles: 120 (30 of each type)")
print(f"Simulation time: {SIMULATION_TIME} seconds ({SIMULATION_TIME/60:.1f} minutes)")
print(f"Vehicle types: auto, motorbike, car, bus (30 each)")
print(f"Potholes: On main roads (pink=50%, orange=75%, red=90% INSTANT speed reduction)")
print("="*60)
print("\nStarting SUMO with pothole speed controller...")
print("NOTE: Vehicles will slow down INSTANTLY when touching potholes!")
print("="*60)

# --- 7. Run SUMO with TraCI pothole controller ---
subprocess.run(["python3", "pothole_controller.py"])
