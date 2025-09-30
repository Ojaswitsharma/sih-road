import os
import subprocess
import xml.etree.ElementTree as ET
import random

# --- SETTINGS ---
osm_file = "mymap.osm"
net_file = "mymap.net.xml"
poly_file = "mymap.poly.xml"
trips_file = "mymap.trips.xml"
rou_file = "mymap.rou.xml"
sumocfg_file = "mymap.sumocfg"

# Path to SUMO home
SUMO_HOME = os.environ.get("SUMO_HOME", "/usr/share/sumo")

# --- 1. Convert OSM to SUMO network ---
print("Converting OSM to SUMO network...")
subprocess.run([
    "netconvert",
    "--osm-files", osm_file,
    "--type-files", os.path.join(SUMO_HOME, "data/typemap/osmNetconvert.typ.xml"),
    "--output-file", net_file,
    "--geometry.remove", "--ramps.guess", "--junctions.join",
    "--tls.guess-signals", "--tls.discard-simple", "--tls.join", "--tls.default-type", "actuated", "-v"
])

# --- 2. Generate polygons (optional) ---
print("Generating polygons...")
subprocess.run([
    "polyconvert",
    "--osm-files", osm_file,
    "--net-file", net_file,
    "--type-file", os.path.join(SUMO_HOME, "data/typemap/osmPolyconvert.typ.xml"),
    "-o", poly_file
])

# --- 3. Generate random trips ---
print("Generating trips...")
subprocess.run([
    "python3", os.path.join(SUMO_HOME, "tools/randomTrips.py"),
    "-n", net_file,
    "-o", trips_file,
    "-e", "3600",  # 1 hour simulation
    "-p", "2",     # new vehicle every 2 sec on average
    "-l"           # allow loops
])

# --- 4. Convert trips to routes ---
print("Converting trips to routes...")
subprocess.run([
    "duarouter",
    "-n", net_file,
    "-t", trips_file,
    "-o", rou_file
])

# --- 5. Generate SUMO configuration ---
print("Writing SUMO config...")
with open(sumocfg_file, "w") as f:
    f.write(f"""<configuration>
    <input>
        <net-file value="{net_file}"/>
        <route-files value="{rou_file}"/>
        <additional-files value="{poly_file}"/>
    </input>
</configuration>""")

# --- 6. Run SUMO GUI ---
print("Running SUMO simulation...")
subprocess.run(["sumo-gui", "-c", sumocfg_file])
