#!/usr/bin/env python3
"""
SIMPLE INDIAN ROAD POTHOLE AVOIDANCE
=====================================
Clean, straightforward logic:
1. Detect pothole ahead (within 100m)
2. Slow down gradually
3. Dodge laterally if there's space (setLateralLanePosition)
4. Return to center after passing
5. If hit, enforce 99% speed loss for 5 seconds

Key Features:
- 4 Indian vehicle types (bus, car, motorbike, auto)
- Small potholes with 99% speed reduction
- 5-second recovery after hits
- Realistic lateral dodging when space available
- Simple, clean code - no over-engineering
"""

import os
import sys
import traci
import math
from collections import defaultdict

# Add SUMO tools to Python path
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")

# ============================================================================
# CONFIGURATION - Simple and Clear
# ============================================================================

# Detection & Avoidance
DETECTION_RANGE = 80.0      # Look 80m ahead for potholes
SLOWDOWN_DISTANCE = 60.0    # Start slowing at 60m
DODGE_DISTANCE = 40.0       # Start dodging at 40m (earlier to have time)
DODGE_OFFSET = 1.5          # Dodge 1.5m laterally (max safe for 3.5m lanes)
ROAD_WIDTH_BUFFER = 0.2     # Stay 0.2m from road edge (tight Indian driving!)
HIT_RADIUS = 1.3            # Vehicle must be within 1.3m of pothole center to hit (tighter)

# Speed Control
SLOWDOWN_SPEED = 5.0        # Slow to 5 m/s when approaching pothole
HIT_SPEED = 0.5             # Force 0.5 m/s for 5 seconds after hit (99% reduction)
HIT_RECOVERY_TIME = 50      # 50 steps = 5 seconds @ 10 steps/sec

# Vehicle States
NORMAL = 'normal'
SLOWING = 'slowing'
DODGING = 'dodging'
RETURNING = 'returning'
RECOVERING = 'recovering'  # After hit

# ============================================================================
# GLOBAL STATE
# ============================================================================

potholes = []               # List of all potholes {x, y}
vehicle_states = {}         # {vid: {'state': NORMAL, 'target_pothole': None, ...}}
hit_vehicles = {}           # {vid: recovery_counter}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_potholes():
    """Load pothole coordinates from obstacles file"""
    global potholes
    
    # Try fewer potholes version first, fall back to original
    obstacles_file = 'mymap_few_potholes.obstacles.xml'
    if not os.path.exists(obstacles_file):
        obstacles_file = 'mymap.obstacles.xml'
    
    if not os.path.exists(obstacles_file):
        print(f"WARNING: {obstacles_file} not found!")
        return
    
    import xml.etree.ElementTree as ET
    tree = ET.parse(obstacles_file)
    root = tree.getroot()
    
    for poly in root.findall('poly'):
        if 'pothole' in poly.get('type', '').lower():
            shape = poly.get('shape', '')
            if shape:
                # Parse polygon points and get center
                points = []
                for coord_pair in shape.split():
                    x, y = map(float, coord_pair.split(','))
                    points.append((x, y))
                
                if points:
                    # Calculate center of polygon
                    cx = sum(p[0] for p in points) / len(points)
                    cy = sum(p[1] for p in points) / len(points)
                    potholes.append({'x': cx, 'y': cy})
    
    print(f"✓ Loaded {len(potholes)} potholes from {obstacles_file}")


def distance(x1, y1, x2, y2):
    """Calculate Euclidean distance"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def get_potholes_ahead(vx, vy, vangle, lane_width):
    """
    Find potholes ahead of vehicle within detection range.
    Returns list of potholes sorted by distance.
    """
    potholes_ahead = []
    
    # Convert angle to radians
    angle_rad = math.radians(vangle)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    
    for pothole in potholes:
        px, py = pothole['x'], pothole['y']
        
        # Vector from vehicle to pothole
        dx = px - vx
        dy = py - vy
        
        # Project onto vehicle's heading direction
        forward_dist = dx * cos_a + dy * sin_a
        lateral_dist = abs(-dx * sin_a + dy * cos_a)
        
        # Check if pothole is ahead and within lane
        if forward_dist > 0 and forward_dist < DETECTION_RANGE:
            if lateral_dist < lane_width / 2 + 1.0:  # Within lane plus buffer
                potholes_ahead.append({
                    'pothole': pothole,
                    'forward_dist': forward_dist,
                    'lateral_dist': lateral_dist
                })
    
    # Sort by forward distance
    potholes_ahead.sort(key=lambda p: p['forward_dist'])
    return potholes_ahead


def can_dodge(vx, vy, vangle, lateral_offset, edge_id, lane_width, target_pothole):
    """
    Check if vehicle can dodge laterally without going off road.
    Returns True if safe to dodge.
    
    Indian driving style: We only check if we'd hit the IMMEDIATE area,
    not every pothole in existence (too strict).
    """
    # Check road boundaries
    max_offset = (lane_width / 2) - ROAD_WIDTH_BUFFER
    
    if abs(lateral_offset) > max_offset:
        # print(f"    DEBUG: Can't dodge - offset {lateral_offset:.1f}m exceeds max {max_offset:.1f}m (lane width {lane_width}m)")
        return False
    
    # Calculate dodge position (simplified - just check lateral displacement)
    # Convert angle to radians
    angle_rad = math.radians(vangle)
    
    # Check only potholes in the IMMEDIATE dodge area (next 40m forward)
    # This is more realistic - we're dodging ONE pothole, not avoiding all of them
    blocking_potholes = 0
    for pothole in potholes:
        # Skip the target pothole itself
        if pothole == target_pothole:
            continue
            
        px, py = pothole['x'], pothole['y']
        
        # Check if this pothole is in our dodge path
        # Use simple forward/lateral distance check
        dx = px - vx
        dy = py - vy
        
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        forward_dist = dx * cos_a + dy * sin_a
        lateral_dist = -dx * sin_a + dy * cos_a
        
        # Only check potholes in the immediate dodge zone (next 40m)
        if 0 < forward_dist < 40:
            # Check if pothole would be hit at dodge offset
            if abs(lateral_dist - lateral_offset) < HIT_RADIUS + 0.5:
                blocking_potholes += 1
                # print(f"    DEBUG: Pothole at forward={forward_dist:.1f}m, lateral={lateral_dist:.1f}m blocks offset {lateral_offset:.1f}m")
                return False  # Would hit this pothole while dodging
    
    # print(f"    DEBUG: Can dodge at offset {lateral_offset:.1f}m (no blocking potholes in 40m)")
    return True


def check_pothole_hit(vid, vx, vy):
    """
    Check if vehicle has hit a pothole.
    Returns True if hit detected.
    """
    for pothole in potholes:
        dist = distance(vx, vy, pothole['x'], pothole['y'])
        if dist < HIT_RADIUS:
            return True
    return False


# ============================================================================
# MAIN CONTROL LOGIC
# ============================================================================

def control_vehicle(vid):
    """
    Main control logic for each vehicle - SIMPLE & CLEAN
    """
    global vehicle_states, hit_vehicles
    
    # Initialize vehicle state
    if vid not in vehicle_states:
        vehicle_states[vid] = {
            'state': NORMAL,
            'target_pothole': None,
            'original_speed': None
        }
    
    state = vehicle_states[vid]
    
    # Get vehicle info
    try:
        vx, vy = traci.vehicle.getPosition(vid)
        vangle = traci.vehicle.getAngle(vid)
        speed = traci.vehicle.getSpeed(vid)
        edge_id = traci.vehicle.getRoadID(vid)
        lane_id = traci.vehicle.getLaneID(vid)
        lane_index = traci.vehicle.getLaneIndex(vid)
        
        # Skip if vehicle not on proper road
        if edge_id.startswith(':'):
            return
        
        # Get lane width
        lane_width = traci.lane.getWidth(lane_id)
        
    except traci.exceptions.TraciException:
        return
    
    # ========================================================================
    # PRIORITY 1: Handle recovery after hitting pothole
    # ========================================================================
    if vid in hit_vehicles:
        if hit_vehicles[vid] > 0:
            traci.vehicle.setSpeed(vid, HIT_SPEED)
            hit_vehicles[vid] -= 1
            if hit_vehicles[vid] == 0:
                print(f"  [{vid}] ✓ RECOVERED from pothole hit")
                del hit_vehicles[vid]
                state['state'] = RETURNING
        return
    
    # Check for new pothole hit
    if check_pothole_hit(vid, vx, vy):
        if vid not in hit_vehicles:
            print(f"  [{vid}] ✗ HIT POTHOLE at ({vx:.1f}, {vy:.1f}) - 99% speed loss for 5 seconds!")
            hit_vehicles[vid] = HIT_RECOVERY_TIME
            state['state'] = RECOVERING
            return
    
    # ========================================================================
    # PRIORITY 2: Return to center after dodging
    # ========================================================================
    if state['state'] == RETURNING:
        current_lateral = traci.vehicle.getLateralLanePosition(vid)
        
        if abs(current_lateral) < 0.3:
            # Successfully returned to center
            traci.vehicle.setSpeed(vid, -1)  # Resume normal speed
            state['state'] = NORMAL
            state['target_pothole'] = None
            print(f"  [{vid}] → Returned to center, resuming normal driving")
        else:
            # Keep moving toward center
            traci.vehicle.setLateralLanePosition(vid, 0.0)
        return
    
    # ========================================================================
    # PRIORITY 3: Find potholes ahead and decide action
    # ========================================================================
    potholes_ahead = get_potholes_ahead(vx, vy, vangle, lane_width)
    
    if not potholes_ahead:
        # No potholes ahead - normal driving
        if state['state'] != NORMAL:
            traci.vehicle.setSpeed(vid, -1)  # Resume normal speed
            state['state'] = NORMAL
            state['target_pothole'] = None
        return
    
    # Get closest pothole
    closest = potholes_ahead[0]
    forward_dist = closest['forward_dist']
    
    # ========================================================================
    # PRIORITY 4: Execute avoidance maneuver
    # ========================================================================
    
    if forward_dist < DODGE_DISTANCE and state['state'] != DODGING:
        # Try to dodge!
        # Determine dodge direction - dodge AWAY from pothole
        # If pothole is to the right (lateral_dist > 0), dodge LEFT (negative offset)
        # If pothole is to the left (lateral_dist < 0), dodge RIGHT (positive offset)
        lateral_dist = closest['lateral_dist']
        primary_offset = -DODGE_OFFSET if lateral_dist > 0 else DODGE_OFFSET
        alternate_offset = -primary_offset
        
        # Try primary direction first
        if can_dodge(vx, vy, vangle, primary_offset, edge_id, lane_width, closest['pothole']):
            traci.vehicle.setLateralLanePosition(vid, primary_offset)
            state['state'] = DODGING
            state['target_pothole'] = closest['pothole']
            direction = "LEFT" if primary_offset < 0 else "RIGHT"
            print(f"  [{vid}] ↔ DODGING {direction} (offset: {primary_offset:.1f}m) for pothole {forward_dist:.1f}m ahead")
        # Try alternate direction
        elif can_dodge(vx, vy, vangle, alternate_offset, edge_id, lane_width, closest['pothole']):
            traci.vehicle.setLateralLanePosition(vid, alternate_offset)
            state['state'] = DODGING
            state['target_pothole'] = closest['pothole']
            direction = "LEFT" if alternate_offset < 0 else "RIGHT"
            print(f"  [{vid}] ↔ DODGING {direction} (offset: {alternate_offset:.1f}m, alternate) for pothole {forward_dist:.1f}m ahead")
        else:
            # Can't dodge either way - just slow down
            traci.vehicle.setSpeed(vid, SLOWDOWN_SPEED)
            state['state'] = SLOWING
            print(f"  [{vid}] ↓ SLOWING for pothole {forward_dist:.1f}m ahead (can't dodge either way)")



    
    elif forward_dist < SLOWDOWN_DISTANCE and state['state'] == NORMAL:
        # Start slowing down
        traci.vehicle.setSpeed(vid, SLOWDOWN_SPEED)
        state['state'] = SLOWING
        state['target_pothole'] = closest['pothole']
        if state['original_speed'] is None:
            state['original_speed'] = speed
        print(f"  [{vid}] ↓ SLOWING for pothole {forward_dist:.1f}m ahead")
    
    elif state['state'] == DODGING:
        # Check if we've passed the pothole
        if state['target_pothole']:
            px, py = state['target_pothole']['x'], state['target_pothole']['y']
            dist_to_target = distance(vx, vy, px, py)
            
            if dist_to_target > DODGE_DISTANCE:
                # Passed it - start returning to center
                state['state'] = RETURNING
                print(f"  [{vid}] ← Passed pothole, returning to center")


# ============================================================================
# SIMULATION MAIN LOOP
# ============================================================================

def run_simulation():
    """Main simulation loop"""
    print("\n" + "="*70)
    print("SIMPLE INDIAN ROAD POTHOLE AVOIDANCE - Starting Simulation")
    print("="*70 + "\n")
    
    # Load potholes
    load_potholes()
    
    if len(potholes) == 0:
        print("ERROR: No potholes loaded!")
        return
    
    # Start SUMO
    sumo_binary = "sumo-gui"  # Use GUI for visualization
    sumo_cmd = [sumo_binary, "-c", "mymap.sumocfg", "--start"]
    
    traci.start(sumo_cmd)
    step = 0
    
    print("\n🚗 Simulation running... Watch vehicles dodge potholes!\n")
    
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1
            
            # Control all vehicles
            for vid in traci.vehicle.getIDList():
                control_vehicle(vid)
            
            # Progress indicator every 100 steps
            if step % 100 == 0:
                num_vehicles = len(traci.vehicle.getIDList())
                num_recovering = len(hit_vehicles)
                print(f"Step {step}: {num_vehicles} vehicles active, {num_recovering} recovering from hits")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Simulation interrupted by user")
    
    finally:
        traci.close()
        
        print("\n" + "="*70)
        print("SIMULATION COMPLETE")
        print("="*70)
        print(f"\nTotal steps: {step}")
        print(f"Total vehicles: {len(vehicle_states)}")
        print("\n✓ Check the SUMO GUI to see dodging behavior")
        print("✓ Vehicles should slow down, dodge laterally, and return to center")


if __name__ == "__main__":
    run_simulation()
