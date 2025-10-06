#!/usr/bin/env python3
"""
Indian Road Traffic Simulation
- 4 vehicle types with realistic Indian driving behavior
- Visible barricades that force lane changes
- Potholes with 99% speed reduction
- 1000 vehicles per class (250 total)
- Live stats display for every vehicle
- AI agent selection: Random, Conservative, Aggressive, or Mixed
"""

import os
import subprocess
import xml.etree.ElementTree as ET
import random
import math
import sys

# Files
osm_file = "mymap.osm"
net_file = "mymap.net.xml"
poly_file = "mymap.poly.xml"
rou_file = "mymap.rou.xml"
sumocfg_file = "mymap.sumocfg"
add_file = "mymap.add.xml"

SUMO_HOME = os.environ.get("SUMO_HOME", "/usr/share/sumo")

# AI AGENT SELECTION
print("\n" + "="*60)
print("🚗 INDIAN ROAD SIMULATION - AI AGENT SELECTION")
print("="*60)
print("\nChoose AI agent behavior for vehicles:")
print("1. RANDOM     - Autos change routes randomly, chaos!")
print("2. CONSERVATIVE - Careful driving, follow rules")
print("3. AGGRESSIVE - Fast, risky, lots of overtaking")
print("4. MIXED      - Combination of all behaviors (realistic)")
print("5. DEFAULT    - Standard SUMO behavior")
print()

while True:
    choice = input("Enter choice (1-5) [default: 4]: ").strip() or "4"
    if choice in ["1", "2", "3", "4", "5"]:
        break
    print("Invalid choice! Please enter 1-5")

AI_MODE = {
    "1": "random",
    "2": "conservative", 
    "3": "aggressive",
    "4": "mixed",
    "5": "default"
}[choice]

print(f"\n✓ Selected: {AI_MODE.upper()} mode\n")
print("="*60 + "\n")

# 1. Convert OSM to SUMO network
print("Converting OSM to SUMO network...")
subprocess.run([
    "netconvert",
    "--osm-files", osm_file,
    "--type-files", os.path.join(SUMO_HOME, "data/typemap/osmNetconvert.typ.xml"),
    "--output-file", net_file,
    "--geometry.remove", "--ramps.guess", "--junctions.join",
    "--tls.guess-signals", "--tls.discard-simple", 
    "--tls.join", "--tls.default-type", "actuated"
])

# 2. Generate polygons
print("Generating polygons...")
subprocess.run([
    "polyconvert",
    "--osm-files", osm_file,
    "--net-file", net_file,
    "--type-file", os.path.join(SUMO_HOME, "data/typemap/osmPolyconvert.typ.xml"),
    "-o", poly_file
])

# 3. Parse network to get edges and lanes
print("Parsing network for obstacles...")
tree = ET.parse(net_file)
root = tree.getroot()
edges = [edge for edge in root.findall('.//edge') if edge.get('function') != 'internal']
suitable_edges = [edge for edge in edges if edge.findall('lane')]

# Get all suitable edges for trips (allow passenger vehicles)
trip_edges = []
for edge in edges:
    edge_id = edge.get('id')
    if not edge_id or edge_id.startswith(':'):
        continue
    lanes = edge.findall('lane')
    for lane in lanes:
        disallow = lane.get('disallow', '')
        if 'passenger' not in disallow and 'all' not in disallow:
            trip_edges.append(edge_id)
            break

print(f"Found {len(trip_edges)} suitable edges for routing")

# 4. Create additionals (barricades, potholes, closings)
print("Creating visible obstacles...")
with open(add_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    f.write('xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n\n')
    
    # BARRICADES - Block specific lanes to force lane changes
    print("  Adding barricades to block lanes...")
    barricade_count = 0
    barricade_edges = random.sample(suitable_edges, min(60, len(suitable_edges)))
    
    for edge in barricade_edges:
        lanes = edge.findall('lane')
        if len(lanes) > 1:  # Only if multiple lanes exist
            # Block one lane (usually the rightmost)
            lane_to_block = lanes[-1]
            lane_id = lane_to_block.get('id')
            length = float(lane_to_block.get('length', '50'))
            shape = lane_to_block.get('shape')
            
            if shape and length > 30:
                coords = shape.split()
                pos = length * 0.5  # Middle of road
                idx = len(coords) // 2
                x, y = map(float, coords[idx].split(','))
                
                # Large visible barricade (yellow with black stripes)
                barricade_shape = f"{x-5},{y-2} {x+5},{y-2} {x+5},{y+2} {x-5},{y+2}"
                f.write(f'    <poly id="barricade_{barricade_count}" type="barricade" ')
                f.write(f'color="1,0.8,0" fill="1" layer="100" shape="{barricade_shape}"/>\n')
                
                # Black stripes
                for i in range(4):
                    stripe_x = x - 4 + i * 2.5
                    stripe = f"{stripe_x},{y-2} {stripe_x+0.8},{y-2} {stripe_x+0.8},{y+2} {stripe_x},{y+2}"
                    f.write(f'    <poly id="barricade_stripe_{barricade_count}_{i}" ')
                    f.write(f'type="stripe" color="0,0,0" fill="1" layer="101" shape="{stripe}"/>\n')
                
                # Lane closing to force lane change
                f.write(f'    <laneAreaDetector id="barricade_detector_{barricade_count}" ')
                f.write(f'lanes="{lane_id}" pos="{pos-10}" endPos="{pos+10}" file="NUL"/>\n')
                
                barricade_count += 1
    
    print(f"  Created {barricade_count} barricades")
    
    # POTHOLES - HIGHLY VISIBLE with dark color and layer 10 (like osm_to_sim.py)
    print("  Adding VISIBLE potholes with speed reduction...")
    pothole_count = 0
    pothole_edges = suitable_edges[:min(200, len(suitable_edges))]
    
    for edge in pothole_edges:
        lanes = edge.findall('lane')
        if lanes:
            # Get all lane IDs
            all_lane_ids = [lane.get('id') for lane in lanes]
            lane = lanes[0]
            length = float(lane.get('length', '50'))
            shape = lane.get('shape')
            
            if shape and length > 20:
                coords = shape.split()
                # 15-25 potholes per road (MANY potholes like real Indian roads!)
                num_potholes = random.randint(15, 25)
                
                for _ in range(num_potholes):
                    pos_ratio = random.uniform(0.1, 0.9)
                    idx = int(len(coords) * pos_ratio)
                    if idx < len(coords):
                        x, y = map(float, coords[idx].split(','))
                        
                        # Size: mostly small, some medium/large (Indian road distribution)
                        size_type = random.choices(['small', 'medium', 'large'], weights=[70, 20, 10])[0]
                        if size_type == 'small':
                            size = random.uniform(0.5, 1.5)  # Slightly bigger for visibility
                        elif size_type == 'medium':
                            size = random.uniform(1.5, 3.0)
                        else:
                            size = random.uniform(3.0, 6.0)
                        
                        # Spread across lanes
                        lateral = random.uniform(-2, 2)
                        
                        # DARK GRAY pothole - VERY VISIBLE (color from osm_to_sim.py)
                        color = "0.2,0.2,0.2"  # Much darker!
                        
                        # Create irregular erratic pothole shape with more points for realism
                        points = []
                        num_points = 8
                        for angle_step in range(num_points):
                            angle = (angle_step * 360 / num_points) + random.uniform(-15, 15)
                            rad = math.radians(angle)
                            radius = size * random.uniform(0.8, 1.2)
                            px = x + radius * math.cos(rad) + lateral
                            py = y + radius * math.sin(rad)
                            points.append(f"{px:.2f},{py:.2f}")
                        
                        pothole_shape = " ".join(points)
                        # IMPORTANT: Use layer="10" for visibility (NOT layer="50")
                        f.write(f'    <poly id="pothole_{pothole_count}" type="pothole" ')
                        f.write(f'color="{color}" fill="1" layer="10" shape="{pothole_shape}"/>\n')
                        
                        # Speed reduction to 30% (70% reduction) for ALL lanes
                        pos = length * pos_ratio
                        speed_limit = float(lane.get('speed', '13.89'))
                        reduced_speed = speed_limit * 0.3  # 70% reduction (more realistic)
                        
                        lanes_str = " ".join(all_lane_ids)
                        f.write(f'    <variableSpeedSign id="pothole_vss_{pothole_count}" ')
                        f.write(f'lanes="{lanes_str}" pos="{pos:.2f}">\n')
                        f.write(f'        <step time="0" speed="{reduced_speed:.2f}"/>\n')
                        f.write(f'    </variableSpeedSign>\n\n')
                        
                        pothole_count += 1
    
    print(f"  Created {pothole_count} potholes")
    
    f.write('</additional>\n')

# 5. Create routes with vehicle types and trips
print("Creating routes with 1000 vehicles (250 per class)...")

# Helper function to get diverse routes
def get_route_pair(edges, route_type="random"):
    """Get origin-destination pair based on route type"""
    if route_type == "short":
        # Short trips (nearby edges)
        from_edge = random.choice(edges)
        nearby_edges = [e for e in edges if abs(edges.index(e) - edges.index(from_edge)) < 50]
        to_edge = random.choice(nearby_edges) if nearby_edges else random.choice(edges)
    elif route_type == "long":
        # Long trips (far apart edges)
        from_edge = random.choice(edges)
        to_edge = random.choice(edges)
        # Ensure they're different
        while to_edge == from_edge:
            to_edge = random.choice(edges)
    elif route_type == "circular":
        # Create potential circular routes
        from_edge = random.choice(edges)
        to_edge = from_edge  # Same start and end
    else:
        # Random
        from_edge = random.choice(edges)
        to_edge = random.choice(edges)
        while to_edge == from_edge:
            to_edge = random.choice(edges)
    
    return from_edge, to_edge

# Apply AI mode parameters
def get_vtype_params(base_vtype, ai_mode):
    """Adjust vehicle parameters based on AI mode"""
    params = {}
    
    if ai_mode == "conservative":
        params = {
            "speedFactor": 0.8,
            "lcAssertive": 0.3,
            "lcImpatience": 0.1,
            "sigma": 0.3
        }
    elif ai_mode == "aggressive":
        params = {
            "speedFactor": 1.5,
            "lcAssertive": 3.0,
            "lcImpatience": 1.0,
            "sigma": 0.9
        }
    elif ai_mode == "random":
        params = {
            "speedFactor": random.uniform(0.7, 1.8),
            "lcAssertive": random.uniform(0.5, 3.0),
            "lcImpatience": random.uniform(0.1, 1.0),
            "sigma": random.uniform(0.3, 1.0)
        }
    # For 'mixed' and 'default', return empty (use base values)
    
    return params

with open(rou_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    f.write('xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n')
    
    # VEHICLE TYPE DEFINITIONS with Indian driving behavior
    
    # Define base parameters with AI adjustments
    if AI_MODE == "mixed":
        # Mixed mode: Define 3 variants per vehicle type
        
        # AUTO-RICKSHAW VARIANTS
        f.write('    <!-- Auto-rickshaw: Rash, frequent overtaking -->\n')
        f.write('    <vType id="auto" length="3.5" minGap="0.5" maxSpeed="15" accel="2.0" decel="4.5"\n')
        f.write('           color="1,1,0" vClass="passenger" guiShape="delivery"\n')
        f.write('           speedFactor="1.3" speedDev="0.4" sigma="0.9"\n')
        f.write('           lcStrategic="3.0" lcCooperative="0.2" lcSpeedGain="3.0"\n')
        f.write('           lcKeepRight="0.1" lcAssertive="2.0" lcImpatience="0.8"/>\n\n')
        
        f.write('    <vType id="auto_calm" length="3.5" minGap="1.0" maxSpeed="15" accel="1.5" decel="4.0"\n')
        f.write('           color="1,1,0" vClass="passenger" guiShape="delivery"\n')
        f.write('           speedFactor="0.9" speedDev="0.2" sigma="0.4"\n')
        f.write('           lcStrategic="1.0" lcCooperative="1.0" lcSpeedGain="1.0"\n')
        f.write('           lcKeepRight="0.5" lcAssertive="0.5" lcImpatience="0.3"/>\n\n')
        
        f.write('    <vType id="auto_crazy" length="3.5" minGap="0.3" maxSpeed="20" accel="3.0" decel="5.0"\n')
        f.write('           color="1,1,0" vClass="passenger" guiShape="delivery"\n')
        f.write('           speedFactor="1.8" speedDev="0.6" sigma="1.0"\n')
        f.write('           lcStrategic="5.0" lcCooperative="0.0" lcSpeedGain="5.0"\n')
        f.write('           lcKeepRight="0.0" lcAssertive="4.0" lcImpatience="1.0"/>\n\n')
        
        # MOTORCYCLE VARIANTS
        f.write('    <!-- Motorcycle: Erratic lane changes, variable speed -->\n')
        f.write('    <vType id="motorcycle" length="2.0" minGap="0.3" maxSpeed="30" accel="4.0" decel="7.0"\n')
        f.write('           color="1,0,0" vClass="motorcycle" guiShape="motorcycle"\n')
        f.write('           speedFactor="1.5" speedDev="0.5" sigma="0.8"\n')
        f.write('           lcStrategic="4.0" lcCooperative="0.1" lcSpeedGain="4.0"\n')
        f.write('           lcKeepRight="0.05" lcAssertive="3.0" lcImpatience="1.0"/>\n\n')
        
        f.write('    <vType id="motorcycle_safe" length="2.0" minGap="0.8" maxSpeed="25" accel="2.5" decel="5.0"\n')
        f.write('           color="1,0,0" vClass="motorcycle" guiShape="motorcycle"\n')
        f.write('           speedFactor="1.0" speedDev="0.3" sigma="0.5"\n')
        f.write('           lcStrategic="1.5" lcCooperative="0.8" lcSpeedGain="1.5"\n')
        f.write('           lcKeepRight="0.3" lcAssertive="1.0" lcImpatience="0.4"/>\n\n')
        
        f.write('    <vType id="motorcycle_racer" length="2.0" minGap="0.2" maxSpeed="40" accel="6.0" decel="9.0"\n')
        f.write('           color="1,0,0" vClass="motorcycle" guiShape="motorcycle"\n')
        f.write('           speedFactor="2.0" speedDev="0.7" sigma="1.0"\n')
        f.write('           lcStrategic="6.0" lcCooperative="0.0" lcSpeedGain="6.0"\n')
        f.write('           lcKeepRight="0.0" lcAssertive="5.0" lcImpatience="1.0"/>\n\n')
        
        # CAR VARIANTS
        f.write('    <!-- Car: Normal speed, stable driving -->\n')
        f.write('    <vType id="car" length="5.0" minGap="2.0" maxSpeed="20" accel="2.5" decel="4.5"\n')
        f.write('           color="0.5,0.5,0.5" vClass="passenger" guiShape="passenger"\n')
        f.write('           speedFactor="1.0" speedDev="0.2" sigma="0.5"\n')
        f.write('           lcStrategic="1.0" lcCooperative="1.0" lcSpeedGain="1.0"\n')
        f.write('           lcKeepRight="0.5" lcAssertive="0.5" lcImpatience="0.3"/>\n\n')
        
        f.write('    <vType id="car_cautious" length="5.0" minGap="3.0" maxSpeed="18" accel="1.8" decel="3.5"\n')
        f.write('           color="0.5,0.5,0.5" vClass="passenger" guiShape="passenger"\n')
        f.write('           speedFactor="0.8" speedDev="0.1" sigma="0.3"\n')
        f.write('           lcStrategic="0.5" lcCooperative="1.5" lcSpeedGain="0.5"\n')
        f.write('           lcKeepRight="0.8" lcAssertive="0.2" lcImpatience="0.1"/>\n\n')
        
        f.write('    <vType id="car_sporty" length="5.0" minGap="1.5" maxSpeed="25" accel="3.5" decel="6.0"\n')
        f.write('           color="0.5,0.5,0.5" vClass="passenger" guiShape="passenger"\n')
        f.write('           speedFactor="1.4" speedDev="0.4" sigma="0.7"\n')
        f.write('           lcStrategic="2.0" lcCooperative="0.5" lcSpeedGain="2.5"\n')
        f.write('           lcKeepRight="0.2" lcAssertive="1.5" lcImpatience="0.7"/>\n\n')
        
        # BUS VARIANTS
        f.write('    <!-- Bus: Slow, stable, less maneuverable -->\n')
        f.write('    <vType id="bus" length="12.0" minGap="3.0" maxSpeed="15" accel="1.0" decel="3.0"\n')
        f.write('           color="0,0.4,1" vClass="bus" guiShape="bus"\n')
        f.write('           speedFactor="0.8" speedDev="0.1" sigma="0.3"\n')
        f.write('           lcStrategic="0.3" lcCooperative="1.5" lcSpeedGain="0.3"\n')
        f.write('           lcKeepRight="0.8" lcAssertive="0.1" lcImpatience="0.1"/>\n\n')
        
        f.write('    <vType id="bus_express" length="12.0" minGap="2.5" maxSpeed="18" accel="1.3" decel="3.5"\n')
        f.write('           color="0,0.4,1" vClass="bus" guiShape="bus"\n')
        f.write('           speedFactor="1.0" speedDev="0.2" sigma="0.4"\n')
        f.write('           lcStrategic="0.8" lcCooperative="1.0" lcSpeedGain="0.8"\n')
        f.write('           lcKeepRight="0.6" lcAssertive="0.3" lcImpatience="0.3"/>\n\n')
        
        f.write('    <vType id="bus_local" length="12.0" minGap="3.5" maxSpeed="12" accel="0.8" decel="2.5"\n')
        f.write('           color="0,0.4,1" vClass="bus" guiShape="bus"\n')
        f.write('           speedFactor="0.6" speedDev="0.1" sigma="0.2"\n')
        f.write('           lcStrategic="0.1" lcCooperative="2.0" lcSpeedGain="0.1"\n')
        f.write('           lcKeepRight="0.9" lcAssertive="0.0" lcImpatience="0.0"/>\n\n')
    
    else:
        # Standard types (for other AI modes)
        # AUTO-RICKSHAW
        f.write('    <!-- Auto-rickshaw: Rash, frequent overtaking -->\n')
        f.write('    <vType id="auto" length="3.5" minGap="0.5" maxSpeed="15" accel="2.0" decel="4.5"\n')
        f.write('           color="1,1,0" vClass="passenger" guiShape="delivery"\n')
        f.write('           speedFactor="1.3" speedDev="0.4" sigma="0.9"\n')
        f.write('           lcStrategic="3.0" lcCooperative="0.2" lcSpeedGain="3.0"\n')
        f.write('           lcKeepRight="0.1" lcAssertive="2.0" lcImpatience="0.8"/>\n\n')
        
        # MOTORCYCLE
        f.write('    <!-- Motorcycle: Erratic lane changes, variable speed -->\n')
        f.write('    <vType id="motorcycle" length="2.0" minGap="0.3" maxSpeed="30" accel="4.0" decel="7.0"\n')
        f.write('           color="1,0,0" vClass="motorcycle" guiShape="motorcycle"\n')
        f.write('           speedFactor="1.5" speedDev="0.5" sigma="0.8"\n')
        f.write('           lcStrategic="4.0" lcCooperative="0.1" lcSpeedGain="4.0"\n')
        f.write('           lcKeepRight="0.05" lcAssertive="3.0" lcImpatience="1.0"/>\n\n')
        
        # CAR
        f.write('    <!-- Car: Normal speed, stable driving -->\n')
        f.write('    <vType id="car" length="5.0" minGap="2.0" maxSpeed="20" accel="2.5" decel="4.5"\n')
        f.write('           color="0.5,0.5,0.5" vClass="passenger" guiShape="passenger"\n')
        f.write('           speedFactor="1.0" speedDev="0.2" sigma="0.5"\n')
        f.write('           lcStrategic="1.0" lcCooperative="1.0" lcSpeedGain="1.0"\n')
        f.write('           lcKeepRight="0.5" lcAssertive="0.5" lcImpatience="0.3"/>\n\n')
        
        # BUS
        f.write('    <!-- Bus: Slow, stable, less maneuverable -->\n')
        f.write('    <vType id="bus" length="12.0" minGap="3.0" maxSpeed="15" accel="1.0" decel="3.0"\n')
        f.write('           color="0,0.4,1" vClass="bus" guiShape="bus"\n')
        f.write('           speedFactor="0.8" speedDev="0.1" sigma="0.3"\n')
        f.write('           lcStrategic="0.3" lcCooperative="1.5" lcSpeedGain="0.3"\n')
        f.write('           lcKeepRight="0.8" lcAssertive="0.1" lcImpatience="0.1"/>\n\n')
    
    # Generate vehicles with better spawning and route distribution
    # Create COMMON DESTINATIONS for traffic convergence (realistic traffic patterns)
    if len(trip_edges) >= 10:
        # Select 5 popular destinations (like malls, stations, city centers)
        popular_destinations = random.sample(trip_edges, min(5, len(trip_edges)))
    else:
        popular_destinations = trip_edges
    
    # Route distribution: 50% go to popular destinations, 50% random
    
    vehicle_types = [
        ("auto", 250),
        ("motorcycle", 250),
        ("car", 250),
        ("bus", 250)
    ]
    
    vehicle_id = 0
    for base_vtype, count in vehicle_types:
        for i in range(count):
            # Determine actual vtype based on AI mode
            if AI_MODE == "mixed":
                # For mixed mode, use variants
                if base_vtype == "auto":
                    vtype = random.choice(["auto", "auto_calm", "auto_crazy"])
                elif base_vtype == "motorcycle":
                    vtype = random.choice(["motorcycle", "motorcycle_safe", "motorcycle_racer"])
                elif base_vtype == "car":
                    vtype = random.choice(["car", "car_cautious", "car_sporty"])
                else:  # bus
                    vtype = random.choice(["bus", "bus_express", "bus_local"])
            else:
                vtype = base_vtype
            
            # Choose route: 50% to popular destination, 50% random
            from_edge = random.choice(trip_edges)
            if random.random() < 0.5 and popular_destinations:
                # Go to popular destination
                to_edge = random.choice(popular_destinations)
            else:
                # Random destination
                to_edge = random.choice(trip_edges)
                while to_edge == from_edge and len(trip_edges) > 1:
                    to_edge = random.choice(trip_edges)
            
            # SPAWN FASTER: Vehicles spawn every 1-3 seconds (instead of 2 seconds each)
            # This creates immediate visible traffic!
            depart = vehicle_id * random.uniform(1, 3)
            
            # For random mode autos, add rerouting capability
            if AI_MODE == "random" and base_vtype == "auto" and random.random() < 0.3:
                # 30% of autos will reroute randomly
                f.write(f'    <trip id="{base_vtype}_{i}" type="{vtype}" depart="{depart:.1f}" ')
                f.write(f'from="{from_edge}" to="{to_edge}" ')
                f.write(f'departLane="best" departSpeed="max">\n')
                f.write(f'        <param key="has.rerouting.device" value="true"/>\n')
                f.write(f'        <param key="device.rerouting.period" value="60"/>\n')
                f.write(f'        <param key="device.rerouting.adaptation-steps" value="30"/>\n')
                f.write(f'    </trip>\n')
            else:
                f.write(f'    <trip id="{base_vtype}_{i}" type="{vtype}" depart="{depart:.1f}" ')
                f.write(f'from="{from_edge}" to="{to_edge}" ')
                f.write(f'departLane="best" departSpeed="max"/>\n')
            
            vehicle_id += 1
    
    f.write('\n</routes>\n')

print(f"Created 400 vehicles")

# 6. Convert trips to routes
print("Routing vehicles...")
subprocess.run([
    "duarouter",
    "-n", net_file,
    "-r", rou_file,
    "-o", rou_file + ".xml",
    "--ignore-errors",
    "--repair",
    "--remove-loops",
    "--routing-algorithm", "astar",
    "--no-step-log"
], capture_output=True)

# Use the routed file
if os.path.exists(rou_file + ".xml"):
    os.rename(rou_file + ".xml", rou_file)

# 7. Create SUMO config
print("Creating SUMO configuration...")
with open(sumocfg_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<configuration>\n')
    f.write('    <input>\n')
    f.write(f'        <net-file value="{net_file}"/>\n')
    f.write(f'        <route-files value="{rou_file}"/>\n')
    f.write(f'        <additional-files value="{poly_file},{add_file}"/>\n')
    f.write('    </input>\n')
    f.write('    <time>\n')
    f.write('        <begin value="0"/>\n')
    f.write('        <end value="3600"/>\n')
    f.write('    </time>\n')
    f.write('    <processing>\n')
    f.write('        <collision.action value="warn"/>\n')
    f.write('        <time-to-teleport value="-1"/>\n')
    f.write('    </processing>\n')
    f.write('    <gui_only>\n')
    f.write('        <start value="true"/>\n')
    f.write('        <quit-on-end value="false"/>\n')
    f.write('    </gui_only>\n')
    f.write('</configuration>\n')

# 8. Create GUI settings for stats display and better visibility
print("Creating GUI settings for better visibility...")
with open("mymap.settings.xml", "w") as f:
    f.write('<viewsettings>\n')
    f.write('    <scheme name="indian_roads_stats">\n')
    # Vehicles - larger and more visible
    f.write('        <vehicles vehicleQuality="3" vehicleSize.minSize="3" ')
    f.write('vehicleSize.exaggeration="3.0"\n')
    f.write('                  vehicleName.show="1" vehicleName.size="80" ')
    f.write('vehicleName.color="0,0,255"\n')
    f.write('                  showBlinker="1" drawMinGap="1"\n')
    f.write('                  vehicleColorMode="0" vehicleShape.show="1"/>\n')
    # Edges/Roads
    f.write('        <edges laneEdgeMode="1" laneShowBorders="1" ')
    f.write('streetName.show="1"/>\n')
    # Polygons (potholes, barricades) - LARGER for visibility
    f.write('        <polys polySize.exaggeration="3" polySize.minSize="2" polyName.show="1"/>\n')
    f.write('        <legend showSizeLegend="1"/>\n')
    f.write('    </scheme>\n')
    f.write('</viewsettings>\n')

print("\n" + "="*60)
print("SIMULATION READY!")
print("="*60)
print(f"AI Mode: {AI_MODE.upper()}")
print(f"Total vehicles: 1000 (250 per class) - BUSY DAY TRAFFIC!")
print(f"Barricades: {barricade_count} (block lanes, force lane changes)")
print(f"Potholes: {pothole_count} (70% speed reduction, DARK GRAY color)")
print(f"\n⚡ SPAWN RATE: Vehicles spawn every 1-3 seconds (IMMEDIATE TRAFFIC!)")
print(f"🎯 DESTINATIONS: 50% go to 5 popular destinations (traffic convergence)")
print("\n🎨 VEHICLE COLORS:")
print("  🟡 Yellow  = Auto-rickshaws")
print("  🔴 Red     = Motorcycles")
print("  ⚫ Gray    = Cars")
print("  🔵 Blue    = Buses")
print("\n�️  POTHOLES:")
print("  • DARK GRAY (0.2,0.2,0.2) - Very visible!")
print("  • Layer 10 (on top of roads)")
print("  • 15-25 per road (realistic Indian roads)")
print("  • 70% speed reduction (vehicles slow down noticeably)")
if AI_MODE == "random":
    print("\n⚡ RANDOM MODE: 30% of autos reroute dynamically!")
print("\nTo see vehicle stats in SUMO GUI:")
print("1. Right-click any vehicle → 'Show Parameter'")
print("2. Press F9 → Vehicles → Color by 'speed'")
print("3. Check 'Show vehicle name'")
print("\n👀 You should see:")
print("  ✓ Dark gray potholes everywhere")
print("  ✓ Many vehicles spawning immediately")
print("  ✓ Traffic converging to popular destinations")
print("\nStarting SUMO GUI...")
print("="*60 + "\n")

# 9. Run SUMO GUI
subprocess.run(["sumo-gui", "-c", sumocfg_file, "--gui-settings-file", "mymap.settings.xml"])
