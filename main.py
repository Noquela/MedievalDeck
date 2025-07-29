"""
Medieval Deck - Main game entry point
A roguelike deckbuilder with AI-generated assets

Sprint 1 Implementation:
- Basic game structure with state management
- Ultrawide 3440x1440 resolution support
- Modular architecture ready for future sprints
"""

import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE

class GameState:
    """Game state constants for state machine"""
    MENU = "menu"
    SELECTION = "selection"
    GAMEPLAY = "gameplay"
    EVENTS = "events"
    GAMEOVER = "gameover"

class MedievalDeck:
    """Main game class handling the core game loop and state management"""
    
    def __init__(self):
        """Initialize pygame and game systems"""
        pygame.init()
        
        # Initialize display with ultrawide resolution
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Medieval Deck - Sprint 1")
        
        # Initialize game systems
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        self.selected_hero = None
        
        # Initialize font system
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 60)
        self.text_font = pygame.font.Font(None, 40)
        
        print(f"Medieval Deck initialized - Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("Sprint 1: Basic structure and ultrawide support ready")
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        """Update game logic based on current state"""
        # State-specific updates will be implemented in respective sprints
        pass
        
    def render(self):
        """Render current game state"""
        self.screen.fill(BLACK)
        
        # State-specific rendering will be implemented in respective sprints
        if self.current_state == GameState.MENU:
            self.render_menu()
        elif self.current_state == GameState.SELECTION:
            self.render_selection()
        elif self.current_state == GameState.GAMEPLAY:
            self.render_gameplay()
            
        pygame.display.flip()
        
    def render_menu(self):
        """Render main menu with ultrawide-optimized layout"""
        # Main title
        title = self.title_font.render("MEDIEVAL DECK", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.subtitle_font.render("Sprint 1 - Foundation", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3 + 100))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Status info
        status_lines = [
            f"Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}",
            "State Management: Active",
            "Modular Architecture: Ready",
            "Press ESC to exit"
        ]
        
        y_start = SCREEN_HEIGHT//2 + 100
        for i, line in enumerate(status_lines):
            text = self.text_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_start + i * 50))
            self.screen.blit(text, text_rect)
        
    def render_selection(self):
        """Placeholder for selection rendering - Sprint 3"""
        title = self.title_font.render("HERO SELECTION", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        info = self.text_font.render("Coming in Sprint 3", True, WHITE)
        info_rect = info.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(info, info_rect)
        
    def render_gameplay(self):
        """Placeholder for gameplay rendering - Sprint 5"""
        title = self.title_font.render("COMBAT", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        info = self.text_font.render("Coming in Sprint 5", True, WHITE)
        info_rect = info.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(info, info_rect)
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MedievalDeck()
    game.run()