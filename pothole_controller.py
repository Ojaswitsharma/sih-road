#!/usr/bin/env python3
"""
Pothole Speed Controller using TraCI
This script runs the SUMO simulation and forces vehicles to slow down instantly when they hit potholes.
"""

import os
import sys
import traci
import xml.etree.ElementTree as ET

# Add SUMO tools to path
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please set SUMO_HOME environment variable")

import sumolib

# Load pothole data from obstacles file
def load_potholes(obstacles_file, net_file):
    """Load pothole positions from obstacles.xml and map them to lanes"""
    potholes = {}
    
    # Parse obstacles file to get pothole polygons
    try:
        tree = ET.parse(obstacles_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error loading obstacles file: {e}")
        return potholes
    
    # Load network to get lane information
    try:
        net = sumolib.net.readNet(net_file)
    except Exception as e:
        print(f"Error loading network file: {e}")
        return potholes
    
    pothole_count = 0
    skipped_count = 0
    
    for poly in root.findall('poly'):
        poly_id = poly.get('id', '')
        poly_type = poly.get('type', '')
        
        # Only process pothole polygons
        if not poly_id.startswith('pothole_'):
            continue
            
        # Get speed multiplier based on type
        # ALL potholes are now DEEP PURPLE with 99% speed reduction (instant drop to 1% of speed for 5 seconds)
        speed_mult = 0.01  # Always 99% reduction for all potholes - holds for 5 seconds then recovers
        
        # Get polygon shape (x,y coordinates)
        shape_str = poly.get('shape', '')
        if not shape_str:
            skipped_count += 1
            continue
            
        try:
            # Parse shape to get center point
            coords = []
            for point in shape_str.split():
                x, y = map(float, point.split(','))
                coords.append((x, y))
            
            if not coords:
                skipped_count += 1
                continue
                
            # Calculate polygon center
            center_x = sum(x for x, y in coords) / len(coords)
            center_y = sum(y for x, y in coords) / len(coords)
            
            # Find nearest lane to this pothole
            nearest_lane = None
            min_dist = float('inf')
            
            for edge in net.getEdges():
                for lane in edge.getLanes():
                    # Get lane shape (list of (x,y) points)
                    lane_shape = lane.getShape()
                    
                    # Find closest point on lane to pothole center
                    for lx, ly in lane_shape:
                        dist = ((center_x - lx)**2 + (center_y - ly)**2)**0.5
                        if dist < min_dist:
                            min_dist = dist
                            nearest_lane = lane
            
            # Only add pothole if we found a nearby lane (within 50m)
            if nearest_lane and min_dist < 50.0:
                lane_id = nearest_lane.getID()
                
                # Project pothole center onto lane to get position along lane
                lane_shape = nearest_lane.getShape()
                closest_point_idx = 0
                min_point_dist = float('inf')
                
                for i, (lx, ly) in enumerate(lane_shape):
                    dist = ((center_x - lx)**2 + (center_y - ly)**2)**0.5
                    if dist < min_point_dist:
                        min_point_dist = dist
                        closest_point_idx = i
                
                # Calculate position along lane
                pothole_pos = 0.0
                for i in range(closest_point_idx):
                    x1, y1 = lane_shape[i]
                    x2, y2 = lane_shape[i + 1]
                    pothole_pos += ((x2 - x1)**2 + (y2 - y1)**2)**0.5
                
                # Add to potholes dict
                if lane_id not in potholes:
                    potholes[lane_id] = []
                potholes[lane_id].append((pothole_pos, speed_mult, poly_type))
                pothole_count += 1
            else:
                skipped_count += 1
                
        except Exception as e:
            print(f"Error processing pothole {poly_id}: {e}")
            skipped_count += 1
            continue
    
    print(f"Loaded {pothole_count} potholes on {len(potholes)} lanes")
    if skipped_count > 0:
        print(f"Skipped {skipped_count} potholes (no nearby lane or parsing error)")
    
    return potholes

# Main simulation loop
def run_simulation(sumocfg_file, obstacles_file, net_file):
    """Run SUMO with pothole speed control"""
    
    print("Loading pothole data...")
    potholes = load_potholes(obstacles_file, net_file)
    print(f"Loaded {sum(len(v) for v in potholes.values())} pothole zones across {len(potholes)} lanes")
    
    # Start SUMO with GUI
    sumo_binary = "sumo-gui"
    sumo_cmd = [sumo_binary, "-c", sumocfg_file]
    
    print("Starting SUMO simulation...")
    traci.start(sumo_cmd)
    
    # Track original max speeds for each vehicle
    vehicle_original_speeds = {}
    vehicle_pothole_hit_time = {}  # Track when vehicle hit pothole (step number)
    vehicle_in_pothole_zone = {}  # Track if vehicle is currently in pothole detection zone
    
    RECOVERY_TIME = 50  # 5 seconds at 0.1s per step = 50 steps
    
    step = 0
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1
            
            # Get all vehicles in simulation
            vehicle_ids = traci.vehicle.getIDList()
            
            for veh_id in vehicle_ids:
                try:
                    # Store original max speed for this vehicle
                    if veh_id not in vehicle_original_speeds:
                        vehicle_original_speeds[veh_id] = traci.vehicle.getMaxSpeed(veh_id)
                    
                    # Get vehicle position
                    lane_id = traci.vehicle.getLaneID(veh_id)
                    lane_pos = traci.vehicle.getLanePosition(veh_id)
                    current_speed = traci.vehicle.getSpeed(veh_id)
                    original_max = vehicle_original_speeds[veh_id]
                    
                    # Check if vehicle is recovering from pothole (5-second timer)
                    if veh_id in vehicle_pothole_hit_time:
                        steps_since_hit = step - vehicle_pothole_hit_time[veh_id]
                        
                        if steps_since_hit < RECOVERY_TIME:
                            # Still in 5-second recovery period - keep at 1% speed
                            target_speed = max(0.5, original_max * 0.01)  # 99% reduction
                            traci.vehicle.setSpeed(veh_id, target_speed)
                        else:
                            # 5 seconds passed - allow normal acceleration
                            traci.vehicle.setSpeed(veh_id, -1)  # Resume normal driving
                            print(f"Step {step}: Vehicle {veh_id} recovered from pothole, resuming normal speed")
                            del vehicle_pothole_hit_time[veh_id]
                            if veh_id in vehicle_in_pothole_zone:
                                del vehicle_in_pothole_zone[veh_id]
                        continue
                    
                    # Check if vehicle is on a lane with potholes
                    if lane_id in potholes:
                        # Check each pothole on this lane
                        in_any_pothole = False
                        
                        for pothole_pos, speed_mult, ptype in potholes[lane_id]:
                            # Pothole zone is 10m (±5m from center)
                            if abs(lane_pos - pothole_pos) < 5.0:
                                in_any_pothole = True
                                
                                # If vehicle just entered pothole zone, trigger instant slowdown
                                if veh_id not in vehicle_in_pothole_zone:
                                    # INSTANT 99% speed reduction
                                    target_speed = max(0.5, original_max * 0.01)
                                    traci.vehicle.setSpeed(veh_id, target_speed)
                                    
                                    # Mark hit time and zone
                                    vehicle_pothole_hit_time[veh_id] = step
                                    vehicle_in_pothole_zone[veh_id] = (lane_id, pothole_pos)
                                    
                                    print(f"Step {step}: Vehicle {veh_id} hit {ptype} pothole at pos {lane_pos:.1f}, INSTANT drop {current_speed:.1f} -> {target_speed:.1f} m/s (99% reduction, holding 5 seconds)")
                                break
                        
                        # If vehicle left pothole zone without hitting, clear zone marker
                        if not in_any_pothole and veh_id in vehicle_in_pothole_zone and veh_id not in vehicle_pothole_hit_time:
                            del vehicle_in_pothole_zone[veh_id]
                
                except traci.exceptions.TraCIException as e:
                    # Vehicle might have left simulation
                    if veh_id in vehicle_in_pothole_zone:
                        del vehicle_in_pothole_zone[veh_id]
                    if veh_id in vehicle_pothole_hit_time:
                        del vehicle_pothole_hit_time[veh_id]
                    if veh_id in vehicle_original_speeds:
                        del vehicle_original_speeds[veh_id]
                    continue
    
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    except Exception as e:
        print(f"\nError in simulation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        traci.close()
        print("Simulation complete!")

if __name__ == "__main__":
    sumocfg_file = "mymap.sumocfg"
    obstacles_file = "mymap.obstacles.xml"
    net_file = "mymap.net.xml"
    
    run_simulation(sumocfg_file, obstacles_file, net_file)
