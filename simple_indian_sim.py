#!/usr/bin/env python3
"""
Simple & Efficient Indian Road Simulation
- No parallel processing overhead
- Controlled pothole generation
- Heavy traffic without lag
- Logging system for debugging
"""

import os
import subprocess
import xml.etree.ElementTree as ET
import random
import math
import sys
import time
from datetime import datetime

# Files
osm_file = "mymap.osm"
net_file = "mymap.net.xml"
poly_file = "mymap.poly.xml"
rou_file = "mymap.rou.xml"
sumocfg_file = "mymap.sumocfg"
add_file = "mymap.add.xml"
log_file = "simulation.log"

SUMO_HOME = os.environ.get("SUMO_HOME", "/usr/share/sumo")

# Logging function
def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_msg = f"[{timestamp}] {level}: {message}"
    print(log_msg)
    with open(log_file, "a") as f:
        f.write(log_msg + "\n")

# Start fresh log
with open(log_file, "w") as f:
    f.write(f"=== Simulation Log Started at {datetime.now()} ===\n\n")

log("Starting Indian Road Simulation")

# AI MODE
print("\n" + "="*60)
print("🚗 INDIAN ROAD SIMULATION (Optimized)")
print("="*60)
print("\nChoose AI agent behavior:")
print("1. RANDOM     - Autos reroute randomly")
print("2. CONSERVATIVE - Careful driving")
print("3. AGGRESSIVE - Fast, risky driving")
print("4. MIXED      - Realistic variety (RECOMMENDED)")
print("5. DEFAULT    - Standard behavior")
print()

while True:
    choice = input("Enter choice (1-5) [default: 4]: ").strip() or "4"
    if choice in ["1", "2", "3", "4", "5"]:
        break
    print("Invalid choice!")

AI_MODE = {
    "1": "random",
    "2": "conservative", 
    "3": "aggressive",
    "4": "mixed",
    "5": "default"
}[choice]

log(f"AI Mode selected: {AI_MODE}")

# Vehicle count
print("\nHow many vehicles per type?")
print("  100 = Light traffic (400 total)")
print("  250 = Medium traffic (1000 total)")
print("  500 = Heavy traffic (2000 total) - May lag!")
while True:
    try:
        vehicle_count = int(input("Enter count [default: 250]: ").strip() or "250")
        if vehicle_count > 0:
            break
    except:
        pass

TOTAL_VEHICLES = vehicle_count * 4
log(f"Vehicle count: {vehicle_count} per type = {TOTAL_VEHICLES} total")

# Pothole density - EXTREME MODE
print("\nPothole density:")
print("  1 = Light (10-20 per road)")
print("  2 = Medium (25-40 per road)")
print("  3 = Heavy (50-80 per road)")
print("  4 = EXTREME (100-150 per road) - Road damage!")
while True:
    density = input("Enter density (1-4) [default: 3]: ").strip() or "3"
    if density in ["1", "2", "3", "4"]:
        break

POTHOLE_DENSITY = {
    "1": (10, 20),
    "2": (25, 40),
    "3": (50, 80),
    "4": (100, 150)
}[density]
log(f"Pothole density: {POTHOLE_DENSITY[0]}-{POTHOLE_DENSITY[1]} per road")

print("\n" + "="*60 + "\n")

# 1. Convert OSM
log("Converting OSM to SUMO network...")
start_time = time.time()
subprocess.run([
    "netconvert",
    "--osm-files", osm_file,
    "--type-files", os.path.join(SUMO_HOME, "data/typemap/osmNetconvert.typ.xml"),
    "--output-file", net_file,
    "--geometry.remove", "--ramps.guess", "--junctions.join",
    "--tls.guess-signals", "--tls.discard-simple", 
    "--tls.join", "--tls.default-type", "actuated"
], capture_output=True, text=True)
log(f"Network conversion took {time.time() - start_time:.2f}s")

# 2. Generate polygons
log("Generating polygons...")
start_time = time.time()
subprocess.run([
    "polyconvert",
    "--osm-files", osm_file,
    "--net-file", net_file,
    "--type-file", os.path.join(SUMO_HOME, "data/typemap/osmPolyconvert.typ.xml"),
    "-o", poly_file
], capture_output=True, text=True)
log(f"Polygon generation took {time.time() - start_time:.2f}s")

# 3. Parse network
log("Parsing network...")
start_time = time.time()
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

log(f"Found {len(all_edges)} edges for potholes, {len(trip_edges)} for routing")
log(f"Parsing took {time.time() - start_time:.2f}s")

# 4. Create obstacles - CONTROLLED GENERATION
log("Creating obstacles...")
start_time = time.time()

pothole_count = 0
barricade_count = 0
small_count = 0
medium_count = 0
large_count = 0

with open(add_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<additional xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    f.write('xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/additional_file.xsd">\n\n')
    
    # BARRICADES - Limited number
    barricade_edges = random.sample(all_edges, min(50, len(all_edges)))
    
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
                
                # Yellow barricade
                barricade_shape = f"{x-6},{y-3} {x+6},{y-3} {x+6},{y+3} {x-6},{y+3}"
                f.write(f'    <poly id="barricade_{barricade_count}" type="barricade" ')
                f.write(f'color="1,0.8,0" fill="1" layer="100" shape="{barricade_shape}"/>\n')
                
                # Black stripes
                for i in range(5):
                    stripe_x = x - 5 + i * 2.5
                    stripe = f"{stripe_x},{y-3} {stripe_x+1},{y-3} {stripe_x+1},{y+3} {stripe_x},{y+3}"
                    f.write(f'    <poly id="barricade_stripe_{barricade_count}_{i}" ')
                    f.write(f'type="stripe" color="0,0,0" fill="1" layer="101" shape="{stripe}"/>\n')
                
                barricade_count += 1
    
    log(f"Created {barricade_count} barricades")
    
    # POTHOLES - COVER 1/3 OF ALL ROADS WITH HIGH DENSITY
    max_pothole_edges = int(len(all_edges) * 0.33)  # 1 out of 3 roads gets potholes
    pothole_edges = random.sample(all_edges, max_pothole_edges)
    
    log(f"Generating potholes on {max_pothole_edges} roads (1/3 of network)...")
    
    # Track bus edges for special treatment
    bus_edges = set()
    
    for edge_idx, edge in enumerate(pothole_edges):
        if edge_idx % 100 == 0:
            log(f"  Progress: {edge_idx}/{max_pothole_edges} edges processed")
        
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
        num_potholes = random.randint(*POTHOLE_DENSITY)
        
        for _ in range(num_potholes):
            pos_ratio = random.uniform(0.05, 0.95)
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
                size = random.uniform(0.4, 1.0)
                speed_reduction = 0.50
                color = "0.4,0.4,0.4"
                small_count += 1
            elif pothole_type == 'medium':
                size = random.uniform(1.0, 2.0)
                speed_reduction = 0.25
                color = "0.3,0.3,0.3"
                medium_count += 1
            else:
                size = random.uniform(2.0, 3.5)
                speed_reduction = 0.10
                color = "0.2,0.2,0.2"
                large_count += 1
            
            lateral = random.uniform(-4, 4)
            
            # Irregular shape
            points = []
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                r = size * random.uniform(0.6, 1.4)
                px = x + r * math.cos(rad) + lateral
                py = y + r * math.sin(rad)
                points.append(f"{px:.2f},{py:.2f}")
            
            pothole_shape = " ".join(points)
            
            f.write(f'    <poly id="pothole_{pothole_type}_{pothole_count}" ')
            f.write(f'type="pothole_{pothole_type}" color="{color}" fill="1" ')
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

log(f"Created {pothole_count} total potholes:")
log(f"  Small (50% reduction): {small_count}")
log(f"  Medium (75% reduction): {medium_count}")
log(f"  Large (90% reduction): {large_count}")
log(f"Obstacle generation took {time.time() - start_time:.2f}s")

# 5. Generate vehicles - SIMPLE SERIAL GENERATION
log(f"Generating {TOTAL_VEHICLES} vehicles...")
start_time = time.time()

all_vehicles = []

# Track bus routes to ensure they have potholes
bus_route_edges = []

for vtype in ["auto", "motorcycle", "car", "bus"]:
    for i in range(vehicle_count):
        # Route selection
        if vtype == "bus":
            from_edge = random.choice(trip_edges)
            far_edges = [e for e in trip_edges if e != from_edge]
            to_edge = random.choice(far_edges) if far_edges else random.choice(trip_edges)
            # Track bus edges
            bus_route_edges.append(from_edge)
            bus_route_edges.append(to_edge)
        else:
            if random.random() < 0.4:
                # Short route
                from_edge = random.choice(trip_edges)
                to_edge = random.choice(trip_edges)
            else:
                # Long route
                from_edge = random.choice(trip_edges)
                to_edge = random.choice(trip_edges)
        
        # Vehicle type for mixed mode
        if AI_MODE == "mixed":
            if vtype == "auto":
                actual_vtype = random.choice(["auto", "auto_calm", "auto_crazy"])
            elif vtype == "motorcycle":
                actual_vtype = random.choice(["motorcycle", "motorcycle_safe", "motorcycle_racer"])
            elif vtype == "car":
                actual_vtype = random.choice(["car", "car_cautious", "car_sporty"])
            else:
                actual_vtype = random.choice(["bus", "bus_express", "bus_local"])
        else:
            actual_vtype = vtype
        
        vehicle_id = len(all_vehicles)
        depart = vehicle_id * 0.5
        
        has_rerouting = (AI_MODE == "random" and vtype == "auto" and random.random() < 0.3)
        
        all_vehicles.append({
            'id': f"{vtype}_{i}",
            'type': actual_vtype,
            'depart': depart,
            'from': from_edge,
            'to': to_edge,
            'rerouting': has_rerouting
        })

# Sort by departure
all_vehicles.sort(key=lambda v: v['depart'])
log(f"Vehicle generation took {time.time() - start_time:.2f}s")

# Add extra potholes to bus routes - GUARANTEE 4+ potholes per bus route
log("Adding guaranteed potholes to bus routes...")
bus_pothole_count = 0
unique_bus_edges = list(set(bus_route_edges))
log(f"Found {len(unique_bus_edges)} unique bus route edges")

# Add to additionals file
with open(add_file, "a") as f:
    # Remove closing tag
    pass

# Rewrite with bus potholes
with open(add_file, "r") as f:
    content = f.read()

# Remove closing tag and add bus potholes
content = content.replace('</additional>', '')

with open(add_file, "w") as f:
    f.write(content)
    
    # Add 4-8 potholes to each bus edge
    for edge_id in unique_bus_edges[:min(100, len(unique_bus_edges))]:  # Limit to avoid too many
        # Find the edge
        edge = None
        for e in all_edges:
            if e.get('id') == edge_id:
                edge = e
                break
        
        if not edge:
            continue
        
        lanes = edge.findall('lane')
        if not lanes:
            continue
        
        all_lane_ids = [lane.get('id') for lane in lanes]
        first_lane = lanes[0]
        length = float(first_lane.get('length', '50'))
        shape = first_lane.get('shape')
        speed_limit = float(first_lane.get('speed', '13.89'))
        
        if not shape or length < 15:
            continue
        
        coords = shape.split()
        num_bus_potholes = random.randint(4, 8)  # Guarantee 4-8 potholes
        
        for _ in range(num_bus_potholes):
            pos_ratio = random.uniform(0.1, 0.9)
            idx = int(len(coords) * pos_ratio)
            if idx >= len(coords):
                idx = len(coords) - 1
            
            x, y = map(float, coords[idx].split(','))
            
            # Mostly medium and large potholes for buses
            pothole_type = random.choices(
                ['medium', 'large'],
                weights=[60, 40]
            )[0]
            
            if pothole_type == 'medium':
                size = random.uniform(1.5, 2.5)
                speed_reduction = 0.25
                color = "0.3,0.3,0.3"
            else:
                size = random.uniform(2.5, 4.0)
                speed_reduction = 0.10
                color = "0.2,0.2,0.2"
            
            lateral = random.uniform(-3, 3)
            
            points = []
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                r = size * random.uniform(0.7, 1.3)
                px = x + r * math.cos(rad) + lateral
                py = y + r * math.sin(rad)
                points.append(f"{px:.2f},{py:.2f}")
            
            pothole_shape = " ".join(points)
            
            f.write(f'    <poly id="bus_pothole_{bus_pothole_count}" ')
            f.write(f'type="bus_pothole" color="{color}" fill="1" ')
            f.write(f'layer="50" shape="{pothole_shape}"/>\n')
            
            pos = length * pos_ratio
            reduced_speed = speed_limit * speed_reduction
            lanes_str = " ".join(all_lane_ids)
            
            f.write(f'    <variableSpeedSign id="bus_pothole_vss_{bus_pothole_count}" ')
            f.write(f'lanes="{lanes_str}" pos="{pos:.2f}">\n')
            f.write(f'        <step time="0" speed="{reduced_speed:.2f}"/>\n')
            f.write(f'    </variableSpeedSign>\n\n')
            
            bus_pothole_count += 1
    
    f.write('</additional>\n')

log(f"Added {bus_pothole_count} guaranteed potholes to bus routes")
total_potholes = pothole_count + bus_pothole_count

# 6. Write route file
log("Writing route file...")
start_time = time.time()

with open(rou_file, "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ')
    f.write('xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n\n')
    
    # Vehicle types (mixed mode has variants)
    if AI_MODE == "mixed":
        # Auto variants
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
        
        # Motorcycle variants
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
        
        # Car variants
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
        
        # Bus variants - ENSURE THEY'RE VISIBLE WITH BRIGHT BLUE
        f.write('    <vType id="bus" length="12.0" minGap="3.0" maxSpeed="18" accel="1.0" decel="3.0"\n')
        f.write('           color="0,0.6,1" vClass="passenger" guiShape="bus"\n')
        f.write('           speedFactor="0.9" speedDev="0.1" sigma="0.3"\n')
        f.write('           lcStrategic="0.3" lcCooperative="1.5" lcSpeedGain="0.3"\n')
        f.write('           lcKeepRight="0.8" lcAssertive="0.1" lcImpatience="0.1"/>\n\n')
        
        f.write('    <vType id="bus_express" length="12.0" minGap="2.5" maxSpeed="22" accel="1.3" decel="3.5"\n')
        f.write('           color="0,0.6,1" vClass="passenger" guiShape="bus"\n')
        f.write('           speedFactor="1.1" speedDev="0.2" sigma="0.4"\n')
        f.write('           lcStrategic="0.8" lcCooperative="1.0" lcSpeedGain="0.8"\n')
        f.write('           lcKeepRight="0.6" lcAssertive="0.3" lcImpatience="0.3"/>\n\n')
        
        f.write('    <vType id="bus_local" length="12.0" minGap="3.5" maxSpeed="15" accel="0.8" decel="2.5"\n')
        f.write('           color="0,0.6,1" vClass="passenger" guiShape="bus"\n')
        f.write('           speedFactor="0.7" speedDev="0.1" sigma="0.2"\n')
        f.write('           lcStrategic="0.1" lcCooperative="2.0" lcSpeedGain="0.1"\n')
        f.write('           lcKeepRight="0.9" lcAssertive="0.0" lcImpatience="0.0"/>\n\n')
    else:
        # Standard types
        f.write('    <vType id="auto" length="3.5" minGap="0.5" maxSpeed="15" accel="2.0" decel="4.5"\n')
        f.write('           color="1,1,0" vClass="passenger" guiShape="delivery"\n')
        f.write('           speedFactor="1.3" speedDev="0.4" sigma="0.9"\n')
        f.write('           lcStrategic="3.0" lcCooperative="0.2" lcSpeedGain="3.0"\n')
        f.write('           lcKeepRight="0.1" lcAssertive="2.0" lcImpatience="0.8"/>\n\n')
        
        f.write('    <vType id="motorcycle" length="2.0" minGap="0.3" maxSpeed="30" accel="4.0" decel="7.0"\n')
        f.write('           color="1,0,0" vClass="motorcycle" guiShape="motorcycle"\n')
        f.write('           speedFactor="1.5" speedDev="0.5" sigma="0.8"\n')
        f.write('           lcStrategic="4.0" lcCooperative="0.1" lcSpeedGain="4.0"\n')
        f.write('           lcKeepRight="0.05" lcAssertive="3.0" lcImpatience="1.0"/>\n\n')
        
        f.write('    <vType id="car" length="5.0" minGap="2.0" maxSpeed="20" accel="2.5" decel="4.5"\n')
        f.write('           color="0.5,0.5,0.5" vClass="passenger" guiShape="passenger"\n')
        f.write('           speedFactor="1.0" speedDev="0.2" sigma="0.5"\n')
        f.write('           lcStrategic="1.0" lcCooperative="1.0" lcSpeedGain="1.0"\n')
        f.write('           lcKeepRight="0.5" lcAssertive="0.5" lcImpatience="0.3"/>\n\n')
        
        # BUS - BRIGHT BLUE, vClass=passenger to ensure visibility
        f.write('    <vType id="bus" length="12.0" minGap="3.0" maxSpeed="18" accel="1.0" decel="3.0"\n')
        f.write('           color="0,0.6,1" vClass="passenger" guiShape="bus"\n')
        f.write('           speedFactor="0.9" speedDev="0.1" sigma="0.3"\n')
        f.write('           lcStrategic="0.3" lcCooperative="1.5" lcSpeedGain="0.3"\n')
        f.write('           lcKeepRight="0.8" lcAssertive="0.1" lcImpatience="0.1"/>\n\n')
    
    # Write sorted vehicles
    for v in all_vehicles:
        if v['rerouting']:
            f.write(f'    <trip id="{v["id"]}" type="{v["type"]}" depart="{v["depart"]:.2f}" ')
            f.write(f'from="{v["from"]}" to="{v["to"]}" departLane="best" departSpeed="max">\n')
            f.write(f'        <param key="has.rerouting.device" value="true"/>\n')
            f.write(f'        <param key="device.rerouting.period" value="60"/>\n')
            f.write(f'    </trip>\n')
        else:
            f.write(f'    <trip id="{v["id"]}" type="{v["type"]}" depart="{v["depart"]:.2f}" ')
            f.write(f'from="{v["from"]}" to="{v["to"]}" departLane="best" departSpeed="max"/>\n')
    
    f.write('\n</routes>\n')

log(f"Route file writing took {time.time() - start_time:.2f}s")

# 7. Route vehicles
log("Computing routes...")
start_time = time.time()
subprocess.run([
    "duarouter",
    "-n", net_file,
    "-r", rou_file,
    "-o", rou_file + ".xml",
    "--ignore-errors",
    "--repair",
    "--remove-loops",
    "--routing-algorithm", "astar",
    "--no-step-log",
    "--no-warnings"
], capture_output=True, text=True)

if os.path.exists(rou_file + ".xml"):
    os.rename(rou_file + ".xml", rou_file)

log(f"Routing took {time.time() - start_time:.2f}s")

# 8. Create SUMO config
log("Creating SUMO configuration...")
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

# 9. GUI settings
log("Creating visualization settings...")
with open("mymap.settings.xml", "w") as f:
    f.write('<viewsettings>\n')
    f.write('    <scheme name="indian_sim">\n')
    f.write('        <vehicles vehicleQuality="3" vehicleSize.minSize="4" ')
    f.write('vehicleSize.exaggeration="2.0"\n')
    f.write('                  vehicleName.show="1" vehicleName.size="70" ')
    f.write('vehicleName.color="0,0,255"\n')
    f.write('                  showBlinker="1" drawMinGap="1"\n')
    f.write('                  vehicleColorMode="5" vehicleShape.show="1"/>\n')
    f.write('        <edges laneEdgeMode="1" laneShowBorders="1" streetName.show="1"/>\n')
    f.write('        <polys polySize.exaggeration="2.5" polyName.show="1"/>\n')
    f.write('        <legend showSizeLegend="1"/>\n')
    f.write('    </scheme>\n')
    f.write('</viewsettings>\n')

print("\n" + "="*60)
print("✅ SIMULATION READY!")
print("="*60)
log("Simulation setup complete")
log(f"AI Mode: {AI_MODE}")
log(f"Total vehicles: {TOTAL_VEHICLES}")
log(f"Total potholes: {total_potholes}")
log(f"Regular potholes: {pothole_count}")
log(f"Bus route potholes: {bus_pothole_count}")
log(f"Barricades: {barricade_count}")

print(f"🤖 AI Mode: {AI_MODE.upper()}")
print(f"🚗 Vehicles: {TOTAL_VEHICLES} ({vehicle_count} per type)")
print(f"🕳️  Potholes: {total_potholes} total")
print(f"   - Regular: {pothole_count}")
print(f"   - Bus routes: {bus_pothole_count} (guaranteed 4+ per route)")
print(f"   - Small (50%): {small_count}")
print(f"   - Medium (75%): {medium_count}")
print(f"   - Large (90%): {large_count}")
print(f"🚧 Barricades: {barricade_count}")
print("\n🎨 VEHICLE COLORS:")
print("  🟡 Yellow = Auto-rickshaws")
print("  🔴 Red    = Motorcycles")
print("  ⚫ Gray   = Cars")
print("  🔵 BRIGHT BLUE = Buses (vClass=passenger for visibility!)")
print(f"\n📋 Check '{log_file}' for detailed logs")
print("\n🚀 Starting SUMO GUI...")
print("="*60 + "\n")

log("Launching SUMO GUI")
subprocess.run(["sumo-gui", "-c", sumocfg_file, "--gui-settings-file", "mymap.settings.xml"])
log("Simulation ended")
