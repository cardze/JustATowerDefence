"""
Main Game class for Tower Defence
"""
import pygame
import logging
import random
from config import *
from enemy import Enemy
from tower import Tower

logger = logging.getLogger(__name__)


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
        
        # Game speed tracking (Comment #2746643544, #2746726455)
        # Speed multiplier affects the ENTIRE GAME SPEED (FPS), not just enemy movement
        # Base FPS is 60, multiplier increases game speed up to 3x (180 FPS)
        self.speed_multiplier = BASE_GAME_SPEED  # Reset to 1.0x on game init/restart
        self.enemies_killed = 0
        
        # Tower type selection
        self.selected_tower_type = 'basic'
        
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
        
        logger.info("Game initialized - Money: $%d, Lives: %d, Speed: %.2fx", 
                   self.money, self.lives, self.speed_multiplier)
        
    def start_wave(self):
        """Start a new wave of enemies"""
        if not self.wave_in_progress and not self.game_over:
            self.wave_number += 1
            self.enemies_to_spawn = INITIAL_ENEMIES_PER_WAVE + (self.wave_number - 1) * ENEMIES_INCREMENT
            self.wave_in_progress = True
            self.spawn_timer = 0
            
            # Generate more complex path for higher waves
            if self.wave_number > 1 and self.wave_number % 5 == 0:
                self.generate_complex_path()
            
            logger.info(f"Wave {self.wave_number} started - Enemies to spawn: {self.enemies_to_spawn}")
            
    def spawn_enemy(self):
        """Spawn a single enemy with varying types"""
        if self.enemies_to_spawn > 0:
            # Determine enemy type based on wave and randomness
            enemy_type = self._get_enemy_type_for_wave()
            enemy = Enemy(self.path, self.wave_number, enemy_type)
            # No need to update enemy speed - entire game speed is controlled by FPS
            self.enemies.append(enemy)
            self.enemies_to_spawn -= 1
    
    def _get_enemy_type_for_wave(self):
        """Determine which enemy type to spawn based on wave number"""
        # Boss every 10 waves
        if self.wave_number % BOSS_WAVE_INTERVAL == 0:
            return 'boss'
        
        # Mix of enemy types based on wave
        rand = random.random()
        if self.wave_number < 3:
            return 'basic'
        elif self.wave_number < 7:
            return 'fast' if rand < 0.3 else 'basic'
        elif self.wave_number < 12:
            if rand < 0.3:
                return 'fast'
            elif rand < 0.6:
                return 'tank'
            else:
                return 'basic'
        else:
            if rand < 0.25:
                return 'fast'
            elif rand < 0.5:
                return 'tank'
            else:
                return 'basic'
            
    def add_tower(self, x, y, tower_type=None):
        """
        Add a tower at the specified position
        
        Args:
            x, y: Position to place tower
            tower_type: Type of tower to build (None uses selected type)
            
        Returns:
            bool: True if tower was placed successfully
        """
        if tower_type is None:
            tower_type = self.selected_tower_type
        
        tower_config = TOWER_TYPES.get(tower_type, TOWER_TYPES['basic'])
        tower_cost = tower_config['cost']
        
        if self.money >= tower_cost:
            # Check if position is valid (not on path, not on another tower)
            if self.is_valid_tower_position(x, y):
                tower = Tower(x, y, tower_type)
                self.towers.append(tower)
                self.money -= tower_cost
                logger.info(f"{tower.name} placed at ({x}, {y}) - Money remaining: ${self.money}")
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
            logger.info(f"Tower sold at ({tower.x}, {tower.y}) for ${TOWER_SELL_VALUE}")
    
    def upgrade_tower(self, tower):
        """
        Upgrade a tower
        
        Args:
            tower: Tower object to upgrade
            
        Returns:
            bool: True if upgrade was successful
        """
        if tower not in self.towers:
            return False
            
        upgrade_cost = tower.get_upgrade_cost()
        if upgrade_cost is None or self.money < upgrade_cost:
            return False
        
        if tower.upgrade():
            self.money -= upgrade_cost
            logger.info(f"Tower at ({tower.x}, {tower.y}) upgraded to level {tower.level} - Damage: {tower.damage}, Range: {tower.range}, Fire Rate: {tower.fire_rate}")
            return True
        
        return False
    
    def generate_complex_path(self):
        """
        Generate a more complex path based on current wave number
        Paths become more intricate as waves progress
        """
        import random
        
        # Different path patterns based on wave progression
        wave_mod = (self.wave_number // 5) % 4
        
        if wave_mod == 0:
            # Zigzag path
            self.path = [
                (50, 50),
                (200, 50),
                (200, 150),
                (100, 150),
                (100, 250),
                (300, 250),
                (300, 400),
                (150, 400),
                (150, 550),
                (600, 550)
            ]
        elif wave_mod == 1:
            # Spiral path
            self.path = [
                (50, 100),
                (500, 100),
                (500, 450),
                (150, 450),
                (150, 200),
                (400, 200),
                (400, 350),
                (250, 350),
                (250, 550),
                (600, 550)
            ]
        elif wave_mod == 2:
            # Snake path
            self.path = [
                (50, 50),
                (550, 50),
                (550, 150),
                (100, 150),
                (100, 300),
                (550, 300),
                (550, 450),
                (100, 450),
                (100, 550),
                (600, 550)
            ]
        else:
            # Maze-like path
            self.path = [
                (50, 300),
                (200, 300),
                (200, 100),
                (400, 100),
                (400, 450),
                (250, 450),
                (250, 200),
                (500, 200),
                (500, 550),
                (600, 550)
            ]
        
        logger.info(f"Path complexity increased - Pattern {wave_mod + 1} activated for wave {self.wave_number}")
            
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
        enemies_killed = 0
        enemies_escaped = 0
        
        for enemy in self.enemies:
            enemy.move()
            
            if enemy.reached_end:
                self.lives -= 1
                enemies_to_remove.append(enemy)
                enemies_escaped += 1
                if self.lives <= 0:
                    self.game_over = True
                    logger.warning(f"Game Over! Wave: {self.wave_number}, Towers: {len(self.towers)}")
            elif enemy.health <= 0:
                self.money += enemy.reward
                enemies_to_remove.append(enemy)
                enemies_killed += 1
                
                # Increase game speed (Comment #2746643544, #2746726455)
                # This increases entire game FPS, not just enemy speed
                self.enemies_killed += 1
                self.speed_multiplier = min(MAX_SPEED_MULTIPLIER, 
                                           BASE_GAME_SPEED + (self.enemies_killed * SPEED_INCREASE_PER_KILL))
                # Log speed change
                if self.enemies_killed % 10 == 0:  # Log every 10 kills
                    logger.info(f"Game speed increased to {self.speed_multiplier:.2f}x (FPS: {int(FPS * self.speed_multiplier)})")
        
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)
        
        if enemies_killed > 0:
            logger.info(f"Enemies defeated: {enemies_killed} - Money earned: ${enemies_killed * ENEMY_REWARD}")
        if enemies_escaped > 0:
            logger.warning(f"Enemies escaped: {enemies_escaped} - Lives remaining: {self.lives}")
        
        # Check if wave is complete
        if self.wave_in_progress and self.enemies_to_spawn == 0 and len(self.enemies) == 0:
            self.wave_in_progress = False
            self.wave_complete_time = pygame.time.get_ticks()
            logger.info(f"Wave {self.wave_number} completed! Money: ${self.money}, Lives: {self.lives}, Towers: {len(self.towers)}")
        
        # Update towers
        for tower in self.towers:
            projectile = tower.update(self.enemies)
            if projectile:
                self.projectiles.append(projectile)
        
        # Update projectiles
        projectiles_to_remove = []
        for projectile in self.projectiles:
            if projectile.move(self.enemies):
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
    
    def get_current_fps(self):
        """
        Get the current FPS based on speed multiplier
        
        Returns:
            int: Current target FPS
        """
        return int(FPS * self.speed_multiplier)
