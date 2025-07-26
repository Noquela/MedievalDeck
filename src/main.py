"""
TODO Sprint 03: ✅ COMPLETO
✔ Sistema de cartas expandido (30 cartas Knight)
✔ Mecânicas de combate por turnos
✔ UI interativa com hover e seleção
✔ Power effects e cartas especiais
✔ Resultado screen corrigido
"""

import pygame
import sys
import os
from ui.screen_manager import ScreenManager
from ui.menu_screen import MenuScreen
import settings


class Game:
    """Main game class that manages the game loop and screen management."""
    
    def __init__(self) -> None:
        """Initialize the game with pygame and basic settings."""
        pygame.init()
        self.screen_width = settings.WINDOW_WIDTH
        self.screen_height = settings.WINDOW_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(settings.GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.target_fps = settings.TARGET_FPS
        self.running = True
        
        # Initialize screen manager with menu screen
        self.screen_manager = ScreenManager()
        self.screen_manager.push(MenuScreen(self.screen_manager))
        
    def handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and len(self.screen_manager._stack) <= 1:
                    # ESC on menu screen exits the game
                    self.running = False
                else:
                    # Delegate to screen manager
                    self.screen_manager.handle_event(event)
            else:
                # Delegate all other events to screen manager
                self.screen_manager.handle_event(event)
    
    def update(self, dt: float) -> None:
        """Update game state."""
        # Check if screen stack is empty (shouldn't happen)
        if self.screen_manager.is_empty():
            self.running = False
            return
        
        # Update current screen
        self.screen_manager.update(dt)
    
    def draw(self) -> None:
        """Draw the current frame."""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw current screen
        self.screen_manager.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(self.target_fps) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main() -> None:
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
