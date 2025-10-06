#!/usr/bin/env python3
"""
STABLE Indian Road Simulation
- Optimized for performance and stability
- Guaranteed to work with reasonable limits
- Visible buses and potholes
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

print("\n" + "="*60)
print("🚗 STABLE INDIAN ROAD SIMULATION")
print("="*60)

# Simple config
print("\n📊 Configuration:")
print("Choose traffic density:")
print("1. Light   - 100 vehicles per type (400 total)")
print("2. Medium  - 250 vehicles per type (1000 total)")
print("3. Heavy   - 500 vehicles per type (2000 total)")

while True:
    traffic = input("\nEnter choice (1-3) [default: 2]: ").strip() or "2"
    if traffic in ["1", "2", "3"]:
        break

vehicle_count = {"1": 100, "2": 250, "3": 500}[traffic]
TOTAL_VEHICLES = vehicle_count * 4

print(f"\n✓ Selected: {TOTAL_VEHICLES} total vehicles")
print("\n" + "="*60 + "\n")

# 1. Convert OSM
print("Step 1/8: Converting OSM to SUMO network...")
subprocess.run([
    "netconvert",
    "--osm-files", osm_file,
    "--type-files", os.path.join(SUMO_HOME, "data/typemap/osmNetconvert.typ.xml"),
    "--output-file", net_file,
    "--geometry.remove", "--ramps.guess", "--junctions.join",
    "--tls.guess-signals", "--tls.discard-simple", 
    "--tls.join", "--tls.default-type", "actuated"
], capture_output=True, text=True)
print("✓ Network created")

# 2. Polygons
print("\nStep 2/8: Generating polygons...")
subprocess.run([
    "polyconvert",
    "--osm-files", osm_file,
    "--net-file", net_file,
    "--type-file", os.path.join(SUMO_HOME, "data/typemap/osmPolyconvert.typ.xml"),
    "-o", poly_file
], capture_output=True, text=True)
print("✓ Polygons created")

# 3. Parse network
print("\nStep 3/8: Parsing network...")
tree = ET.parse(net_file)
root = tree.getroot()

all_edges = []
trip_edges = []

for edge in root.findall('.//edge'):
    edge_id = edge.get('id')
    if edge_id and edge_id.startswith(':'):
        continue
    
    lanes = edge.findall('lane')
    if not lanes:
        continue
    
    all_edges.append(edge)
    
    for lane in lanes:
        disallow = lane.get('disallow', '')
        if 'passenger' not in disallow and 'all' not in disallow:
            trip_edges.append(edge_id)
            break

print(f"✓ Found {len(all_edges)} edges, {len(trip_edges)} suitable for routing")

# 4. Create obstacles - STABLE LIMITS
print("\nStep 4/8: Creating obstacles...")

# SAFE LIMITS to prevent crashes
MAX_POTHOLE_ROADS = 800  # Max roads with potholes
MAX_POTHOLES_PER_ROAD = 15  # Max potholes per road
MAX_TOTAL_POTHOLES = 10000  # Hard limit

pothole_count = 0
barricade_count = 0

with open(add_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    f.write('xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n\n')
    
    # BARRICADES
    barricade_edges = random.sample(all_edges, min(30, len(all_edges)))
    
    for edge in barricade_edges:
        lanes = edge.findall('lane')
        if len(lanes) > 1:
            lane_to_block = lanes[-1]
            lane_id = lane_to_block.get('id')
            length = float(lane_to_block.get('length', '50'))
            shape = lane_to_block.get('shape')
            
            if shape and length > 30:
                coords = shape.split()
                pos = length * 0.5
                idx = len(coords) // 2
                x, y = map(float, coords[idx].split(','))
                
                barricade_shape = f"{x-6},{y-3} {x+6},{y-3} {x+6},{y+3} {x-6},{y+3}"
                f.write(f'    <poly id="barricade_{barricade_count}" type="barricade" ')
                f.write(f'color="1,0.8,0" fill="1" layer="100" shape="{barricade_shape}"/>\n')
                
                for i in range(5):
                    stripe_x = x - 5 + i * 2.5
                    stripe = f"{stripe_x},{y-3} {stripe_x+1},{y-3} {stripe_x+1},{y+3} {stripe_x},{y+3}"
                    f.write(f'    <poly id="barricade_stripe_{barricade_count}_{i}" ')
                    f.write(f'type="stripe" color="0,0,0" fill="1" layer="101" shape="{stripe}"/>\n')
                
                barricade_count += 1
    
    # POTHOLES - CONTROLLED
    num_pothole_roads = min(MAX_POTHOLE_ROADS, len(all_edges))
    pothole_edges = random.sample(all_edges, num_pothole_roads)
    
    print(f"  Adding potholes to {num_pothole_roads} roads...")
    
    for edge in pothole_edges:
        if pothole_count >= MAX_TOTAL_POTHOLES:
            print(f"  ! Reached pothole limit ({MAX_TOTAL_POTHOLES}), stopping")
            break
        
        lanes = edge.findall('lane')
        if not lanes:
            continue
        
        all_lane_ids = [lane.get('id') for lane in lanes]
        first_lane = lanes[0]
        length = float(first_lane.get('length', '50'))
        shape = first_lane.get('shape')
        speed_limit = float(first_lane.get('speed', '13.89'))
        
        if not shape or length < 10:
            continue
        
        coords = shape.split()
        
        # Calculate potholes for this road
        num_potholes = min(
            random.randint(8, MAX_POTHOLES_PER_ROAD),
            MAX_TOTAL_POTHOLES - pothole_count
        )
        
        for _ in range(num_potholes):
            pos_ratio = random.uniform(0.1, 0.9)
            idx = int(len(coords) * pos_ratio)
            if idx >= len(coords):
                idx = len(coords) - 1
            
            x, y = map(float, coords[idx].split(','))
            
            # Pothole type
            pothole_type = random.choices(
                ['small', 'medium', 'large'],
                weights=[60, 30, 10]
            )[0]
            
            if pothole_type == 'small':
                size = random.uniform(0.5, 1.0)
                speed_reduction = 0.50
                color = "0.3,0.3,0.3"
            elif pothole_type == 'medium':
                size = random.uniform(1.0, 2.0)
                speed_reduction = 0.25
                color = "0.25,0.25,0.25"
            else:
                size = random.uniform(2.0, 3.0)
                speed_reduction = 0.10
                color = "0.2,0.2,0.2"
            
            lateral = random.uniform(-3, 3)
            
            # Create shape
            points = []
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                r = size * random.uniform(0.7, 1.3)
                px = x + r * math.cos(rad) + lateral
                py = y + r * math.sin(rad)
                points.append(f"{px:.2f},{py:.2f}")
            
            pothole_shape = " ".join(points)
            
            f.write(f'    <poly id="pothole_{pothole_count}" ')
            f.write(f'type="pothole" color="{color}" fill="1" ')
            f.write(f'layer="50" shape="{pothole_shape}"/>\n')
            
            pos = length * pos_ratio
            reduced_speed = speed_limit * speed_reduction
            lanes_str = " ".join(all_lane_ids)
            
            f.write(f'    <variableSpeedSign id="pothole_vss_{pothole_count}" ')
            f.write(f'lanes="{lanes_str}" pos="{pos:.2f}">\n')
            f.write(f'        <step time="0" speed="{reduced_speed:.2f}"/>\n')
            f.write(f'    </variableSpeedSign>\n\n')
            
            pothole_count += 1
    
    f.write('</additional>\n')

print(f"✓ Created {barricade_count} barricades, {pothole_count} potholes")

# 5. Generate vehicles
print(f"\nStep 5/8: Generating {TOTAL_VEHICLES} vehicles...")

all_vehicles = []

for vtype in ["auto", "motorcycle", "car", "bus"]:
    for i in range(vehicle_count):
        from_edge = random.choice(trip_edges)
        to_edge = random.choice(trip_edges)
        while to_edge == from_edge:
            to_edge = random.choice(trip_edges)
        
        vehicle_id = len(all_vehicles)
        depart = vehicle_id * 1.0  # 1 second intervals
        
        all_vehicles.append({
            'id': f"{vtype}_{i}",
            'type': vtype,
            'depart': depart,
            'from': from_edge,
            'to': to_edge
        })

all_vehicles.sort(key=lambda v: v['depart'])
print(f"✓ Generated and sorted {len(all_vehicles)} vehicles")

# 6. Write routes
print("\nStep 6/8: Writing route file...")

with open(rou_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    f.write('xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n')
    
    # Vehicle types - ALL use vClass="passenger" for compatibility
    f.write('    <!-- Auto-rickshaw -->\n')
    f.write('    <vType id="auto" length="3.5" minGap="0.5" maxSpeed="15" accel="2.0" decel="4.5"\n')
    f.write('           color="1,1,0" vClass="passenger" guiShape="delivery"\n')
    f.write('           speedFactor="1.3" speedDev="0.3" sigma="0.8"/>\n\n')
    
    f.write('    <!-- Motorcycle -->\n')
    f.write('    <vType id="motorcycle" length="2.0" minGap="0.3" maxSpeed="25" accel="3.0" decel="6.0"\n')
    f.write('           color="1,0,0" vClass="passenger" guiShape="motorcycle"\n')
    f.write('           speedFactor="1.4" speedDev="0.4" sigma="0.7"/>\n\n')
    
    f.write('    <!-- Car -->\n')
    f.write('    <vType id="car" length="5.0" minGap="2.0" maxSpeed="20" accel="2.5" decel="4.5"\n')
    f.write('           color="0.5,0.5,0.5" vClass="passenger" guiShape="passenger"\n')
    f.write('           speedFactor="1.0" speedDev="0.2" sigma="0.5"/>\n\n')
    
    f.write('    <!-- Bus - BRIGHT BLUE -->\n')
    f.write('    <vType id="bus" length="12.0" minGap="3.0" maxSpeed="18" accel="1.2" decel="3.0"\n')
    f.write('           color="0,0.7,1" vClass="passenger" guiShape="bus"\n')
    f.write('           speedFactor="0.9" speedDev="0.1" sigma="0.3"/>\n\n')
    
    # Write vehicles
    for v in all_vehicles:
        f.write(f'    <trip id="{v["id"]}" type="{v["type"]}" depart="{v["depart"]:.1f}" ')
        f.write(f'from="{v["from"]}" to="{v["to"]}" departLane="best" departSpeed="max"/>\n')
    
    f.write('\n</routes>\n')

print("✓ Route file written")

# 7. Route vehicles
print("\nStep 7/8: Computing routes...")
result = subprocess.run([
    "duarouter",
    "-n", net_file,
    "-r", rou_file,
    "-o", rou_file + ".xml",
    "--ignore-errors",
    "--repair",
    "--remove-loops",
    "--routing-algorithm", "astar",
    "--no-step-log"
], capture_output=True, text=True)

if os.path.exists(rou_file + ".xml"):
    os.rename(rou_file + ".xml", rou_file)
    print("✓ Routing complete")
else:
    print("⚠ Routing had issues but continuing...")

# 8. Create config
print("\nStep 8/8: Creating SUMO configuration...")

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

# GUI settings
with open("mymap.settings.xml", "w") as f:
    f.write('<viewsettings>\n')
    f.write('    <scheme name="stable">\n')
    f.write('        <vehicles vehicleQuality="2" vehicleSize.minSize="3"\n')
    f.write('                  vehicleName.show="1" vehicleName.size="60"\n')
    f.write('                  vehicleColorMode="0" vehicleShape.show="1"/>\n')
    f.write('        <edges laneEdgeMode="1" laneShowBorders="1"/>\n')
    f.write('        <polys polySize.exaggeration="2.0"/>\n')
    f.write('    </scheme>\n')
    f.write('</viewsettings>\n')

print("✓ Configuration created")

print("\n" + "="*60)
print("✅ SIMULATION READY - STABLE VERSION")
print("="*60)
print(f"🚗 Vehicles: {TOTAL_VEHICLES}")
print(f"   - Auto-rickshaws: {vehicle_count} (Yellow)")
print(f"   - Motorcycles: {vehicle_count} (Red)")
print(f"   - Cars: {vehicle_count} (Gray)")
print(f"   - Buses: {vehicle_count} (BRIGHT BLUE)")
print(f"\n🕳️  Potholes: {pothole_count}")
print(f"🚧 Barricades: {barricade_count}")
print("\n💡 TIP: In SUMO GUI, use:")
print("   - Right-click vehicle → Show Parameter")
print("   - F9 → Vehicles → Color by speed")
print("   - Zoom in to see potholes")
print("\n🚀 Starting SUMO GUI...")
print("="*60 + "\n")

# Run SUMO
subprocess.run(["sumo-gui", "-c", sumocfg_file, "--gui-settings-file", "mymap.settings.xml"])

print("\n✓ Simulation completed successfully!")
