"""
Configuration file for Tower Defence game
Contains all game constants and settings
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)

# Game settings
INITIAL_MONEY = 200
INITIAL_LIVES = 20
TOWER_COST = 50
TOWER_SELL_VALUE = 25

# Tower settings
TOWER_DAMAGE = 20
TOWER_RANGE = 100
TOWER_FIRE_RATE = 30  # frames between shots
TOWER_MAX_LEVEL = 3
TOWER_UPGRADE_COST = 40
TOWER_UPGRADE_DAMAGE_BONUS = 10
TOWER_UPGRADE_RANGE_BONUS = 20
TOWER_UPGRADE_FIRE_RATE_BONUS = 5  # lower is faster

# Enemy settings
ENEMY_SPEED = 2
ENEMY_HEALTH = 100
ENEMY_REWARD = 10

# Wave settings
INITIAL_ENEMIES_PER_WAVE = 5
ENEMIES_INCREMENT = 3  # additional enemies per wave

# UI settings
SIDEBAR_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_PADDING = 10
