#!/bin/bash

echo "======================================================================"
echo "  POTHOLE AVOIDANCE SIMULATION"
echo "======================================================================"
echo ""
echo "This simulation shows vehicles avoiding potholes by:"
echo "  1. Detecting potholes 100m ahead"
echo "  2. Slowing down at 80m distance"
echo "  3. Swerving laterally 6m at 50-70m to dodge"
echo "  4. Being FORCED to 0.5 m/s if they hit a pothole"
echo "  5. Returning to lane center after 8 seconds"
echo ""
echo "======================================================================"
echo ""

# Run the simulation with GUI
python3 pothole_swerve_controller.py --config mymap.sumocfg

echo ""
echo "Simulation ended!"
