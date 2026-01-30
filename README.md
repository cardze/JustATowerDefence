# JustATowerDefence
An unlimited Tower Defence game powered by Pygame.

## Description
A classic tower defence game where you must strategically place towers to defend against waves of enemies. Build towers, upgrade your defenses, and survive as many waves as possible!

## Features
- **Strategic Tower Placement**: Place towers along the path to defend against enemies
- **Tower Upgrades**: Upgrade towers up to level 3 to increase damage, range, and fire rate
- **Wave-based Gameplay**: Face increasingly difficult waves of enemies
- **Dynamic Path Complexity**: Paths become more challenging every 5 waves
- **Resource Management**: Earn money by defeating enemies and spend it wisely on towers
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

### Controls
- **Left Click**: Place a tower in the game area
- **Right Click**: Select a tower
- **Start Next Wave Button**: Begin the next wave of enemies
- **Upgrade Button**: Upgrade the selected tower (if available)
- **Sell Button**: Sell the selected tower for money

### Game Rules
- You start with $200 and 20 lives
- Towers cost $50 to build and sell for $25
- Towers can be upgraded up to level 3 for $40 each upgrade
- Each enemy that reaches the end costs you 1 life
- Defeat enemies to earn money
- Paths change every 5 waves for increased challenge
- Survive as many waves as possible!

### Tips
- Place towers strategically along the path
- Don't place towers too close to the path or other towers
- Upgrade towers instead of building too many to save space
- Save money for later waves when enemies get tougher
- Use the tower range indicator to optimize placement
- Watch the logs (tower_defence.log) to analyze your strategy

## Game Elements

### Towers
- **Cost**: $50 to build
- **Upgrade Cost**: $40 per level
- **Max Level**: 3
- **Level 1**: Damage: 20, Range: 100, Fire Rate: 30 frames
- **Level 2**: Damage: 30, Range: 120, Fire Rate: 25 frames
- **Level 3**: Damage: 40, Range: 140, Fire Rate: 20 frames

### Enemies
- **Health**: 100 (increases with each wave)
- **Speed**: 2 pixels per frame
- **Reward**: $10 (increases with each wave)

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

## License
See LICENSE file for details.
