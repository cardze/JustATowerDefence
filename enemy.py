"""
Enemy class for Tower Defence game
"""
import pygame
import math
from config import *


class Enemy:
    """Represents an enemy that moves along the path"""
    
    def __init__(self, path, wave_number=1, enemy_type='basic'):
        """
        Initialize an enemy
        
        Args:
            path: List of (x, y) tuples representing the path
            wave_number: Current wave number (affects health)
            enemy_type: Type of enemy ('basic', 'fast', 'tank', 'boss')
        """
        self.path = path
        self.path_index = 0
        self.x, self.y = path[0]
        self.enemy_type = enemy_type
        
        # Get enemy type configuration
        enemy_config = ENEMY_TYPES.get(enemy_type, ENEMY_TYPES['basic'])
        self.name = enemy_config['name']
        self.base_speed = enemy_config['speed']
        self.speed = self.base_speed
        base_health = enemy_config['health']
        self.reward = enemy_config['reward'] + (wave_number - 1) * 2
        self.color = enemy_config['color']
        self.radius = enemy_config['radius']
        
        # Scale health with wave number
        self.max_health = base_health + (wave_number - 1) * 20
        self.health = self.max_health
        self.reached_end = False
        
    def update_speed(self, speed_multiplier):
        """Update enemy speed based on game speed multiplier"""
        self.speed = self.base_speed * speed_multiplier
        
    def move(self):
        """Move the enemy along the path"""
        if self.path_index >= len(self.path) - 1:
            self.reached_end = True
            return
            
        target_x, target_y = self.path[self.path_index + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.speed:
            self.path_index += 1
            if self.path_index >= len(self.path) - 1:
                self.reached_end = True
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def take_damage(self, damage):
        """
        Reduce enemy health by damage amount
        
        Args:
            damage: Amount of damage to deal
            
        Returns:
            bool: True if enemy is killed
        """
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        """
        Draw the enemy on the screen
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw enemy circle with type-specific color
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw a border for better visibility
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw health bar
        health_bar_width = self.radius * 2
        health_bar_height = 3
        health_percentage = self.health / self.max_health
        
        health_bar_x = self.x - health_bar_width // 2
        health_bar_y = self.y - self.radius - 5
        
        # Background (red)
        pygame.draw.rect(screen, RED, 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        # Health (green)
        pygame.draw.rect(screen, GREEN, 
                        (health_bar_x, health_bar_y, 
                         health_bar_width * health_percentage, health_bar_height))
    
    def get_position(self):
        """Return current position as tuple"""
        return (self.x, self.y)
