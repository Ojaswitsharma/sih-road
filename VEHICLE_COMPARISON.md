# Vehicle Type Comparison - Indian Road Simulation

## Quick Reference Table

| Property | Auto-rickshaw | Motorcycle | Car | Bus/Truck |
|----------|--------------|------------|-----|-----------|
| **Color** | Yellow | Red | White | Blue |
| **Max Speed** | 50 km/h | 90 km/h | 120 km/h | 70 km/h |
| **Acceleration** | 1.5 m/s² | 3.0 m/s² | 2.6 m/s² | 1.0 m/s² |
| **Length** | 3.0 m | 2.0 m | 5.0 m | 12.0 m |
| **Min Gap** | 1.0 m | 0.5 m | 2.5 m | 3.0 m |
| **Lane Change** | Aggressive | Very Aggressive | Normal | Conservative |
| **Distribution** | 20% | 40% | 30% | 10% |

## Behavioral Characteristics

### Auto-rickshaw (Yellow)
- **Driving Style**: Opportunistic and maneuverable
- **Speed Factor**: 0.9 (slightly slower than limit)
- **Imperfection (Sigma)**: 0.8 (high driver imperfection)
- **Lane Strategy**: 1.5 (seeks opportunities to change lanes)
- **Cooperation**: 0.5 (low - doesn't yield much)
- **Real-world behavior**: Squeezes through gaps, sudden stops, picks up passengers

### Motorcycle (Red)
- **Driving Style**: Fast and aggressive
- **Speed Factor**: 1.1 (exceeds speed limit)
- **Imperfection (Sigma)**: 0.6 (moderate imperfection)
- **Lane Strategy**: 2.0 (very high - constantly looking to overtake)
- **Cooperation**: 0.3 (very low - cuts through traffic)
- **Real-world behavior**: Weaves through traffic, lane splitting, quick acceleration

### Car (White)
- **Driving Style**: Balanced and rule-following
- **Speed Factor**: 1.0 (follows speed limit)
- **Imperfection (Sigma)**: 0.5 (moderate imperfection)
- **Lane Strategy**: 1.0 (normal lane changing)
- **Cooperation**: 1.0 (normal - follows rules)
- **Real-world behavior**: Standard driving, follows traffic rules mostly

### Bus/Truck (Blue)
- **Driving Style**: Slow and steady
- **Speed Factor**: 0.8 (slower than limit)
- **Imperfection (Sigma)**: 0.3 (low - professional drivers)
- **Lane Strategy**: 0.5 (rarely changes lanes)
- **Cooperation**: 1.5 (high - aware of size, yields to smaller vehicles)
- **Real-world behavior**: Stays in lane, slow acceleration, cautious

## Speed Comparison (km/h)

```
Auto-rickshaw: ████████████░░░░░░░░░░░░ 50 km/h
Motorcycle:    ████████████████████░░░░ 90 km/h
Car:           ████████████████████████ 120 km/h
Bus/Truck:     ██████████████░░░░░░░░░░ 70 km/h
```

## Acceleration Comparison (m/s²)

```
Auto-rickshaw: ██████░░░░ 1.5
Motorcycle:    ████████████ 3.0
Car:           ██████████░░ 2.6
Bus/Truck:     ████░░░░░░░░ 1.0
```

## Traffic Mix (Percentage)

```
Motorcycle:     ████████████████████ 40%
Car:            ███████████████ 30%
Auto-rickshaw:  ██████████ 20%
Bus/Truck:      █████ 10%
```

## Obstacle Effects

### Barricades
- Force all vehicles to change lanes
- Create bottlenecks
- More challenging for larger vehicles (buses/trucks)

### Potholes
- Reduce speed by 40% at specific locations
- All vehicle types affected equally
- Simulate poor road conditions common in India

## Key Differences Summary

1. **Motorcycles** are the most aggressive and fastest accelerating - they weave through all traffic
2. **Auto-rickshaws** are slow but maneuverable - they exploit small gaps
3. **Cars** maintain steady speed and follow rules - standard behavior
4. **Buses/Trucks** are large and slow - they block traffic but are cautious

## Simulation Realism

The mix of 70% two/three-wheelers (motorcycles + auto-rickshaws) accurately reflects Indian traffic where:
- Two-wheelers dominate urban roads
- Cars are growing but still minority
- Buses/trucks provide public transport and logistics
- Road obstacles (barricades, potholes) are common

This creates realistic traffic scenarios with:
- Mixed speeds
- Aggressive lane changes
- Traffic congestion
- Obstacle navigation
