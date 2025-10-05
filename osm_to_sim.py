import os
import subprocess
import xml.etree.ElementTree as ET
import random

# --- SETTINGS ---
osm_file = "mymap.osm"
net_file = "mymap.net.xml"
poly_file = "mymap.poly.xml"
trips_file = "mymap.trips.xml"
rou_file = "mymap.rou.xml"
sumocfg_file = "mymap.sumocfg"
vtypes_file = "mymap.vtypes.xml"
obstacles_file = "mymap.obstacles.xml"

# Path to SUMO home
SUMO_HOME = os.environ.get("SUMO_HOME", "/usr/share/sumo")

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

# --- 2.5. Generate vehicle types ---
print("Generating vehicle types...")
with open(vtypes_file, "w") as f:
    f.write(f"""<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <!-- Auto-rickshaw: Small, slow, highly maneuverable -->
    <vType id="auto_rickshaw" accel="1.5" decel="4.0" sigma="0.8" length="3.0" minGap="1.0" 
           maxSpeed="13.89" color="1,1,0" vClass="taxi" guiShape="delivery" 
           speedFactor="0.9" speedDev="0.2" lcStrategic="1.5" lcCooperative="0.5"
           lcSpeedGain="2.0" lcKeepRight="0.3"/>
    
    <!-- Motorcycle/Scooter: Fast, agile, weaves through traffic -->
    <vType id="motorcycle" accel="3.5" decel="6.0" sigma="0.6" length="2.0" minGap="0.5" 
           maxSpeed="27.78" color="1,0,0" vClass="motorcycle" guiShape="motorcycle"
           speedFactor="1.2" speedDev="0.3" lcStrategic="2.0" lcCooperative="0.3"
           lcSpeedGain="3.0" lcKeepRight="0.1"/>
    
    <!-- Car: Medium speed, standard behavior -->
    <vType id="car" accel="2.6" decel="4.5" sigma="0.5" length="5.0" minGap="2.5" 
           maxSpeed="33.33" color="0.9,0.9,0.9" vClass="passenger" guiShape="passenger"
           speedFactor="1.0" speedDev="0.15" lcStrategic="1.0" lcCooperative="1.0"
           lcSpeedGain="1.0" lcKeepRight="0.5"/>
    
    <!-- Bus/Truck: Large, slow, less maneuverable - FIXED routing -->
    <vType id="bus_truck" accel="1.2" decel="3.5" sigma="0.3" length="12.0" minGap="3.5" 
           maxSpeed="22.22" color="0,0,1" vClass="bus" guiShape="bus"
           speedFactor="0.85" speedDev="0.1" lcStrategic="0.5" lcCooperative="1.5"
           lcSpeedGain="0.5" lcKeepRight="0.8"/>
</routes>""")

# --- 2.6. Generate road obstacles (barricades and potholes) ---
print("Generating road obstacles and Indian road features...")
# Parse network file to get edge information
tree = ET.parse(net_file)
root = tree.getroot()
edges = [edge for edge in root.findall('.//edge') if edge.get('function') != 'internal']

# Use ALL suitable edges for potholes (every road gets potholes)
suitable_edges = [edge for edge in edges if edge.findall('lane')]

import math

with open(obstacles_file, "w") as f:
    f.write(f"""<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n""")
    
    # Add barricades - YELLOW AND BLACK STRIPED
    print(f"  Adding barricades (yellow-black striped)...")
    barricade_edges = random.sample(suitable_edges, min(50, len(suitable_edges)))  # Increased to 50 for more chaos
    
    for i, edge in enumerate(barricade_edges):
        lanes = edge.findall('lane')
        if lanes:
            lane = lanes[0]
            shape = lane.get('shape')
            if shape:
                coords = shape.split()
                if len(coords) >= 3:
                    mid_idx = len(coords)//2
                    mid_point = coords[mid_idx]
                    x, y = map(float, mid_point.split(','))
                    
                    # Create LARGE yellow-black striped barricade
                    poly_shape = f"{x-4},{y-1.5} {x+4},{y-1.5} {x+4},{y+1.5} {x-4},{y+1.5}"
                    f.write(f"""    <poly id="barricade_yellow_{i}" type="barricade" color="1,1,0" fill="1" layer="10" shape="{poly_shape}"/>\n""")
                    
                    # Black diagonal stripes (3 stripes)
                    for s in range(3):
                        offset = -3 + s * 2.5
                        stripe_shape = f"{x+offset-0.3},{y-1.5} {x+offset+0.3},{y-1.5} {x+offset+1.3},{y+1.5} {x+offset+0.7},{y+1.5}"
                        f.write(f"""    <poly id="barricade_stripe_{i}_{s}" type="barricade_stripe" color="0,0,0" fill="1" layer="11" shape="{stripe_shape}"/>\n""")
    
    # Add VISIBLE POTHOLES - REALISTIC INDIAN ROAD SIZES (mostly small, erratic shapes)
    print(f"  Adding realistic potholes (8-12 per road, mostly small, erratic)...")
    pothole_count = 0
    
    # Limit to reasonable number of roads to avoid overload
    pothole_edges = suitable_edges[:min(200, len(suitable_edges))]
    
    for edge in pothole_edges:
        lanes = edge.findall('lane')
        if lanes:
            lane = lanes[0]
            lane_id = lane.get('id')
            length = float(lane.get('length', '50'))
            shape = lane.get('shape')
            
            if shape and length > 20:
                coords = shape.split()
                
                # 8-12 potholes per road at random positions (Indian road reality)
                num_potholes = random.randint(8, 12)
                positions = [random.uniform(0.1, 0.9) for _ in range(num_potholes)]
                
                for pos_ratio in positions:
                    pos_idx = int(len(coords) * pos_ratio)
                    if pos_idx < len(coords):
                        point = coords[pos_idx]
                        x, y = map(float, point.split(','))
                        
                        # Weighted size distribution: 70% small, 20% medium, 10% large
                        size_type = random.choices(['small', 'medium', 'large'], weights=[70, 20, 10])[0]
                        
                        if size_type == 'small':
                            size = random.uniform(0.3, 1.0)  # Small potholes (most common)
                        elif size_type == 'medium':
                            size = random.uniform(1.0, 2.5)  # Medium potholes
                        else:
                            size = random.uniform(2.5, 5.0)  # Large potholes (rare)
                        
                        color = "0.2,0.2,0.2"  # Dark gray
                        
                        # Create irregular erratic pothole shape
                        points = []
                        num_points = 8
                        for angle_step in range(num_points):
                            angle = (angle_step * 360 / num_points) + random.uniform(-15, 15)
                            rad = math.radians(angle)
                            radius = size * random.uniform(0.8, 1.2)
                            px = x + radius * math.cos(rad)
                            py = y + radius * math.sin(rad)
                            points.append(f"{px:.2f},{py:.2f}")
                        poly_shape = " ".join(points)
                        
                        f.write(f"""    <poly id="pothole_{pothole_count}" type="pothole" color="{color}" fill="1" layer="10" shape="{poly_shape}"/>\n""")
                        
                        # Add speed reduction
                        pos = length * pos_ratio
                        speed_limit = float(lane.get('speed', '13.89'))
                        reduced_speed = speed_limit * 0.4
                        f.write(f"""    <variableSpeedSign id="pothole_speed_{pothole_count}" lanes="{lane_id}" pos="{pos:.2f}">
        <step time="0" speed="{reduced_speed:.2f}"/>
    </variableSpeedSign>\n""")
                        
                        pothole_count += 1
    
    print(f"    Total potholes created: {pothole_count}")
    
    # Add speed breakers
    print("  Adding speed breakers...")
    breaker_edges = random.sample(suitable_edges, min(20, len(suitable_edges)))
    
    for i, edge in enumerate(breaker_edges):
        lanes = edge.findall('lane')
        if lanes:
            lane = lanes[0]
            shape = lane.get('shape')
            if shape:
                coords = shape.split()
                if len(coords) >= 3:
                    idx = int(len(coords) * 0.4)
                    point = coords[idx]
                    x, y = map(float, point.split(','))
                    poly_shape = f"{x-3},{y-0.4} {x+3},{y-0.4} {x+3},{y+0.4} {x-3},{y+0.4}"
                    f.write(f"""    <poly id="speedbreaker_{i}" type="speedbreaker" color="1,1,0" fill="1" layer="10" shape="{poly_shape}"/>\n""")
    
    # Add roadside obstacles
    print("  Adding roadside obstacles...")
    roadside_edges = random.sample(suitable_edges, min(10, len(suitable_edges)))
    
    for i, edge in enumerate(roadside_edges):
        lanes = edge.findall('lane')
        if lanes and len(lanes) > 1:
            lane = lanes[-1]
            shape = lane.get('shape')
            if shape:
                coords = shape.split()
                if len(coords) >= 2:
                    idx = random.randint(0, len(coords)-1)
                    point = coords[idx]
                    x, y = map(float, point.split(','))
                    obstacle_type = random.choice(['vendor', 'parked'])
                    if obstacle_type == 'vendor':
                        poly_shape = f"{x+6},{y-1} {x+8},{y-1} {x+8},{y+1} {x+6},{y+1}"
                        color = "0.2,0.6,0.2"
                    else:
                        poly_shape = f"{x+6},{y-2} {x+9},{y-2} {x+9},{y+2} {x+6},{y+2}"
                        color = "0.5,0.5,0.5"
                    f.write(f"""    <poly id="roadside_{obstacle_type}_{i}" type="{obstacle_type}" color="{color}" fill="1" layer="10" shape="{poly_shape}"/>\n""")
    
    f.write(f"""</additional>""")


# --- 2.7. Create enhanced view settings ---
print("Creating enhanced visualization settings...")
view_file = "mymap.view.xml"
with open(view_file, "w") as f:
    f.write("""<viewsettings>
    <scheme name="indian_roads">
        <background backgroundColor="0.8,0.9,0.8" showGrid="0"/>
        <edges laneEdgeMode="1" scaleMode="0" laneShowBorders="1" 
               edgeName.show="0" streetName.show="1" edgeData.show="0"
               edgeColorMode="0" edgeWidthMode="0"/>
        <vehicles vehicleQuality="3" vehicleSize.minSize="1" vehicleSize.exaggeration="2.0"
                 vehicleName.show="1" vehicleColorMode="0" vehicleShape.show="1"
                 vehicleText.show="1" vehicleText.param="speed" vehicleText.size="50"/>
        <persons personQuality="2" personSize.minSize="1" personSize.exaggeration="1"/>
        <junctions junctionMode="1" drawLinkTLIndex="0" drawLinkJunctionIndex="0"
                   junctionName.show="0" internalJunctionName.show="0" tlsPhaseIndex.show="0"/>
        <additionals addMode="0" addSize.exaggeration="3" addName.show="1" addFullName.show="1"/>
        <pois poiSize.minSize="1" poiSize.exaggeration="2" poiName.show="0"/>
        <polys polySize.minSize="2" polySize.exaggeration="3" polyName.show="1"/>
        <legend showSizeLegend="0"/>
        <opengl antialiase="1" dither="1"/>
    </scheme>
</viewsettings>""")



# --- 3. Generate random trips ---
print("Generating trips with improved routing...")
subprocess.run([
    "python3", os.path.join(SUMO_HOME, "tools/randomTrips.py"),
    "-n", net_file,
    "-o", trips_file,
    "-e", "3600",  # 1 hour simulation
    "-p", "2",     # new vehicle every 2 sec on average
    "-l",          # allow loops
    "--min-distance", "300",  # Minimum trip distance to avoid U-turns
    "--max-distance", "3000",  # Maximum trip distance for realism
    "--fringe-factor", "10",  # More traffic from edges
    "--allow-fringe",  # Allow fringe nodes
    "--validate"  # Validate trips
])

# --- 4. Convert trips to routes ---
print("Converting trips to routes with better routing algorithm...")
subprocess.run([
    "duarouter",
    "-n", net_file,
    "-t", trips_file,
    "-o", rou_file,
    "--additional-files", vtypes_file,  # Include vehicle types
    "--ignore-errors",  # Continue on errors
    "--repair",  # Repair broken routes
    "--remove-loops",  # Remove route loops
    "--routing-algorithm", "astar",  # Better routing algorithm
    "--weights.random-factor", "1.5"  # Add route variation
])

# --- 4.5. Modify routes to assign different vehicle types ---
print("Assigning vehicle types to routes...")
tree = ET.parse(rou_file)
root = tree.getroot()

# Vehicle type distribution (Indian traffic mix)
# 40% motorcycles, 30% cars, 20% auto-rickshaws, 10% buses/trucks
vehicle_types = ["motorcycle"] * 40 + ["car"] * 30 + ["auto_rickshaw"] * 20 + ["bus_truck"] * 10

for vehicle in root.findall('vehicle'):
    vtype = random.choice(vehicle_types)
    vehicle.set('type', vtype)

# Write modified routes
tree.write(rou_file, encoding='UTF-8', xml_declaration=True)

# --- 5. Generate SUMO configuration ---
print("Writing SUMO config with enhanced visualization...")
with open(sumocfg_file, "w") as f:
    f.write(f"""<configuration>
    <input>
        <net-file value="{net_file}"/>
        <route-files value="{rou_file}"/>
        <additional-files value="{poly_file},{vtypes_file},{obstacles_file}"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="3600"/>
        <step-length value="0.1"/>
    </time>
    <processing>
        <collision.action value="none"/>
        <collision.mingap-factor value="0"/>
        <time-to-teleport value="-1"/>
        <max-depart-delay value="900"/>
        <ignore-route-errors value="true"/>
    </processing>
    <routing>
        <device.rerouting.probability value="0.3"/>
        <device.rerouting.period value="300"/>
        <device.rerouting.adaptation-steps value="180"/>
    </routing>
    <gui_only>
        <gui-settings-file value="mymap.view.xml"/>
        <start value="true"/>
        <quit-on-end value="false"/>
        <game value="false"/>
    </gui_only>
</configuration>""")

# --- 6. Run SUMO GUI ---
print("Running SUMO simulation...")
subprocess.run(["sumo-gui", "-c", sumocfg_file])
