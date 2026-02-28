"""
Tower class for Tower Defence game

Implements Strategy Pattern for different attack strategies
and State Pattern for tower state management
"""
import pygame
import math
from config import *
from projectile import Projectile
from attack_strategy import ClosestEnemyStrategy, AttackStrategy
from tower_state import IdleState, TowerState
from event_system import EventManager, GameEvent


class Tower:
    """
    Represents a defensive tower with state and strategy patterns
    
    Uses:
    - Strategy Pattern: Different attack strategies (closest, fastest, strongest, farthest)
    - State Pattern: Tower states (Idle, Attacking, Upgraded)
    - Observer Pattern: Emits events when important actions occur
    """
    
    def __init__(self, x, y, tower_type='basic'):
        """
        Initialize a tower
        
        Args:
            x, y: Position of the tower
            tower_type: Type of tower ('basic', 'sniper', 'rapid', 'cannon')
        """
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.level = 1
        
        # Get tower type configuration
        tower_config = TOWER_TYPES.get(tower_type, TOWER_TYPES['basic'])
        self.name = tower_config['name']
        self.base_damage = tower_config['damage']
        self.base_range = tower_config['range']
        self.base_fire_rate = tower_config['fire_rate']
        self.color = tower_config['color']
        self.upgrade_cost = tower_config['upgrade_cost']
        self.max_level = tower_config['max_level']
        
        # Current stats (can be upgraded)
        self.damage = self.base_damage
        self.range = self.base_range
        self.fire_rate = self.base_fire_rate
        
        # AoE for cannon towers
        self.aoe_radius = tower_config.get('aoe_radius', 0)
        
        self.frames_since_fire = 0
        self.width = 30
        self.height = 30
        self.target = None
        
        # Strategy pattern: Default attack strategy is closest enemy
        self.attack_strategy: AttackStrategy = ClosestEnemyStrategy()
        
        # State pattern: Tower starts in idle state
        self.state: TowerState = IdleState()
        self.state.enter(self)
        
        # Event system
        self.event_manager = EventManager()
        self.event_manager.emit(GameEvent.TOWER_PLACED, {
            'tower': self,
            'position': (self.x, self.y),
            'type': self.tower_type
        })
    
    def set_attack_strategy(self, strategy: AttackStrategy):
        """
        Change the attack strategy for this tower (Strategy Pattern)
        
        Args:
            strategy: New attack strategy to use
        """
        self.attack_strategy = strategy
    
    def set_state(self, new_state: TowerState):
        """
        Change tower state (State Pattern)
        
        Args:
            new_state: New state for the tower
        """
        self.state.exit(self)
        self.state = new_state
        self.state.enter(self)
        
    def upgrade(self):
        """
        Upgrade the tower to next level
        
        Returns:
            bool: True if upgrade was successful
        """
        if self.level >= self.max_level:
            return False
            
        self.level += 1
        self.damage += TOWER_UPGRADE_DAMAGE_BONUS
        self.range += TOWER_UPGRADE_RANGE_BONUS
        self.fire_rate = max(5, self.fire_rate - TOWER_UPGRADE_FIRE_RATE_BONUS)
        
        # Emit upgrade event
        self.event_manager.emit(GameEvent.TOWER_UPGRADED, {
            'tower': self,
            'new_level': self.level,
            'damage': self.damage,
            'range': self.range
        })
        
        # Update state to upgraded
        from tower_state import UpgradedState
        self.set_state(UpgradedState())
        
        return True
    
    def get_upgrade_cost(self):
        """Get the cost to upgrade this tower"""
        if self.level >= self.max_level:
            return None
        return self.upgrade_cost
    
    def can_upgrade(self):
        """Check if tower can be upgraded"""
        return self.level < self.max_level
        
    def find_target(self, enemies):
        """
        Find the closest enemy within range
        
        Uses the current attack strategy to find target
        
        Args:
            enemies: List of enemy objects
            
        Returns:
            Enemy object or None
        """
        # Delegate to attack strategy
        return self.attack_strategy.get_target(self, enemies)
    
    def update(self, enemies):
        """
        Update tower state and find targets
        
        Uses State Pattern to manage tower behavior
        
        Args:
            enemies: List of enemy objects
            
        Returns:
            Projectile object if tower fires, None otherwise
        """
        # Find new target if needed
        if not self.target:
            self.target = self.find_target(enemies)
        
        # Check if current target is still valid
        if self.target and self.target.health <= 0:
            self.target = None
        
        # Check if target is still in range
        if self.target:
            target_x, target_y = self.target.get_position()
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.range:
                self.target = None
                # Emit event when enemy goes out of range
                self.event_manager.emit(GameEvent.ENEMY_OUT_OF_RANGE, {
                    'tower': self
                })
            else:
                # Emit event when enemy is in range
                self.event_manager.emit(GameEvent.ENEMY_IN_RANGE, {
                    'tower': self,
                    'enemy': self.target
                })
        
        # Use attack strategy to handle firing
        self.frames_since_fire += 1
        return self.attack_strategy.attack(self, enemies)
    
    def draw(self, screen):
        """
        Draw the tower on the screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw tower body with type-specific color and level shading
        base_color = self.color
        # Darken color slightly for each level
        level_mod = min(self.level - 1, 2) * 20
        color = tuple(max(0, c - level_mod) for c in base_color)
        
        tower_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, color, tower_rect)
        pygame.draw.rect(screen, BLACK, tower_rect, 2)  # Border
        
        # Draw level indicator
        if self.level > 1:
            font = pygame.font.Font(None, 20)
            level_text = font.render(str(self.level), True, YELLOW)
            text_rect = level_text.get_rect(center=(self.x, self.y))
            screen.blit(level_text, text_rect)
        
        # Draw range circle (semi-transparent)
        range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(range_surface, (*GRAY, 50), (self.range, self.range), self.range)
        screen.blit(range_surface, 
                   (self.x - self.range, self.y - self.range))
    
    def get_position(self):
        """Return tower position as tuple"""
        return (self.x, self.y)
    
    def is_clicked(self, mouse_x, mouse_y):
        """
        Check if mouse position is within tower bounds
        
        Args:
            mouse_x, mouse_y: Mouse position
            
        Returns:
            bool: True if tower is clicked
        """
        return (abs(mouse_x - self.x) < self.width // 2 and 
                abs(mouse_y - self.y) < self.height // 2)
