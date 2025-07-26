"""Main menu screen."""

import pygame
import os
from typing import TYPE_CHECKING
from .screen_base import ScreenBase
from engine.resources import load_image

if TYPE_CHECKING:
    from .screen_manager import ScreenManager


class MenuScreen(ScreenBase):
    """Main menu screen with play button."""
    
    def __init__(self, screen_manager: 'ScreenManager') -> None:
        """Initialize menu screen.
        
        Args:
            screen_manager: Reference to screen manager for navigation
        """
        super().__init__()
        self.screen_manager = screen_manager
        
        # Load background
        self.background = load_image("assets/bg/menu.png", cache=True)
        
        # Button setup
        self.play_button_rect = pygame.Rect(1720 - 150, 720 - 50, 300, 100)  # Center of screen
        self.play_button_hovered = False
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle menu events."""
        if event.type == pygame.MOUSEMOTION:
            self.play_button_hovered = self.play_button_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.play_button_hovered:  # Left click on play button
                from .character_select_screen import CharacterSelectScreen
                self.screen_manager.push(CharacterSelectScreen(self.screen_manager))
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                from .character_select_screen import CharacterSelectScreen
                self.screen_manager.push(CharacterSelectScreen(self.screen_manager))
    
    def update(self, dt: float) -> None:
        """Update menu state."""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the menu screen."""
        # Draw background
        if self.background:
            # Scale to fit screen
            scaled_bg = pygame.transform.scale(self.background, (3440, 1440))
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill((25, 25, 35))  # Fallback dark background
        
        # Draw title
        title_text = self.font_title.render("Medieval Deck", True, (255, 215, 0))
        title_shadow = self.font_title.render("Medieval Deck", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(1720, 300))
        shadow_rect = title_shadow.get_rect(center=(1723, 303))
        surface.blit(title_shadow, shadow_rect)
        surface.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.font_medium.render("Roguelike Card Game", True, (200, 180, 120))
        subtitle_rect = subtitle_text.get_rect(center=(1720, 380))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Draw play button
        button_color = (100, 60, 30) if not self.play_button_hovered else (140, 90, 50)
        border_color = (200, 150, 100) if not self.play_button_hovered else (255, 200, 150)
        
        pygame.draw.rect(surface, button_color, self.play_button_rect)
        pygame.draw.rect(surface, border_color, self.play_button_rect, 3)
        
        # Draw button text
        button_text = self.font_large.render("JOGAR", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=self.play_button_rect.center)
        surface.blit(button_text, text_rect)
        
        # Draw instructions
        instructions = [
            "Pressione ESPAÇO ou clique em JOGAR para começar",
            "ESC para sair"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (180, 180, 180))
            inst_rect = inst_text.get_rect(center=(1720, 1000 + i * 30))
            surface.blit(inst_text, inst_rect)
