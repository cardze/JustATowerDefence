"""
Main Game class for Tower Defence
"""
import pygame
from config import *
from enemy import Enemy
from tower import Tower


class Game:
    """Main game logic and state management"""
    
    def __init__(self):
        """Initialize game state"""
        self.money = INITIAL_MONEY
        self.lives = INITIAL_LIVES
        self.wave_number = 0
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.game_over = False
        self.wave_in_progress = False
        self.enemies_to_spawn = 0
        self.spawn_timer = 0
        self.wave_complete_time = None
        self.selected_tower = None
        
        # Define the path for enemies
        self.path = [
            (50, 50),
            (150, 50),
            (150, 200),
            (300, 200),
            (300, 400),
            (500, 400),
            (500, 550),
            (600, 550)
        ]
        
    def start_wave(self):
        """Start a new wave of enemies"""
        if not self.wave_in_progress and not self.game_over:
            self.wave_number += 1
            self.enemies_to_spawn = INITIAL_ENEMIES_PER_WAVE + (self.wave_number - 1) * ENEMIES_INCREMENT
            self.wave_in_progress = True
            self.spawn_timer = 0
            
    def spawn_enemy(self):
        """Spawn a single enemy"""
        if self.enemies_to_spawn > 0:
            enemy = Enemy(self.path, self.wave_number)
            self.enemies.append(enemy)
            self.enemies_to_spawn -= 1
            
    def add_tower(self, x, y):
        """
        Add a tower at the specified position
        
        Args:
            x, y: Position to place tower
            
        Returns:
            bool: True if tower was placed successfully
        """
        if self.money >= TOWER_COST:
            # Check if position is valid (not on path, not on another tower)
            if self.is_valid_tower_position(x, y):
                tower = Tower(x, y)
                self.towers.append(tower)
                self.money -= TOWER_COST
                return True
        return False
    
    def is_valid_tower_position(self, x, y):
        """
        Check if tower position is valid
        
        Args:
            x, y: Position to check
            
        Returns:
            bool: True if position is valid
        """
        # Check if too close to path
        for i in range(len(self.path) - 1):
            x1, y1 = self.path[i]
            x2, y2 = self.path[i + 1]
            
            # Calculate distance to line segment
            if self.point_to_segment_distance(x, y, x1, y1, x2, y2) < 40:
                return False
        
        # Check if too close to another tower
        for tower in self.towers:
            tx, ty = tower.get_position()
            distance = ((x - tx)**2 + (y - ty)**2)**0.5
            if distance < 40:
                return False
                
        return True
    
    def point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        """
        Calculate distance from point to line segment
        
        Args:
            px, py: Point coordinates
            x1, y1, x2, y2: Line segment endpoints
            
        Returns:
            float: Distance to line segment
        """
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return ((px - x1)**2 + (py - y1)**2)**0.5
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx**2 + dy**2)))
        projection_x = x1 + t * dx
        projection_y = y1 + t * dy
        
        return ((px - projection_x)**2 + (py - projection_y)**2)**0.5
    
    def sell_tower(self, tower):
        """
        Sell a tower and get money back
        
        Args:
            tower: Tower object to sell
        """
        if tower in self.towers:
            self.towers.remove(tower)
            self.money += TOWER_SELL_VALUE
            self.selected_tower = None
            
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
        # Spawn enemies during wave
        if self.wave_in_progress and self.enemies_to_spawn > 0:
            self.spawn_timer += 1
            if self.spawn_timer >= 60:  # Spawn every second
                self.spawn_enemy()
                self.spawn_timer = 0
        
        # Update enemies
        enemies_to_remove = []
        for enemy in self.enemies:
            enemy.move()
            
            if enemy.reached_end:
                self.lives -= 1
                enemies_to_remove.append(enemy)
                if self.lives <= 0:
                    self.game_over = True
            elif enemy.health <= 0:
                self.money += enemy.reward
                enemies_to_remove.append(enemy)
        
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        
        # Check if wave is complete
        if self.wave_in_progress and self.enemies_to_spawn == 0 and len(self.enemies) == 0:
            self.wave_in_progress = False
            self.wave_complete_time = pygame.time.get_ticks()
        
        # Update towers
        for tower in self.towers:
            projectile = tower.update(self.enemies)
            if projectile:
                self.projectiles.append(projectile)
        
        # Update projectiles
        projectiles_to_remove = []
        for projectile in self.projectiles:
            if projectile.move():
                projectiles_to_remove.append(projectile)
        
        for projectile in projectiles_to_remove:
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)
    
    def draw_path(self, screen):
        """
        Draw the enemy path
        
        Args:
            screen: Pygame surface to draw on
        """
        if len(self.path) > 1:
            pygame.draw.lines(screen, GRAY, False, self.path, 20)
            
    def draw(self, screen):
        """
        Draw all game elements
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw path
        self.draw_path(screen)
        
        # Draw towers
        for tower in self.towers:
            tower.draw(screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
            
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
    
    def get_tower_at_position(self, x, y):
        """
        Get tower at mouse position
        
        Args:
            x, y: Mouse position
            
        Returns:
            Tower object or None
        """
        for tower in self.towers:
            if tower.is_clicked(x, y):
                return tower
        return None
