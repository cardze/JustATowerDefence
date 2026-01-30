"""
Tower class for Tower Defence game
"""
import pygame
import math
from config import *
from projectile import Projectile


class Tower:
    """Represents a defensive tower"""
    
    def __init__(self, x, y):
        """
        Initialize a tower
        
        Args:
            x, y: Position of the tower
        """
        self.x = x
        self.y = y
        self.level = 1
        self.range = TOWER_RANGE
        self.damage = TOWER_DAMAGE
        self.fire_rate = TOWER_FIRE_RATE
        self.frames_since_fire = 0
        self.width = 30
        self.height = 30
        self.target = None
        
    def upgrade(self):
        """
        Upgrade the tower to next level
        
        Returns:
            bool: True if upgrade was successful
        """
        if self.level >= TOWER_MAX_LEVEL:
            return False
            
        self.level += 1
        self.damage += TOWER_UPGRADE_DAMAGE_BONUS
        self.range += TOWER_UPGRADE_RANGE_BONUS
        self.fire_rate = max(5, self.fire_rate - TOWER_UPGRADE_FIRE_RATE_BONUS)
        return True
    
    def get_upgrade_cost(self):
        """Get the cost to upgrade this tower"""
        if self.level >= TOWER_MAX_LEVEL:
            return None
        return TOWER_UPGRADE_COST
    
    def can_upgrade(self):
        """Check if tower can be upgraded"""
        return self.level < TOWER_MAX_LEVEL
        
    def find_target(self, enemies):
        """
        Find the closest enemy within range
        
        Args:
            enemies: List of enemy objects
            
        Returns:
            Enemy object or None
        """
        closest_enemy = None
        closest_distance = self.range
        
        for enemy in enemies:
            if enemy.health <= 0:
                continue
                
            enemy_x, enemy_y = enemy.get_position()
            dx = enemy_x - self.x
            dy = enemy_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
                
        return closest_enemy
    
    def update(self, enemies):
        """
        Update tower state and find targets
        
        Args:
            enemies: List of enemy objects
            
        Returns:
            Projectile object if tower fires, None otherwise
        """
        self.frames_since_fire += 1
        
        # Check if current target is still valid
        if self.target and self.target.health <= 0:
            self.target = None
            
        # Find new target if needed
        if not self.target:
            self.target = self.find_target(enemies)
        
        # Check if target is still in range
        if self.target:
            target_x, target_y = self.target.get_position()
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.range:
                self.target = None
        
        # Fire at target if ready
        if self.target and self.frames_since_fire >= self.fire_rate:
            self.frames_since_fire = 0
            return Projectile(self.x, self.y, self.target, self.damage)
            
        return None
    
    def draw(self, screen):
        """
        Draw the tower on the screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw tower body with color based on level
        tower_colors = [BLUE, (0, 0, 200), (0, 0, 150)]
        color = tower_colors[min(self.level - 1, len(tower_colors) - 1)]
        
        tower_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
        )
        pygame.draw.rect(screen, color, tower_rect)
        
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
