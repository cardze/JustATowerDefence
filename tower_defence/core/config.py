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
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
DARK_RED = (139, 0, 0)

# Game settings (from README.md line 44)
INITIAL_MONEY = 200
INITIAL_LIVES = 20

# Game speed settings (Comment #2746643544)
SPEED_INCREASE_PER_KILL = 0.05  # 5% speed increase per kill (0.1x per 2 kills), intentionally raised from 0.01 (0.1x per 10 kills) to make gameplay faster
MAX_SPEED_MULTIPLIER = 3.0  # Maximum 3x speed
BASE_GAME_SPEED = 1.0

# Enemy reward settings
ENEMY_REWARD_REDUCTION_FACTOR = 0.75  # Enemies give 25% less money (75% of original)

# Tower types and costs
TOWER_TYPES = {
    'basic': {
        'name': 'Basic Tower',
        'cost': 50,
        'sell_value': 25,
        'damage': 20,
        'range': 100,
        'fire_rate': 30,
        'color': BLUE,
        'upgrade_cost': 40,
        'max_level': 3
    },
    'sniper': {
        'name': 'Sniper Tower',
        'cost': 80,
        'sell_value': 40,
        'damage': 50,
        'range': 200,
        'fire_rate': 60,
        'color': PURPLE,
        'upgrade_cost': 50,
        'max_level': 3
    },
    'rapid': {
        'name': 'Rapid Tower',
        'cost': 60,
        'sell_value': 30,
        'damage': 10,
        'range': 80,
        'fire_rate': 15,
        'color': ORANGE,
        'upgrade_cost': 35,
        'max_level': 3
    },
    'cannon': {
        'name': 'Cannon Tower',
        'cost': 100,
        'sell_value': 50,
        'damage': 35,
        'range': 120,
        'fire_rate': 45,
        'color': DARK_RED,
        'aoe_radius': 40,  # Area of effect damage
        'upgrade_cost': 60,
        'max_level': 3
    },
    'dog': {
        'name': 'Dog Tower',
        'cost': 75,
        'sell_value': 40,
        'damage': 0,
        'range': 0,
        'fire_rate': 0,
        'color': CYAN,
        'upgrade_cost': 0,
        'max_level': 1
    }
}

# Legacy tower settings for backward compatibility
TOWER_COST = 50
TOWER_SELL_VALUE = 25
TOWER_DAMAGE = 20
TOWER_RANGE = 100
TOWER_FIRE_RATE = 30
TOWER_MAX_LEVEL = 3
TOWER_UPGRADE_COST = 40
TOWER_UPGRADE_DAMAGE_BONUS = 10
TOWER_UPGRADE_RANGE_BONUS = 20
TOWER_UPGRADE_FIRE_RATE_BONUS = 5  # lower is faster

# Enemy types
ENEMY_TYPES = {
    'basic': {
        'name': 'Basic Enemy',
        'speed': 2,
        'health': 100,
        'reward': 10,
        'color': RED,
        'radius': 10
    },
    'fast': {
        'name': 'Fast Enemy',
        'speed': 4,
        'health': 60,
        'reward': 15,
        'color': YELLOW,
        'radius': 8
    },
    'tank': {
        'name': 'Tank Enemy',
        'speed': 1,
        'health': 200,
        'reward': 25,
        'color': GRAY,
        'radius': 12
    },
    'boss': {
        'name': 'Boss Enemy',
        'speed': 1.5,
        'health': 500,
        'reward': 100,
        'color': PURPLE,
        'radius': 15
    }
}

# Legacy enemy settings for backward compatibility
ENEMY_SPEED = 2
ENEMY_HEALTH = 100
ENEMY_REWARD = 20

# Wave settings
INITIAL_ENEMIES_PER_WAVE = 5
ENEMIES_INCREMENT = 3  # additional enemies per wave
BOSS_WAVE_INTERVAL = 10  # Boss appears every N waves

# UI settings
SIDEBAR_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_PADDING = 10
