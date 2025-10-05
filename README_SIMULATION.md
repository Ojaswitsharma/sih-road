# Indian Road Traffic Simulation - Enhanced Features

## Overview
This SUMO simulation has been enhanced to realistically simulate Indian road conditions with diverse vehicle types and common road obstacles.

## Vehicle Types (4 Types)

### 1. **Auto-rickshaw** (Yellow)
- **Color**: Yellow
- **Max Speed**: 13.89 m/s (~50 km/h)
- **Length**: 3.0 m
- **Acceleration**: 1.5 m/s²
- **Characteristics**: Small, slow, highly maneuverable, common in Indian cities
- **Behavior**: Higher lane-changing strategic value (1.5), lower cooperation (0.5) - tends to weave through traffic

### 2. **Motorcycle/Scooter** (Red)
- **Color**: Red
- **Max Speed**: 25.0 m/s (~90 km/h)
- **Length**: 2.0 m
- **Acceleration**: 3.0 m/s²
- **Characteristics**: Fast, agile, can weave through traffic
- **Behavior**: Very high lane-changing strategic value (2.0), very low cooperation (0.3) - aggressive lane changes

### 3. **Car** (White)
- **Color**: White
- **Max Speed**: 33.33 m/s (~120 km/h)
- **Length**: 5.0 m
- **Acceleration**: 2.6 m/s²
- **Characteristics**: Medium speed, standard behavior
- **Behavior**: Balanced lane-changing (1.0), balanced cooperation (1.0) - follows rules

### 4. **Bus/Truck** (Blue)
- **Color**: Blue
- **Max Speed**: 19.44 m/s (~70 km/h)
- **Length**: 12.0 m
- **Acceleration**: 1.0 m/s²
- **Characteristics**: Large, slow, less maneuverable
- **Behavior**: Low lane-changing strategic value (0.5), high cooperation (1.5) - stays in lane mostly

## Vehicle Distribution (Indian Traffic Mix)
- **40%** Motorcycles/Scooters
- **30%** Cars
- **20%** Auto-rickshaws
- **10%** Buses/Trucks

This distribution reflects typical Indian urban traffic patterns where two-wheelers dominate.

## Road Obstacles

### 1. **Barricades** (Orange polygons)
- **Visual**: Orange rectangular shapes on roads
- **Count**: Up to 5 randomly placed on different roads
- **Purpose**: Simulates construction zones, police barricades, or temporary road blocks
- **Effect**: Visual obstruction, forces lane changes

### 2. **Potholes** (Speed reduction zones)
- **Visual**: Not directly visible (implemented as variable speed signs)
- **Count**: Up to 5 randomly placed on different roads
- **Purpose**: Simulates the impact of poor road conditions
- **Effect**: 40% speed reduction when vehicles pass through these zones
- **Behavior**: Vehicles slow down at specific positions simulating potholes

## How Vehicle Types Differ

### Speed Characteristics
- **Fastest**: Car (120 km/h max) → Motorcycle (90 km/h) → Bus (70 km/h) → Auto-rickshaw (50 km/h)

### Acceleration
- **Quickest**: Motorcycle (3.0 m/s²) → Car (2.6 m/s²) → Auto-rickshaw (1.5 m/s²) → Bus (1.0 m/s²)

### Size & Maneuverability
- **Smallest**: Motorcycle (2m) → Auto-rickshaw (3m) → Car (5m) → Bus (12m)
- **Most Agile**: Motorcycle → Auto-rickshaw → Car → Bus

### Lane Changing Behavior
- **Most Aggressive**: Motorcycle (weaves through traffic)
- **Strategic**: Auto-rickshaw (opportunistic lane changes)
- **Balanced**: Car (follows rules)
- **Conservative**: Bus (stays in lane)

## Files Generated

1. **mymap.vtypes.xml** - Vehicle type definitions with all parameters
2. **mymap.obstacles.xml** - Barricades and pothole definitions
3. **mymap.rou.xml** - Modified routes with vehicle type assignments
4. **mymap.sumocfg** - Updated configuration including all additional files

## Running the Simulation

Simply run:
```bash
python3 osm_to_sim.py
```

The script will:
1. Convert OSM map to SUMO network
2. Generate polygons
3. Create vehicle type definitions
4. Generate road obstacles (barricades & potholes)
5. Generate random trips with mixed vehicle classes
6. Assign vehicle types to match Indian traffic distribution
7. Launch SUMO GUI

## Visual Guide

In SUMO GUI, you'll see:
- **Yellow vehicles**: Auto-rickshaws (slow, small, weaving)
- **Red vehicles**: Motorcycles (fast, aggressive, lane-changing)
- **White vehicles**: Cars (medium speed, balanced behavior)
- **Blue vehicles**: Buses/Trucks (large, slow, lane-keeping)
- **Orange rectangles**: Barricades/Road blocks
- **Speed changes on road**: Potholes (vehicles slow down)

## Realistic Indian Road Behavior

The simulation captures:
1. **Mixed traffic**: Diverse vehicle types with different speeds
2. **Aggressive motorcycles**: Weaving through traffic
3. **Slow auto-rickshaws**: Maneuvering in tight spaces
4. **Large buses**: Taking up more space, slower acceleration
5. **Road obstacles**: Barricades forcing detours
6. **Poor road conditions**: Potholes causing speed reductions
7. **Traffic distribution**: 70% two/three-wheelers (motorcycles + auto-rickshaws)

This creates a realistic simulation of Indian urban road conditions!
