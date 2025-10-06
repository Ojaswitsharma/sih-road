#!/usr/bin/env python3
"""Quick test to show pothole density"""
import xml.etree.ElementTree as ET

# Count potholes
tree = ET.parse("mymap.obstacles.xml")
root = tree.getroot()
potholes = [poly for poly in root.findall('.//poly') if 'pothole' in poly.get('type', '')]
print(f"Total potholes: {len(potholes)}")

# Get road network stats
import sumolib
net = sumolib.net.readNet("mymap.net.xml")
edges = [e for e in net.getEdges() if not e.getID().startswith(':')]
total_length = sum(e.getLength() for e in edges)
print(f"Total road length: {total_length:.0f}m")
print(f"Pothole density: {len(potholes) / (total_length/1000):.1f} potholes per km")
print(f"Average distance between potholes: {total_length / len(potholes):.1f}m")
print()
print("This is WHY vehicles can't avoid - potholes every ~50m means constant dodging!")
