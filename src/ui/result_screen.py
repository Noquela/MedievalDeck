"""Result screen displayed after combat ends."""

import pygame
from typing import TYPE_CHECKING
from .screen_base import ScreenBase

if TYPE_CHECKING:
    from .screen_manager import ScreenManager


class ResultScreen(ScreenBase):
    """Screen shown after combat with victory/defeat status."""
    
    def __init__(self, screen_manager: 'ScreenManager', victory: bool, character_name: str) -> None:
        """Initialize result screen.
        
        Args:
            screen_manager: Reference to screen manager for navigation
            victory: Whether the player won
            character_name: Name of the character used
        """
        super().__init__()
        self.screen_manager = screen_manager
        self.victory = victory
        self.character_name = character_name
        
        # Auto-return timer
        self.display_time = 3000  # 3 seconds
        self.start_time = pygame.time.get_ticks()
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle result screen events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self._return_to_menu()
            elif event.key == pygame.K_ESCAPE:
                self._return_to_menu()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._return_to_menu()
    
    def _return_to_menu(self) -> None:
        """Return to main menu."""
        # Pop twice: Result → Combat → Character Select, leaving only Menu
        self.screen_manager.pop()  # Remove result screen
        self.screen_manager.pop()  # Remove combat screen
        self.screen_manager.pop()  # Remove character select screen
        # Now we're back at the menu
    
    def update(self, dt: float) -> None:
        """Update result screen."""
        # Auto-return to menu after display time
        if pygame.time.get_ticks() - self.start_time > self.display_time:
            self._return_to_menu()
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the result screen."""
        # Semi-transparent overlay
        overlay = pygame.Surface((3440, 1440))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Result title
        if self.victory:
            title_text = "VITÓRIA!"
            title_color = (0, 255, 0)
            subtitle_text = f"{self.character_name} derrotou o inimigo!"
        else:
            title_text = "DERROTA"
            title_color = (255, 0, 0)
            subtitle_text = f"{self.character_name} foi derrotado..."
        
        # Draw title
        title_surface = self.font_title.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(1720, 600))
        surface.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_surface = self.font_large.render(subtitle_text, True, (255, 255, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(1720, 700))
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Instructions
        inst_text = "Pressione qualquer tecla ou clique para continuar"
        inst_surface = self.font_medium.render(inst_text, True, (200, 200, 200))
        inst_rect = inst_surface.get_rect(center=(1720, 800))
        surface.blit(inst_surface, inst_rect)
        
        # Timer indicator
        remaining_time = max(0, self.display_time - (pygame.time.get_ticks() - self.start_time))
        seconds_left = remaining_time // 1000 + 1
        timer_text = f"Retornando ao menu em {seconds_left}s..."
        timer_surface = self.font_small.render(timer_text, True, (150, 150, 150))
        timer_rect = timer_surface.get_rect(center=(1720, 900))
        surface.blit(timer_surface, timer_rect)
