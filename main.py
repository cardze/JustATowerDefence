#!/usr/bin/env python3
"""
Tower Defence Game - Main Entry Point
A simple tower defence game built with Pygame
"""
import pygame
import sys
from config import *
from game import Game


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
        y_offset += 50
        
        # Start wave button
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
        tower_info = self.font.render("Build Tower:", True, WHITE)
        self.screen.blit(tower_info, (sidebar_x + 10, y_offset))
        y_offset += 30
        
        cost_text = self.font.render(f"Cost: ${TOWER_COST}", True, WHITE)
        self.screen.blit(cost_text, (sidebar_x + 10, y_offset))
        y_offset += 25
        
        damage_text = self.font.render(f"Damage: {TOWER_DAMAGE}", True, WHITE)
        self.screen.blit(damage_text, (sidebar_x + 10, y_offset))
        y_offset += 25
        
        range_text = self.font.render(f"Range: {TOWER_RANGE}", True, WHITE)
        self.screen.blit(range_text, (sidebar_x + 10, y_offset))
        y_offset += 40
        
        # Instructions
        inst_text = self.font.render("Click to build", True, YELLOW)
        self.screen.blit(inst_text, (sidebar_x + 10, y_offset))
        y_offset += 25
        
        inst_text2 = self.font.render("Right-click to sell", True, YELLOW)
        self.screen.blit(inst_text2, (sidebar_x + 10, y_offset))
        
        # Selected tower info
        if game.selected_tower:
            y_offset += 50
            selected_text = self.font.render("Selected Tower:", True, WHITE)
            self.screen.blit(selected_text, (sidebar_x + 10, y_offset))
            y_offset += 30
            
            sell_button_rect = pygame.Rect(sidebar_x + BUTTON_PADDING, y_offset,
                                          SIDEBAR_WIDTH - 2 * BUTTON_PADDING, BUTTON_HEIGHT)
            pygame.draw.rect(self.screen, RED, sell_button_rect)
            pygame.draw.rect(self.screen, BLACK, sell_button_rect, 2)
            
            sell_text = self.font.render(f"Sell (${TOWER_SELL_VALUE})", True, WHITE)
            sell_text_rect = sell_text.get_rect(center=sell_button_rect.center)
            self.screen.blit(sell_text, sell_text_rect)
        
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
                            # Try to place tower
                            game.add_tower(mouse_x, mouse_y)
                    else:
                        # Check if clicking start wave button
                        sidebar_x = SCREEN_WIDTH - SIDEBAR_WIDTH
                        button_y = 150
                        button_rect = pygame.Rect(sidebar_x + BUTTON_PADDING, button_y,
                                                  SIDEBAR_WIDTH - 2 * BUTTON_PADDING, BUTTON_HEIGHT)
                        
                        if button_rect.collidepoint(mouse_x, mouse_y):
                            game.start_wave()
                        
                        # Check if clicking sell button
                        if game.selected_tower:
                            sell_button_y = 450
                            sell_button_rect = pygame.Rect(sidebar_x + BUTTON_PADDING, sell_button_y,
                                                          SIDEBAR_WIDTH - 2 * BUTTON_PADDING, BUTTON_HEIGHT)
                            if sell_button_rect.collidepoint(mouse_x, mouse_y):
                                game.sell_tower(game.selected_tower)
                
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
                        game = Game()
                    elif event.key == pygame.K_q:
                        running = False
        
        # Update game
        game.update()
        
        # Draw everything
        screen.fill(WHITE)
        game.draw(screen)
        wave_button_rect = ui.draw_sidebar(game)
        
        if game.game_over:
            ui.draw_game_over(game)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
