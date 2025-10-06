#!/usr/bin/env python3
"""Test if moveToXY actually moves vehicles laterally"""
import os
import sys
import traci
import math

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please set SUMO_HOME")

# Start SUMO
traci.start(["sumo", "-c", "mymap.sumocfg"])

step = 0
tests_done = 0

with open('/tmp/swerve_test.log', 'w') as f:
    f.write("Testing lateral movement with moveToXY\n")
    f.write("="*50 + "\n\n")
    
    while traci.simulation.getMinExpectedNumber() > 0 and tests_done < 5:
        traci.simulationStep()
        step += 1
        
        for veh_id in traci.vehicle.getIDList():
            try:
                # Get current position
                x1, y1 = traci.vehicle.getPosition(veh_id)
                edge_id = traci.vehicle.getRoadID(veh_id)
                
                if edge_id.startswith(':'):
                    continue
                
                # Try to move vehicle 5m to the left (perpendicular)
                lane_idx = traci.vehicle.getLaneIndex(veh_id)
                lane_id = f"{edge_id}_{lane_idx}"
                
                # Get lane direction
                lane_shape = traci.lane.getShape(lane_id)
                if len(lane_shape) < 2:
                    continue
                
                x_start, y_start = lane_shape[0]
                x_end, y_end = lane_shape[-1]
                
                # Calculate perpendicular
                dx = x_end - x_start
                dy = y_end - y_start
                length = math.sqrt(dx*dx + dy*dy)
                
                if length == 0:
                    continue
                
                dx_norm = dx / length
                dy_norm = dy / length
                perp_x = -dy_norm
                perp_y = dx_norm
                
                # Move 5m left
                new_x = x1 + perp_x * 5.0
                new_y = y1 + perp_y * 5.0
                
                # Apply move
                traci.vehicle.moveToXY(veh_id, edge_id, -1, new_x, new_y, angle=0, keepRoute=2)
                
                # Check actual position
                x2, y2 = traci.vehicle.getPosition(veh_id)
                actual_move = math.sqrt((x2-x1)**2 + (y2-y1)**2)
                
                f.write(f"Step {step}: {veh_id}\n")
                f.write(f"  Before: ({x1:.2f}, {y1:.2f})\n")
                f.write(f"  Target: ({new_x:.2f}, {new_y:.2f})\n")
                f.write(f"  After:  ({x2:.2f}, {y2:.2f})\n")
                f.write(f"  Actual movement: {actual_move:.2f}m\n")
                f.write(f"  Expected: 5.0m\n")
                f.write(f"  SUCCESS: {'YES' if actual_move > 3.0 else 'NO - moveToXY NOT WORKING!'}\n\n")
                f.flush()
                
                tests_done += 1
                if tests_done >= 5:
                    break
                    
            except Exception as e:
                f.write(f"Error: {e}\n")
                continue

traci.close()
print("Test complete! Check /tmp/swerve_test.log")
