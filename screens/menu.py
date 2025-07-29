"""
Main menu screen for Medieval Deck
Sprint 2 Implementation: Interactive menu with navigation buttons
"""

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GOLD
from utils.buttons import MenuButtonSet

class MenuScreen:
    """
    Main menu screen with title and navigation buttons
    Optimized for 3440x1440 ultrawide resolution
    """
    
    def __init__(self, game_instance):
        """
        Initialize menu screen
        
        Args:
            game_instance: Reference to main game instance for state changes
        """
        self.game = game_instance
        
        # Initialize fonts optimized for ultrawide
        self.title_font = pygame.font.Font(None, 140)
        self.subtitle_font = pygame.font.Font(None, 70)
        self.button_font = pygame.font.Font(None, 50)
        
        # Create button set
        self.button_set = MenuButtonSet(SCREEN_WIDTH, SCREEN_HEIGHT, self.button_font)
        self._setup_buttons()
        
        # Pre-render title elements
        self.title_surface = self.title_font.render("MEDIEVAL DECK", True, GOLD)
        self.title_rect = self.title_surface.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4)
        )
        
        self.subtitle_surface = self.subtitle_font.render(
            "A Roguelike Deckbuilder with AI-Generated Assets", True, WHITE
        )
        self.subtitle_rect = self.subtitle_surface.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 100)
        )
        
        print("Menu screen initialized for Sprint 2")
        
    def _setup_buttons(self):
        """Setup menu buttons with callbacks"""
        self.button_set.add_button("JOGAR", self._start_game)
        self.button_set.add_button("OPÇÕES", self._show_options)
        self.button_set.add_button("SAIR", self._quit_game)
        
    def _start_game(self):
        """Callback for start game button"""
        print("Starting game - transitioning to hero selection")
        
    def _show_options(self):
        """Callback for options button"""
        print("Options menu - Coming in future sprint")
        
    def _quit_game(self):
        """Callback for quit button"""
        print("Quitting game")
        self.game.running = False
        
    def handle_events(self, events):
        """
        Handle menu-specific events
        
        Args:
            events: List of pygame events
            
        Returns:
            str: Next game state or None
        """
        clicked_button = self.button_set.handle_events(events)
        
        if clicked_button == "JOGAR":
            return "selection"  # Transition to hero selection
        elif clicked_button == "SAIR":
            self.game.running = False
            
        return None
        
    def update(self):
        """Update menu logic (placeholder for animations)"""
        pass
        
    def render(self, screen):
        """
        Render menu screen with title and buttons
        
        Args:
            screen: Pygame surface to render on
        """
        # Clear screen
        screen.fill(BLACK)
        
        # Draw title
        screen.blit(self.title_surface, self.title_rect)
        screen.blit(self.subtitle_surface, self.subtitle_rect)
        
        # Draw Sprint 2 indicator
        sprint_text = self.button_font.render("Sprint 2: Menu System", True, WHITE)
        sprint_rect = sprint_text.get_rect(bottomright=(SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50))
        screen.blit(sprint_text, sprint_rect)
        
        # Draw buttons
        self.button_set.draw(screen)
        
        # Draw controls info
        controls_text = [
            "Mouse: Navigate and click buttons",
            "ESC: Quit game"
        ]
        
        y_offset = SCREEN_HEIGHT - 150
        for i, text in enumerate(controls_text):
            control_surface = self.button_font.render(text, True, WHITE)
            control_rect = control_surface.get_rect(bottomleft=(50, y_offset + i * 40))
            screen.blit(control_surface, control_rect)