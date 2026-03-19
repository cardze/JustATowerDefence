# JustATowerDefence
An unlimited Tower Defence game powered by Pygame.

## Description
A classic tower defence game where you must strategically place towers to defend against waves of enemies. Build different types of towers, upgrade your defenses, and survive as many waves as possible! Features multiple enemy types, diverse tower options, and dynamic difficulty scaling.

## Features
- **Multiple Tower Types**: Choose from 4 different tower types with unique abilities
- **Diverse Enemy Types**: Face 4 different enemy types including bosses
- **Tower Upgrades**: Upgrade towers up to level 3 to increase damage, range, and fire rate
- **Wave-based Gameplay**: Face increasingly difficult waves of enemies
- **Dynamic Path Complexity**: Paths become more challenging every 5 waves
- **Game Speed Scaling**: Speed increases as you defeat enemies for progressive difficulty
- **Resource Management**: Earn money by defeating enemies and spend it wisely on towers
- **Strategic Tower Placement**: Place towers along the path to defend against enemies
- **Comprehensive Logging**: All game events are logged for debugging and analysis
- **Simple Controls**: Easy to learn, challenging to master

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cardze/JustATowerDefence.git
cd JustATowerDefence
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python main.py
```

## Project Structure

The runtime code now lives under the `tower_defence/` package:

- `tower_defence/app/`: game loop and application flow
- `tower_defence/core/`: shared configuration constants
- `tower_defence/entities/`: enemies and projectiles
- `tower_defence/towers/`: towers, builders, and tower states
- `tower_defence/combat/`: attack strategies
- `tower_defence/systems/`: event system and observers

The repository-root `main.py` remains as a compatibility entry point that launches `tower_defence.app.main`.

### Controls
- **Tower Type Buttons (B/S/R/C)**: Click to select tower type before building
- **Left Click**: Place a tower in the game area
- **Right Click**: Select a tower  
- **Start Next Wave Button**: Begin the next wave of enemies
- **Upgrade Button**: Upgrade the selected tower (if available)
- **Sell Button**: Sell the selected tower for money

### Game Rules
- You start with $200 and 20 lives
- Different tower types have different costs and abilities
- Each enemy that reaches the end costs you 1 life
- Defeat enemies to earn money
- Game speed increases by 1% per enemy killed (up to 3x)
- Paths change every 5 waves for increased challenge
- Boss enemies appear every 10 waves
- Survive as many waves as possible!

### Tips
- Choose the right tower type for your strategy
- Sniper towers excel at long-range single targets
- Rapid towers are great for fast enemies
- Cannon towers deal area damage to groups
- Upgrade towers instead of building too many to save space
- Save money for later waves when enemies get tougher
- Use the tower range indicator to optimize placement
- Watch the logs (tower_defence.log) to analyze your strategy

## Game Elements

### Tower Types

#### Basic Tower (Blue)
- **Cost**: $50 | **Sell**: $25
- **Damage**: 20 | **Range**: 100 | **Fire Rate**: 30 frames
- **Upgrade Cost**: $40 per level | **Max Level**: 3
- Balanced all-around tower, good for starting

#### Sniper Tower (Purple)
- **Cost**: $80 | **Sell**: $40
- **Damage**: 50 | **Range**: 200 | **Fire Rate**: 60 frames
- **Upgrade Cost**: $50 per level | **Max Level**: 3
- Long-range specialist, perfect for picking off enemies early

#### Rapid Tower (Orange)
- **Cost**: $60 | **Sell**: $30
- **Damage**: 10 | **Range**: 80 | **Fire Rate**: 15 frames
- **Upgrade Cost**: $35 per level | **Max Level**: 3
- Fast firing tower, excellent against fast enemies

#### Cannon Tower (Dark Red)
- **Cost**: $100 | **Sell**: $50
- **Damage**: 35 | **Range**: 120 | **Fire Rate**: 45 frames
- **AoE Radius**: 40 pixels (50% damage to nearby enemies)
- **Upgrade Cost**: $60 per level | **Max Level**: 3
- Area of effect damage, devastating against groups

### Enemy Types

#### Basic Enemy (Red)
- **Health**: 100 (+ 20 per wave)
- **Speed**: 2 pixels per frame
- **Reward**: $10 (+ $2 per wave)
- Standard enemy, appears in all waves

#### Fast Enemy (Yellow)
- **Health**: 60 (+ 20 per wave)
- **Speed**: 4 pixels per frame
- **Reward**: $15 (+ $2 per wave)
- Quick and agile, starts appearing from wave 3

#### Tank Enemy (Gray)
- **Health**: 200 (+ 20 per wave)
- **Speed**: 1 pixel per frame
- **Reward**: $25 (+ $2 per wave)
- Slow but heavily armored, starts appearing from wave 7

#### Boss Enemy (Purple)
- **Health**: 500 (+ 20 per wave)
- **Speed**: 1.5 pixels per frame
- **Reward**: $100 (+ $2 per wave)
- Powerful boss, appears every 10 waves

### Game Speed Scaling
- Base speed: 1.0x
- Increases by 1% per enemy killed
- Maximum speed: 3.0x
- Applies to all enemy movement
- Creates progressive difficulty

### Paths
- Paths change every 5 waves
- 4 different complex path patterns
- Progressively more challenging layouts

## Logging

The game logs all important events to `tower_defence.log`:
- Game initialization
- Tower placement and upgrades
- Wave starts and completions
- Enemy kills and escapes
- Money and lives changes
- Path complexity changes

## Technical Details
- Built with Python and Pygame
- Resolution: 800x600
- Frame Rate: 60 FPS
- Comprehensive logging system
- Dynamic path generation
- Source layout organized under the `tower_defence/` package for clearer module boundaries

## License
See LICENSE file for details.
