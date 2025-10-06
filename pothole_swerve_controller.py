#!/usr/bin/env python3
"""
Pothole Swerve Controller using TraCI
Vehicles detect potholes ahead, slow down, swerve laterally to avoid them, then return to lane center.
Uses XY coordinate-based detection for true lateral avoidance.
"""

import os
import sys
import traci
import xml.etree.ElementTree as ET
import math

# Add SUMO tools to path
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please set SUMO_HOME environment variable")

import sumolib

def load_potholes(obstacles_file, net_file):
    """Load pothole positions and calculate XY coordinates"""
    potholes_by_lane = {}
    potholes_xy = []  # List of (x, y, radius, type) for XY-based detection
    
    try:
        tree = ET.parse(obstacles_file)
        root = tree.getroot()
        net = sumolib.net.readNet(net_file)
    except Exception as e:
        print(f"Error loading files: {e}")
        return potholes_by_lane, potholes_xy
    
    for poly in root.findall('poly'):
        poly_id = poly.get('id', '')
        poly_type = poly.get('type', '')
        
        if not poly_id.startswith('pothole_'):
            continue
        
        speed_mult = 0.01  # 99% speed reduction
        shape_str = poly.get('shape', '')
        
        if not shape_str:
            continue
        
        try:
            coords = []
            for point in shape_str.split():
                x, y = map(float, point.split(','))
                coords.append((x, y))
            
            if not coords:
                continue
            
            # Calculate polygon center
            center_x = sum(x for x, y in coords) / len(coords)
            center_y = sum(y for x, y in coords) / len(coords)
            
            # Store XY coordinate pothole (2.5m radius for hit detection)
            potholes_xy.append((center_x, center_y, 2.5, poly_type))
            
            # Also map to nearest lane for ahead detection
            nearest_lane = None
            min_dist = float('inf')
            
            for edge in net.getEdges():
                for lane in edge.getLanes():
                    lane_shape = lane.getShape()
                    for lx, ly in lane_shape:
                        dist = ((center_x - lx)**2 + (center_y - ly)**2)**0.5
                        if dist < min_dist:
                            min_dist = dist
                            nearest_lane = lane
            
            if nearest_lane and min_dist < 50.0:
                lane_id = nearest_lane.getID()
                lane_shape = nearest_lane.getShape()
                
                # Project pothole onto lane to get position
                closest_point_idx = 0
                min_point_dist = float('inf')
                for idx, (lx, ly) in enumerate(lane_shape):
                    dist = ((center_x - lx)**2 + (center_y - ly)**2)**0.5
                    if dist < min_point_dist:
                        min_point_dist = dist
                        closest_point_idx = idx
                
                # Calculate lane position
                lane_length = nearest_lane.getLength()
                if len(lane_shape) > 1:
                    dist_along = sum(
                        ((lane_shape[i+1][0] - lane_shape[i][0])**2 + 
                         (lane_shape[i+1][1] - lane_shape[i][1])**2)**0.5
                        for i in range(min(closest_point_idx, len(lane_shape)-2))
                    )
                    pothole_pos = min(dist_along, lane_length - 1)
                else:
                    pothole_pos = lane_length / 2
                
                if lane_id not in potholes_by_lane:
                    potholes_by_lane[lane_id] = []
                potholes_by_lane[lane_id].append((pothole_pos, speed_mult, poly_type, center_x, center_y))
        
        except Exception as e:
            print(f"Error processing pothole {poly_id}: {e}")
            continue
    
    print(f"Loaded {len(potholes_xy)} potholes at XY coordinates")
    return potholes_by_lane, potholes_xy

def run_simulation(sumo_config):
    """Run SUMO simulation with pothole swerve avoidance"""
    
    # Load potholes
    obstacles_file = sumo_config.replace('.sumocfg', '.obstacles.xml')
    net_file = sumo_config.replace('.sumocfg', '.net.xml')
    potholes_by_lane, potholes_xy = load_potholes(obstacles_file, net_file)
    
    # Start TraCI with GUI
    traci.start(["sumo-gui", "-c", sumo_config])
    
    # Tracking dictionaries
    vehicle_original_speeds = {}
    vehicle_pothole_hit_time = {}
    vehicle_in_pothole_zone = {}
    vehicle_slowed_for_pothole = {}
    vehicle_swerved_for_pothole = {}
    vehicle_swerve_time = {}
    vehicle_original_lane = {}
    
    # Constants
    RECOVERY_TIME = 50  # 5 seconds to recover from pothole
    SWERVE_RETURN_DELAY = 80  # 8 seconds swerved before returning
    POTHOLE_DETECTION_DISTANCE = 150.0  # Look ahead 150m (increased for earlier detection)
    SLOWDOWN_START_DISTANCE = 100.0  # Slow at 100m (earlier)
    SWERVE_START_DISTANCE = 90.0  # Swerve at 90m (earlier)
    MIN_SWERVE_DISTANCE = 70.0  # Must be 70m+ away (earlier)
    SLOWDOWN_SPEED = 8.0  # Slow to 8 m/s
    SWERVE_OFFSET = 4.0  # Swerve 4m laterally (reduced to stay within lane)
    POTHOLE_HIT_RADIUS = 2.0  # Hit if within 2.0m (vehicle width ~2m + pothole radius ~1.3m = ~3.3m, but 2.0m for center-to-center)
    
    step = 0
    try:
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step += 1
            
            vehicle_ids = traci.vehicle.getIDList()
            
            for veh_id in vehicle_ids:
                try:
                    # Store original max speed
                    if veh_id not in vehicle_original_speeds:
                        vehicle_original_speeds[veh_id] = traci.vehicle.getMaxSpeed(veh_id)
                    
                    original_max = vehicle_original_speeds[veh_id]
                    current_speed = traci.vehicle.getSpeed(veh_id)
                    
                    # Recovery from pothole hit
                    if veh_id in vehicle_pothole_hit_time:
                        if step - vehicle_pothole_hit_time[veh_id] >= RECOVERY_TIME:
                            traci.vehicle.setSpeed(veh_id, -1)  # Resume normal
                            traci.vehicle.setMaxSpeed(veh_id, original_max)
                            del vehicle_pothole_hit_time[veh_id]
                            if veh_id in vehicle_in_pothole_zone:
                                del vehicle_in_pothole_zone[veh_id]
                        continue
                    
                    # Return to lane center after swerve
                    if veh_id in vehicle_swerve_time:
                        if step - vehicle_swerve_time[veh_id] >= SWERVE_RETURN_DELAY:
                            try:
                                # Return to lane center (lateral position 0)
                                traci.vehicle.setLateralLanePosition(veh_id, 0.0)
                                traci.vehicle.setMaxSpeed(veh_id, original_max)
                                
                                print(f"Step {step}: Vehicle {veh_id} RETURNED to lane center")
                                
                                del vehicle_swerve_time[veh_id]
                                if veh_id in vehicle_swerved_for_pothole:
                                    del vehicle_swerved_for_pothole[veh_id]
                                if veh_id in vehicle_slowed_for_pothole:
                                    del vehicle_slowed_for_pothole[veh_id]
                                if veh_id in vehicle_original_lane:
                                    del vehicle_original_lane[veh_id]
                            except Exception as e:
                                print(f"Return to center failed for {veh_id}: {e}")
                        continue
                    
                    # Get vehicle position
                    edge_id = traci.vehicle.getRoadID(veh_id)
                    if edge_id.startswith(':'):  # Skip junctions
                        continue
                    
                    lane_idx = traci.vehicle.getLaneIndex(veh_id)
                    lane_id = f"{edge_id}_{lane_idx}"
                    lane_pos = traci.vehicle.getLanePosition(veh_id)
                    veh_x, veh_y = traci.vehicle.getPosition(veh_id)
                    
                    # Check for potholes ahead on current lane
                    if lane_id in potholes_by_lane:
                        pothole_ahead = None
                        pothole_distance = float('inf')
                        
                        for pothole_pos, speed_mult, ptype, px, py in potholes_by_lane[lane_id]:
                            distance = pothole_pos - lane_pos
                            
                            if 0 < distance < POTHOLE_DETECTION_DISTANCE:
                                if distance < pothole_distance:
                                    pothole_ahead = (pothole_pos, speed_mult, ptype, px, py)
                                    pothole_distance = distance
                        
                        # STEP 1: Slowdown when approaching
                        if pothole_ahead and pothole_distance < SLOWDOWN_START_DISTANCE:
                            pothole_pos, speed_mult, ptype, px, py = pothole_ahead
                            
                            if veh_id not in vehicle_slowed_for_pothole or vehicle_slowed_for_pothole[veh_id] != (px, py):
                                if current_speed > SLOWDOWN_SPEED:
                                    traci.vehicle.slowDown(veh_id, SLOWDOWN_SPEED, 1.0)
                                    print(f"Step {step}: Vehicle {veh_id} SLOWING DOWN to {SLOWDOWN_SPEED} m/s - pothole at {pothole_distance:.1f}m")
                                vehicle_slowed_for_pothole[veh_id] = (px, py)
                        
                        # STEP 2: Swerve laterally
                        if pothole_ahead and MIN_SWERVE_DISTANCE < pothole_distance < SWERVE_START_DISTANCE:
                            pothole_pos, speed_mult, ptype, px, py = pothole_ahead
                            
                            if veh_id not in vehicle_swerved_for_pothole or vehicle_swerved_for_pothole[veh_id] != (px, py):
                                try:
                                    lane_shape = traci.lane.getShape(lane_id)
                                    lane_length = traci.lane.getLength(lane_id)
                                    lane_width = traci.lane.getWidth(lane_id)
                                    
                                    if lane_length > 0 and len(lane_shape) >= 2:
                                        # Calculate current position on lane
                                        pos_ratio = min(lane_pos / lane_length, 1.0)
                                        x1, y1 = lane_shape[0]
                                        x2, y2 = lane_shape[-1]
                                        center_x = x1 + (x2 - x1) * pos_ratio
                                        center_y = y1 + (y2 - y1) * pos_ratio
                                        
                                        # Calculate perpendicular vector
                                        dx = x2 - x1
                                        dy = y2 - y1
                                        length = math.sqrt(dx*dx + dy*dy)
                                        
                                        if length > 0:
                                            # Normalize and get perpendicular
                                            dx_norm = dx / length
                                            dy_norm = dy / length
                                            perp_x = -dy_norm
                                            perp_y = dx_norm
                                            
                                            # Determine swerve direction - check which side is safer
                                            num_lanes = traci.edge.getLaneNumber(edge_id)
                                            
                                            # Check both swerve directions for other potholes
                                            # We need to check the entire swerved path, not just target point
                                            left_safe = True
                                            right_safe = True
                                            
                                            # Check multiple points along the swerved path
                                            test_distances = [0, 20, 40, 60, 80]  # Check at 0m, 20m, 40m, 60m, 80m ahead
                                            SAFETY_MARGIN = 4.0  # Need 4m clearance from any pothole
                                            
                                            for test_dist in test_distances:
                                                # Calculate test position ahead
                                                test_ratio = min((lane_pos + test_dist) / lane_length, 1.0) if lane_length > 0 else 0
                                                test_cx = x1 + (x2 - x1) * test_ratio
                                                test_cy = y1 + (y2 - y1) * test_ratio
                                                
                                                test_left_x = test_cx + perp_x * SWERVE_OFFSET
                                                test_left_y = test_cy + perp_y * SWERVE_OFFSET
                                                test_right_x = test_cx - perp_x * SWERVE_OFFSET
                                                test_right_y = test_cy - perp_y * SWERVE_OFFSET
                                                
                                                # Check potholes near swerve path
                                                for test_px, test_py, test_radius, test_ptype in potholes_xy:
                                                    left_dist = math.sqrt((test_left_x - test_px)**2 + (test_left_y - test_py)**2)
                                                    right_dist = math.sqrt((test_right_x - test_px)**2 + (test_right_y - test_py)**2)
                                                    
                                                    if left_dist < SAFETY_MARGIN:
                                                        left_safe = False
                                                    if right_dist < SAFETY_MARGIN:
                                                        right_safe = False
                                            
                                            # Choose safer direction
                                            if not left_safe and not right_safe:
                                                # Both sides blocked - STOP HARD instead of swerving into another pothole
                                                traci.vehicle.slowDown(veh_id, 1.0, 2.0)
                                                print(f"Step {step}: Vehicle {veh_id} BLOCKED - both sides have potholes within {SAFETY_MARGIN}m, hard brake at {pothole_distance:.1f}m")
                                                continue
                                            elif right_safe and not left_safe:
                                                swerve_dir = -SWERVE_OFFSET  # Right is safer
                                            elif left_safe and not right_safe:
                                                swerve_dir = SWERVE_OFFSET  # Left is safer
                                            elif lane_idx > 0 or lane_width > 4.0:
                                                swerve_dir = -SWERVE_OFFSET  # Both safe, prefer right
                                            else:
                                                swerve_dir = SWERVE_OFFSET  # Both safe, default left
                                            
                                            # Apply swerve using lateral lane position (MUCH simpler and works!)
                                            # Positive = left, Negative = right from lane center
                                            lateral_offset = swerve_dir  # 4.0m or -4.0m
                                            
                                            try:
                                                traci.vehicle.setLateralLanePosition(veh_id, lateral_offset)
                                                
                                                # Verify it worked
                                                actual_lateral = traci.vehicle.getLateralLanePosition(veh_id)
                                                
                                                print(f"Step {step}: Vehicle {veh_id} SWERVED {abs(lateral_offset):.1f}m {'RIGHT' if lateral_offset < 0 else 'LEFT'} - lateral position: {actual_lateral:.2f}m from center")
                                            except traci.exceptions.TraCIException as e:
                                                # Fallback: just slow down if lateral movement fails
                                                traci.vehicle.slowDown(veh_id, 2.0, 1.0)
                                                print(f"Step {step}: Vehicle {veh_id} lateral swerve failed ({e}), slowing to 2 m/s")
                                            
                                            vehicle_swerved_for_pothole[veh_id] = (px, py)
                                            vehicle_swerve_time[veh_id] = step
                                            vehicle_original_lane[veh_id] = lane_idx
                                
                                except Exception as e:
                                    print(f"Swerve failed for {veh_id}: {e}")
                    
                    # Check for pothole HITS using XY distance
                    for px, py, radius, ptype in potholes_xy:
                        xy_dist = math.sqrt((veh_x - px)**2 + (veh_y - py)**2)
                        
                        if xy_dist < POTHOLE_HIT_RADIUS:
                            if veh_id not in vehicle_in_pothole_zone:
                                # HIT!
                                target_speed = max(0.5, original_max * 0.01)
                                traci.vehicle.setSpeed(veh_id, target_speed)
                                vehicle_pothole_hit_time[veh_id] = step
                                vehicle_in_pothole_zone[veh_id] = (px, py)
                                print(f"Step {step}: Vehicle {veh_id} HIT {ptype} pothole at XY dist {xy_dist:.1f}m - speed drop {current_speed:.1f} -> {target_speed:.1f} m/s")
                            break
                    
                    # Clear zone if left
                    if veh_id in vehicle_in_pothole_zone and veh_id not in vehicle_pothole_hit_time:
                        px, py = vehicle_in_pothole_zone[veh_id]
                        xy_dist = math.sqrt((veh_x - px)**2 + (veh_y - py)**2)
                        if xy_dist >= POTHOLE_HIT_RADIUS:
                            del vehicle_in_pothole_zone[veh_id]
                
                except traci.exceptions.TraCIException:
                    # Vehicle left simulation
                    for d in [vehicle_in_pothole_zone, vehicle_pothole_hit_time, vehicle_original_speeds,
                             vehicle_slowed_for_pothole, vehicle_swerved_for_pothole, vehicle_swerve_time]:
                        if veh_id in d:
                            del d[veh_id]
                    continue
    
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    finally:
        traci.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='mymap.sumocfg', help='SUMO config file')
    args = parser.parse_args()
    
    run_simulation(args.config)
