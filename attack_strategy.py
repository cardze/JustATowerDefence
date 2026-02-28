"""
Strategy Pattern: Different attack strategies for towers

This module defines various attack strategies that towers can use.
Each strategy represents a different way of dealing damage to enemies.
"""
from abc import ABC, abstractmethod
import math


class AttackStrategy(ABC):
    """Abstract base class for attack strategies"""
    
    @abstractmethod
    def attack(self, tower, enemies):
        """
        Execute attack strategy
        
        Args:
            tower: The tower performing the attack
            enemies: List of enemies in the game
            
        Returns:
            Enemy object or None
        """
        pass
    
    @abstractmethod
    def get_target(self, tower, enemies):
        """
        Get target based on strategy
        
        Args:
            tower: The tower
            enemies: List of enemies
            
        Returns:
            Enemy object or None
        """
        pass


class ClosestEnemyStrategy(AttackStrategy):
    """Attack the closest enemy within range"""
    
    def get_target(self, tower, enemies):
        """Find and return the closest enemy"""
        closest_enemy = None
        closest_distance = tower.range
        
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            
            enemy_x, enemy_y = enemy.get_position()
            dx = enemy_x - tower.x
            dy = enemy_y - tower.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
        
        return closest_enemy
    
    def attack(self, tower, enemies):
        """Attack the closest enemy"""
        return self.get_target(tower, enemies)


class FastestEnemyStrategy(AttackStrategy):
    """Attack the fastest enemy within range (prioritize by speed)"""
    
    def get_target(self, tower, enemies):
        """Find and return the fastest enemy"""
        fastest_enemy = None
        fastest_speed = -1
        
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            
            enemy_x, enemy_y = enemy.get_position()
            dx = enemy_x - tower.x
            dy = enemy_y - tower.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance <= tower.range and enemy.speed > fastest_speed:
                fastest_speed = enemy.speed
                fastest_enemy = enemy
        
        return fastest_enemy
    
    def attack(self, tower, enemies):
        """Attack the fastest enemy"""
        return self.get_target(tower, enemies)


class StrongestEnemyStrategy(AttackStrategy):
    """Attack the strongest enemy (most health) within range"""
    
    def get_target(self, tower, enemies):
        """Find and return the enemy with most health"""
        strongest_enemy = None
        max_health = -1
        
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            
            enemy_x, enemy_y = enemy.get_position()
            dx = enemy_x - tower.x
            dy = enemy_y - tower.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance <= tower.range and enemy.health > max_health:
                max_health = enemy.health
                strongest_enemy = enemy
        
        return strongest_enemy
    
    def attack(self, tower, enemies):
        """Attack the strongest enemy"""
        return self.get_target(tower, enemies)


class FarthestEnemyStrategy(AttackStrategy):
    """Attack the enemy furthest along the path (most advanced)"""
    
    def get_target(self, tower, enemies):
        """Find and return the furthest enemy along path"""
        furthest_enemy = None
        furthest_progress = -1
        
        for enemy in enemies:
            if enemy.health <= 0:
                continue
            
            enemy_x, enemy_y = enemy.get_position()
            dx = enemy_x - tower.x
            dy = enemy_y - tower.y
            distance = math.sqrt(dx**2 + dy**2)
            
            # Enemy progress is based on path_index
            if distance <= tower.range and enemy.path_index > furthest_progress:
                furthest_progress = enemy.path_index
                furthest_enemy = enemy
        
        return furthest_enemy
    
    def attack(self, tower, enemies):
        """Attack the furthest enemy along path"""
        return self.get_target(tower, enemies)
