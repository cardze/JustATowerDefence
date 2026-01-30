"""
Projectile class for Tower Defence game
"""
import pygame
import math
from config import *


class Projectile:
    """Represents a projectile shot by a tower"""
    
    def __init__(self, x, y, target, damage, aoe_radius=0):
        """
        Initialize a projectile
        
        Args:
            x, y: Starting position
            target: Enemy object to track
            damage: Damage dealt on hit
            aoe_radius: Area of effect radius (0 for single target)
        """
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.aoe_radius = aoe_radius
        self.speed = 5
        self.radius = 3
        self.hit = False
        self.hit_position = None
        
    def move(self, all_enemies=None):
        """
        Move projectile towards target
        
        Args:
            all_enemies: List of all enemies (for AoE damage)
        
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
            self.hit_position = (target_x, target_y)
            
            # Apply damage
            self.target.take_damage(self.damage)
            
            # AoE damage if applicable
            if self.aoe_radius > 0 and all_enemies:
                for enemy in all_enemies:
                    if enemy == self.target or enemy.health <= 0:
                        continue
                    ex, ey = enemy.get_position()
                    dist = math.sqrt((ex - target_x)**2 + (ey - target_y)**2)
                    if dist <= self.aoe_radius:
                        enemy.take_damage(self.damage * 0.5)  # 50% damage to nearby enemies
            
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
