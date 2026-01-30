# JustATowerDefence
An unlimited Tower Defence game powered by Pygame.

## Description
A classic tower defence game where you must strategically place towers to defend against waves of enemies. Build towers, upgrade your defenses, and survive as many waves as possible!

## Features
- **Strategic Tower Placement**: Place towers along the path to defend against enemies
- **Wave-based Gameplay**: Face increasingly difficult waves of enemies
- **Resource Management**: Earn money by defeating enemies and spend it wisely on towers
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
- **Sell Button**: Sell the selected tower for money

### Game Rules
- You start with $200 and 20 lives
- Towers cost $50 to build and sell for $25
- Each enemy that reaches the end costs you 1 life
- Defeat enemies to earn money
- Survive as many waves as possible!

### Tips
- Place towers strategically along the path
- Don't place towers too close to the path or other towers
- Save money for later waves when enemies get tougher
- Use the tower range indicator to optimize placement

## Game Elements

### Towers
- **Cost**: $50
- **Damage**: 20
- **Range**: 100 pixels
- **Fire Rate**: Every 30 frames

### Enemies
- **Health**: 100 (increases with each wave)
- **Speed**: 2 pixels per frame
- **Reward**: $10 (increases with each wave)

## Technical Details
- Built with Python and Pygame
- Resolution: 800x600
- Frame Rate: 60 FPS

## License
See LICENSE file for details.
