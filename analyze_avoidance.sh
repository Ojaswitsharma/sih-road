#!/bin/bash
# Analyze pothole avoidance effectiveness

echo "Running 60-second simulation to analyze avoidance..."
timeout 60 python3 pothole_swerve_controller.py --config mymap.sumocfg 2>&1 > /tmp/sim_test.log

HITS=$(grep "HIT pothole" /tmp/sim_test.log | wc -l)
SWERVED=$(grep "SWERVED" /tmp/sim_test.log | wc -l)
SLOWED=$(grep "SLOWING DOWN" /tmp/sim_test.log | wc -l)
BLOCKED=$(grep "BLOCKED" /tmp/sim_test.log | wc -l)

echo ""
echo "=== POTHOLE AVOIDANCE ANALYSIS ==="
echo "Hits: $HITS"
echo "Swerves: $SWERVED"  
echo "Slowdowns: $SLOWED"
echo "Blocked (both sides unsafe): $BLOCKED"
echo ""

TOTAL_ENCOUNTERS=$((HITS + SWERVED))
if [ $TOTAL_ENCOUNTERS -gt 0 ]; then
    AVOID_RATE=$((SWERVED * 100 / TOTAL_ENCOUNTERS))
    echo "Avoidance Rate: $AVOID_RATE% ($SWERVED avoided out of $TOTAL_ENCOUNTERS encounters)"
else
    echo "No pothole encounters detected"
fi

echo ""
echo "Recent activity:"
tail -30 /tmp/sim_test.log | grep -E "(HIT|SWERVED|BLOCKED|SLOWING)"
