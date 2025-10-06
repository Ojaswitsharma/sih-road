#!/bin/bash
# Simple Pothole Avoidance Simulation Runner

echo "=========================================="
echo "SIMPLE INDIAN ROAD POTHOLE AVOIDANCE"
echo "=========================================="
echo ""
echo "Features:"
echo "- 4 Indian vehicle types (bus, car, motorbike, auto)"
echo "- 200 potholes (reduced from 1571)"
echo "- 99% speed loss on hit (5-second recovery)"
echo "- Lateral dodging when space available"
echo "- Simple, clean logic"
echo ""
echo "Starting simulation..."
echo ""

python3 simple_pothole_avoidance.py 2>&1 | tee simulation_simple.log

echo ""
echo "=========================================="
echo "SIMULATION COMPLETE"
echo "=========================================="
echo ""
echo "Analyzing results..."
echo ""

# Count events
HITS=$(grep "HIT POTHOLE" simulation_simple.log | wc -l)
DODGES=$(grep "DODGING" simulation_simple.log | wc -l)
RECOVERIES=$(grep "RECOVERED" simulation_simple.log | wc -l)

echo "📊 STATISTICS:"
echo "  - Pothole hits: $HITS"
echo "  - Dodge attempts: $DODGES"
echo "  - Recoveries: $RECOVERIES"

if [ $DODGES -gt 0 ] && [ $HITS -gt 0 ]; then
    AVOIDANCE=$(echo "scale=1; ($DODGES * 100) / ($HITS + $DODGES)" | bc)
    echo "  - Avoidance rate: ${AVOIDANCE}%"
fi

echo ""
echo "✓ Full log saved to: simulation_simple.log"
echo ""
