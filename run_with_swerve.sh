#!/bin/bash
# Run SUMO simulation with pothole swerve avoidance

echo "Starting SUMO simulation with swerve avoidance..."
echo "Vehicles will:"
echo "  1. Detect potholes 100m ahead"
echo "  2. Slow down at 80m"
echo "  3. Swerve laterally 6m at 50-70m to avoid"
echo "  4. Return to center after 8 seconds"
echo ""
echo "Watch the console output to see swerving behavior!"
echo "Press Ctrl+C to stop"
echo ""

python3 pothole_swerve_controller.py --config mymap.sumocfg
