# 🤖 AI Agent Modes - Indian Road Simulation

## Overview
The simulation now supports 5 different AI behavior modes that control how vehicles drive!

---

## 🎯 AI Modes Explained

### 1. RANDOM Mode 🎲
**Best for:** Unpredictable chaos, testing edge cases

**Features:**
- 30% of auto-rickshaws reroute dynamically every 60 seconds
- Random driving parameters for each vehicle
- Highly unpredictable behavior
- Maximum variety in driving styles

**Vehicle Behavior:**
- SpeedFactor: 0.7 - 1.8 (random)
- Assertiveness: 0.5 - 3.0 (random)
- Impatience: 0.1 - 1.0 (random)

---

### 2. CONSERVATIVE Mode 🐢
**Best for:** Calm traffic, rule-following simulation

**Features:**
- All vehicles drive carefully
- Respect lane discipline
- Lower speeds
- Less overtaking

**Vehicle Parameters:**
- SpeedFactor: 0.8 (20% slower)
- Assertiveness: 0.3 (very passive)
- Impatience: 0.1 (very patient)
- Sigma: 0.3 (low randomness)

---

### 3. AGGRESSIVE Mode 🏎️
**Best for:** Rush hour chaos, maximum overtaking

**Features:**
- Fast, risky driving
- Constant lane changes
- Heavy overtaking
- High-speed maneuvering

**Vehicle Parameters:**
- SpeedFactor: 1.5 (50% faster!)
- Assertiveness: 3.0 (very aggressive)
- Impatience: 1.0 (maximum impatience)
- Sigma: 0.9 (high randomness)

---

### 4. MIXED Mode 🌈 (RECOMMENDED)
**Best for:** Realistic Indian traffic, variety

**Features:**
- 3 variants per vehicle type (12 total types!)
- Combines all behaviors
- Most realistic simulation
- Different vehicles have different personalities

**Vehicle Variants:**

#### Auto-rickshaws:
- `auto` - Normal (rash driving)
- `auto_calm` - Careful driver
- `auto_crazy` - Extreme aggressive

#### Motorcycles:
- `motorcycle` - Normal (erratic)
- `motorcycle_safe` - Defensive driving
- `motorcycle_racer` - Speed demon

#### Cars:
- `car` - Normal speed
- `car_cautious` - Slow and safe
- `car_sporty` - Fast and aggressive

#### Buses:
- `bus` - Normal (slow)
- `bus_express` - Faster express bus
- `bus_local` - Very slow local bus

---

### 5. DEFAULT Mode ⚙️
**Best for:** Standard SUMO behavior, baseline comparison

**Features:**
- Standard vehicle type definitions
- No AI modifications
- Baseline behavior
- Good for testing

---

## 🚗 Vehicle Colors

All modes maintain color consistency:

| Vehicle Type | Color | Visual |
|--------------|-------|--------|
| Auto-rickshaw | Yellow | 🟡 |
| Motorcycle | Red | 🔴 |
| Car | Gray | ⚫ |
| Bus | Blue | 🔵 |

---

## 📍 Route Distribution

All modes use improved route distribution:

- **40% Short trips** - Nearby destinations (local traffic)
- **40% Long trips** - Far destinations (through traffic)
- **20% Random/Varied** - Mixed routes

**RANDOM Mode Bonus:**
- 30% of autos reroute every 60 seconds
- Creates dynamic traffic patterns

---

## 🎮 How to Use

### Start Simulation
```bash
python3 indian_road_sim.py
```

### Select AI Mode
You'll see:
```
Choose AI agent behavior for vehicles:
1. RANDOM     - Autos change routes randomly, chaos!
2. CONSERVATIVE - Careful driving, follow rules
3. AGGRESSIVE - Fast, risky, lots of overtaking
4. MIXED      - Combination of all behaviors (realistic)
5. DEFAULT    - Standard SUMO behavior

Enter choice (1-5) [default: 4]:
```

### Recommendations

**For Realistic Indian Roads:** Choose **4 (MIXED)**
- Best variety
- Most realistic
- Different driver personalities

**For Testing Chaos:** Choose **1 (RANDOM)**
- Maximum unpredictability
- Dynamic rerouting
- Edge case testing

**For Rush Hour:** Choose **3 (AGGRESSIVE)**
- High-speed chaos
- Constant overtaking
- Heavy traffic interactions

**For Calm Traffic:** Choose **2 (CONSERVATIVE)**
- Smooth flow
- Rule-following
- Low stress simulation

---

## 🔍 Viewing Different Behaviors

### In SUMO GUI:

1. **Right-click any vehicle** → "Show Parameter"
   - See its type (auto, auto_calm, auto_crazy, etc.)
   - View current behavior parameters

2. **Track vehicles** to see behavior differences:
   - Track a `motorcycle_racer` - watch it weave aggressively
   - Track a `car_cautious` - see it drive slowly
   - Track an `auto_crazy` - experience chaos!

3. **Color by speed** (Press F9):
   - Conservative mode: Mostly yellow/green (slower)
   - Aggressive mode: Mostly green/blue (faster)
   - Mixed mode: Full spectrum

---

## 💡 Pro Tips

### Get Maximum Chaos
```
Mode: RANDOM (1)
+ 1000 vehicles
+ Potholes active
+ Barricades blocking lanes
= ULTIMATE CHAOS! 🔥
```

### Get Realistic Indian Traffic
```
Mode: MIXED (4)
+ Varied routes
+ Different vehicle personalities
+ Real driving behaviors
= AUTHENTIC SIMULATION 🇮🇳
```

### Test Performance
```
Mode: CONSERVATIVE (2)
+ Smooth traffic flow
+ Less collisions
+ Easier to debug
= STABLE TESTING ✅
```

---

## 📊 Statistics by Mode

| Mode | Avg Speed | Lane Changes | Overtakes | Collisions |
|------|-----------|--------------|-----------|------------|
| Conservative | Low | Low | Rare | Very Rare |
| Aggressive | High | Very High | Frequent | Common |
| Mixed | Medium | High | Common | Occasional |
| Random | Variable | Random | Random | Unpredictable |
| Default | Medium | Medium | Moderate | Rare |

---

## 🛠️ Customization

Want to create your own AI mode? Edit `indian_road_sim.py`:

```python
# Add your custom mode
if ai_mode == "custom":
    params = {
        "speedFactor": 1.2,      # Your speed
        "lcAssertive": 1.5,      # Your aggression
        "lcImpatience": 0.5,     # Your patience
        "sigma": 0.6             # Your randomness
    }
```

---

## ❓ FAQ

**Q: Which mode is fastest?**
A: AGGRESSIVE (mode 3) - vehicles drive 50% faster!

**Q: Which mode has most variety?**
A: MIXED (mode 4) - 12 different vehicle types!

**Q: Which mode is most realistic for India?**
A: MIXED (mode 4) - combines all behaviors like real traffic

**Q: Can I change mode mid-simulation?**
A: No, restart the simulation and select a new mode

**Q: Do potholes work in all modes?**
A: Yes! All modes have 99% speed reduction in potholes

---

## 🚀 Quick Start Commands

```bash
# Realistic Indian traffic
python3 indian_road_sim.py
# Select: 4 (MIXED)

# Maximum chaos
python3 indian_road_sim.py
# Select: 1 (RANDOM)

# Rush hour simulation
python3 indian_road_sim.py
# Select: 3 (AGGRESSIVE)
```

---

**Enjoy your enhanced simulation!** 🇮🇳🚗💨
