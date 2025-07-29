"""
Medieval Deck - Main game entry point
A roguelike deckbuilder with AI-generated assets

Sprint 4 Implementation:
- RTX 5070 optimized SDXL pipeline
- High-quality hero sprite generation
- Advanced post-processing and image enhancement
- Memory optimization and performance tuning
"""

import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE
from screens.menu import MenuScreen
from screens.selection import SelectionScreen

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
        pygame.display.set_caption("Medieval Deck - Sprint 4")
        
        # Initialize game systems
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        self.selected_hero = None
        
        # Initialize screen objects
        self.menu_screen = MenuScreen(self)
        self.selection_screen = SelectionScreen(self)
        self.screens = {
            GameState.MENU: self.menu_screen,
            GameState.SELECTION: self.selection_screen
        }
        
        # Initialize font system for fallback rendering
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 60)
        self.text_font = pygame.font.Font(None, 40)
        
        print(f"Medieval Deck initialized - Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("Sprint 4: RTX 5070 optimized AI generation with hero sprites ready")
        
    def handle_events(self):
        """Handle pygame events and delegate to current screen"""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Delegate events to current screen
        if self.current_state in self.screens:
            new_state = self.screens[self.current_state].handle_events(events)
            if new_state:
                self.change_state(new_state)
                    
    def change_state(self, new_state):
        """
        Change game state with validation
        
        Args:
            new_state: Target state to transition to
        """
        if new_state == GameState.GAMEPLAY and new_state not in self.screens:
            print("State change: SELECTION -> GAMEPLAY (Coming in Sprint 5)")
            # For now, stay in selection until Sprint 5
            return
        
        print(f"State change: {self.current_state} -> {new_state}")
        self.current_state = new_state
        
    def update(self):
        """Update game logic based on current state"""
        if self.current_state in self.screens:
            self.screens[self.current_state].update()
        
    def render(self):
        """Render current game state"""
        self.screen.fill(BLACK)
        
        # Delegate rendering to current screen
        if self.current_state in self.screens:
            self.screens[self.current_state].render(self.screen)
        else:
            # Fallback rendering for unimplemented screens
            self.render_fallback()
            
        pygame.display.flip()
        
    def render_fallback(self):
        """Fallback rendering for unimplemented screens"""
        title = self.title_font.render(f"SCREEN: {self.current_state.upper()}", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        info = self.text_font.render("Coming in future sprint", True, WHITE)
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