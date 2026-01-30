"""
Projectile class for Tower Defence game
"""
import pygame
import math
from config import *


class Projectile:
    """Represents a projectile shot by a tower"""
    
    def __init__(self, x, y, target, damage):
        """
        Initialize a projectile
        
        Args:
            x, y: Starting position
            target: Enemy object to track
            damage: Damage dealt on hit
        """
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.speed = 5
        self.radius = 3
        self.hit = False
        
    def move(self):
        """
        Move projectile towards target
        
        Returns:
            bool: True if projectile hit target or target is dead
        """
        if not self.target or self.target.health <= 0:
            self.hit = True
            return True
            
        target_x, target_y = self.target.get_position()
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.speed + self.target.radius:
            self.hit = True
            self.target.take_damage(self.damage)
            return True
        
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        return False
    
    def draw(self, screen):
        """
        Draw the projectile on the screen
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
