#!/usr/bin/env python3
"""
Tower Defence Game - Main Entry Point
A simple tower defence game built with Pygame
"""
import pygame
import sys
import logging
from config import *
from game import Game

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tower_defence.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class UI:
    """Handles user interface rendering"""
    
    def __init__(self, screen):
        """
        Initialize UI
        
        Args:
            screen: Pygame surface to draw on
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
        # Button positions (initialized to avoid AttributeError)
        self.wave_button_y = 0
        self.tower_buttons_y = 0
        self.upgrade_button_y = None
        self.sell_button_y = None
        self.upgrade_button_rect = None
        self.sell_button_rect = None
        
    def draw_sidebar(self, game):
        """
        Draw the sidebar with game info and controls
        
        Args:
            game: Game object
        """
        sidebar_x = SCREEN_WIDTH - SIDEBAR_WIDTH
        pygame.draw.rect(self.screen, DARK_GREEN, 
                        (sidebar_x, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        
        y_offset = 20
        
        # Title
        title = self.title_font.render("Tower Defence", True, WHITE)
        self.screen.blit(title, (sidebar_x + 10, y_offset))
        y_offset += 50
        
        # Game stats
        money_text = self.font.render(f"Money: ${game.money}", True, WHITE)
        self.screen.blit(money_text, (sidebar_x + 10, y_offset))
        y_offset += 30
        
        lives_text = self.font.render(f"Lives: {game.lives}", True, WHITE)
        self.screen.blit(lives_text, (sidebar_x + 10, y_offset))
        y_offset += 30
        
        wave_text = self.font.render(f"Wave: {game.wave_number}", True, WHITE)
        self.screen.blit(wave_text, (sidebar_x + 10, y_offset))
        y_offset += 25
        
        # Game speed (Comment #2746643544)
        speed_text = self.font.render(f"Speed: {game.speed_multiplier:.2f}x", True, YELLOW)
        self.screen.blit(speed_text, (sidebar_x + 10, y_offset))
        y_offset += 50
        
        # Start wave button
        self.wave_button_y = y_offset  # Store for click detection
        button_rect = pygame.Rect(sidebar_x + BUTTON_PADDING, y_offset, 
                                  SIDEBAR_WIDTH - 2 * BUTTON_PADDING, BUTTON_HEIGHT)
        
        if game.wave_in_progress:
            button_color = GRAY
            button_text = "Wave In Progress"
        else:
            button_color = GREEN
            button_text = "Start Next Wave"
        
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        
        text = self.font.render(button_text, True, BLACK)
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)
        
        y_offset += BUTTON_HEIGHT + 20
        
        # Tower info
        tower_config = TOWER_TYPES.get(game.selected_tower_type, TOWER_TYPES['basic'])
        tower_info = self.font.render(f"{tower_config['name']}:", True, WHITE)
        self.screen.blit(tower_info, (sidebar_x + 10, y_offset))
        y_offset += 30
        
        cost_text = self.font.render(f"Cost: ${tower_config['cost']}", True, WHITE)
        self.screen.blit(cost_text, (sidebar_x + 10, y_offset))
        y_offset += 20
        
        damage_text = self.font.render(f"Dmg: {tower_config['damage']}", True, WHITE)
        self.screen.blit(damage_text, (sidebar_x + 10, y_offset))
        y_offset += 20
        
        range_text = self.font.render(f"Rng: {tower_config['range']}", True, WHITE)
        self.screen.blit(range_text, (sidebar_x + 10, y_offset))
        y_offset += 25
        
        # Tower type buttons (small colored squares)
        self.tower_buttons_y = y_offset  # Store for click detection
        small_font = pygame.font.Font(None, 16)
        button_size = 35
        button_spacing = 5
        types = ['basic', 'sniper', 'rapid', 'cannon']
        type_labels = ['B', 'S', 'R', 'C']
        
        for i, (t_type, label) in enumerate(zip(types, type_labels)):
            btn_x = sidebar_x + 10 + i * (button_size + button_spacing)
            btn_rect = pygame.Rect(btn_x, y_offset, button_size, button_size)
            t_config = TOWER_TYPES[t_type]
            
            # Highlight selected type
            if t_type == game.selected_tower_type:
                pygame.draw.rect(self.screen, YELLOW, btn_rect)
                pygame.draw.rect(self.screen, t_config['color'], btn_rect.inflate(-4, -4))
            else:
                pygame.draw.rect(self.screen, t_config['color'], btn_rect)
            pygame.draw.rect(self.screen, BLACK, btn_rect, 2)
            
            # Draw label
            label_text = small_font.render(label, True, WHITE)
            label_rect = label_text.get_rect(center=btn_rect.center)
            self.screen.blit(label_text, label_rect)
        
        y_offset += button_size + 15
        
        # Instructions
        inst_text = self.font.render("Click to build", True, YELLOW)
        self.screen.blit(inst_text, (sidebar_x + 10, y_offset))
        y_offset += 25
        
        inst_text2 = self.font.render("Right-click tower", True, YELLOW)
        self.screen.blit(inst_text2, (sidebar_x + 10, y_offset))
        y_offset += 20
        
        inst_text3 = self.font.render("  to upgrade/sell", True, YELLOW)
        self.screen.blit(inst_text3, (sidebar_x + 10, y_offset))
        
        # Selected tower info (sidebar) and buttons (beside tower)
        if game.selected_tower:
            selected_panel_start = SCREEN_HEIGHT - 120
            y_offset = max(y_offset + 20, selected_panel_start)
            selected_text = self.font.render("Selected Tower:", True, WHITE)
            self.screen.blit(selected_text, (sidebar_x + 10, y_offset))
            y_offset += 22
            
            # Tower stats
            tower = game.selected_tower
            level_text = self.font.render(f"Level: {tower.level}", True, WHITE)
            self.screen.blit(level_text, (sidebar_x + 10, y_offset))
            y_offset += 18
            
            dmg_text = self.font.render(f"Damage: {tower.damage}", True, WHITE)
            self.screen.blit(dmg_text, (sidebar_x + 10, y_offset))
            y_offset += 18
            
            rng_text = self.font.render(f"Range: {tower.range}", True, WHITE)
            self.screen.blit(rng_text, (sidebar_x + 10, y_offset))
            
            # Floating buttons beside tower
            button_width = 120
            button_height = 30
            gap = 6
            base_x = tower.x + tower.width // 2 + 10
            base_y = tower.y - button_height - gap
            
            # Keep buttons within game area bounds
            max_x = SCREEN_WIDTH - SIDEBAR_WIDTH - button_width - 5
            min_x = 5
            base_x = max(min_x, min(base_x, max_x))
            base_y = max(5, min(base_y, SCREEN_HEIGHT - (button_height * 2 + gap + 5)))
            
            # Upgrade button
            upgrade_cost = tower.get_upgrade_cost()
            if tower.can_upgrade() and upgrade_cost is not None:
                self.upgrade_button_rect = pygame.Rect(base_x, base_y, button_width, button_height)
                upgrade_color = GREEN if game.money >= upgrade_cost else GRAY
                pygame.draw.rect(self.screen, upgrade_color, self.upgrade_button_rect)
                pygame.draw.rect(self.screen, BLACK, self.upgrade_button_rect, 2)
                upgrade_text = self.font.render(f"Upgrade (${upgrade_cost})", True, BLACK)
                upgrade_text_rect = upgrade_text.get_rect(center=self.upgrade_button_rect.center)
                self.screen.blit(upgrade_text, upgrade_text_rect)
            else:
                self.upgrade_button_rect = None
                max_rect = pygame.Rect(base_x, base_y, button_width, button_height)
                pygame.draw.rect(self.screen, GRAY, max_rect)
                pygame.draw.rect(self.screen, BLACK, max_rect, 2)
                max_text = self.font.render("MAX LEVEL", True, BLACK)
                max_text_rect = max_text.get_rect(center=max_rect.center)
                self.screen.blit(max_text, max_text_rect)
            
            # Sell button
            sell_y = base_y + button_height + gap
            self.sell_button_rect = pygame.Rect(base_x, sell_y, button_width, button_height)
            pygame.draw.rect(self.screen, RED, self.sell_button_rect)
            pygame.draw.rect(self.screen, BLACK, self.sell_button_rect, 2)
            sell_text = self.font.render(f"Sell (${TOWER_SELL_VALUE})", True, WHITE)
            sell_text_rect = sell_text.get_rect(center=self.sell_button_rect.center)
            self.screen.blit(sell_text, sell_text_rect)
        else:
            self.upgrade_button_y = None
            self.sell_button_y = None
            self.upgrade_button_rect = None
            self.sell_button_rect = None
        
        return button_rect
    
    def draw_game_over(self, game):
        """
        Draw game over screen
        
        Args:
            game: Game object
        """
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        wave_text = self.font.render(f"You survived {game.wave_number} waves!", True, WHITE)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(wave_text, wave_rect)
        
        restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)


def main():
    """Main game loop"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defence")
    clock = pygame.time.Clock()
    
    logger.info("=== Tower Defence Game Started ===")
    game = Game()
    ui = UI(screen)
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                if event.button == 1:  # Left click
                    # Check if clicking in game area
                    if mouse_x < SCREEN_WIDTH - SIDEBAR_WIDTH:
                        if not game.game_over:
                            # Handle floating upgrade/sell buttons first
                            if game.selected_tower:
                                if ui.upgrade_button_rect and ui.upgrade_button_rect.collidepoint(mouse_x, mouse_y):
                                    if game.upgrade_tower(game.selected_tower):
                                        logger.info("Tower upgrade successful")
                                    continue
                                if ui.sell_button_rect and ui.sell_button_rect.collidepoint(mouse_x, mouse_y):
                                    game.sell_tower(game.selected_tower)
                                    continue

                            # Select tower if clicked, otherwise place new tower
                            clicked_tower = game.get_tower_at_position(mouse_x, mouse_y)
                            if clicked_tower:
                                game.selected_tower = clicked_tower
                            else:
                                game.selected_tower = None
                                game.add_tower(mouse_x, mouse_y)
                    else:
                        # Check tower type selection buttons (using stored position)
                        sidebar_x = SCREEN_WIDTH - SIDEBAR_WIDTH
                        button_size = 35
                        button_spacing = 5
                        types = ['basic', 'sniper', 'rapid', 'cannon']
                        
                        for i, t_type in enumerate(types):
                            btn_x = sidebar_x + 10 + i * (button_size + button_spacing)
                            btn_rect = pygame.Rect(btn_x, ui.tower_buttons_y, button_size, button_size)
                            if btn_rect.collidepoint(mouse_x, mouse_y):
                                game.selected_tower_type = t_type
                                logger.info(f"Selected tower type: {t_type}")
                                break
                        
                        # Check if clicking start wave button (using stored position)
                        button_rect = pygame.Rect(sidebar_x + BUTTON_PADDING, ui.wave_button_y,
                                                  SIDEBAR_WIDTH - 2 * BUTTON_PADDING, BUTTON_HEIGHT)
                        
                        if button_rect.collidepoint(mouse_x, mouse_y):
                            game.start_wave()
                        
                        # Floating buttons are handled in the game area click block
                
                elif event.button == 3:  # Right click
                    if mouse_x < SCREEN_WIDTH - SIDEBAR_WIDTH:
                        tower = game.get_tower_at_position(mouse_x, mouse_y)
                        if tower:
                            game.selected_tower = tower
                        else:
                            game.selected_tower = None
            
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    if event.key == pygame.K_r:
                        logger.info("Game restarted by player")
                        game = Game()
                    elif event.key == pygame.K_q:
                        logger.info("Game quit by player")
                        running = False
        
        # Update game
        game.update()
        
        # Draw everything
        screen.fill(WHITE)
        game.draw(screen)
        ui.draw_sidebar(game)
        
        if game.game_over:
            ui.draw_game_over(game)
        
        pygame.display.flip()
        # Use dynamic FPS based on speed multiplier (Comment #2746726455)
        current_fps = game.get_current_fps()
        clock.tick(current_fps)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
