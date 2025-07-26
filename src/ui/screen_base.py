"""
TODO Sprint 03:
□ Screen base class abstrata
□ Sistema de transição entre telas
□ Gestão de eventos padrão
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import pygame


class ScreenBase(ABC):
    """Base class for all game screens."""
    
    def __init__(self, screen: pygame.Surface) -> None:
        """Initialize screen.
        
        Args:
            screen: Main pygame screen surface
        """
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.running = True
        self.next_screen: Optional[str] = None
        
        # Common fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 48)
        self.font_title = pygame.font.Font(None, 72)
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle a pygame event.
        
        Args:
            event: Pygame event to handle
        """
        pass
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update screen state.
        
        Args:
            dt: Delta time in seconds
        """
        pass
    
    @abstractmethod
    def draw(self) -> None:
        """Draw the screen."""
        pass
    
    def set_next_screen(self, screen_name: str) -> None:
        """Set the next screen to transition to.
        
        Args:
            screen_name: Name of screen to transition to
        """
        self.next_screen = screen_name
        self.running = False
    
    def is_running(self) -> bool:
        """Check if screen is still running.
        
        Returns:
            True if screen should continue running
        """
        return self.running
    
    def get_next_screen(self) -> Optional[str]:
        """Get the next screen to transition to.
        
        Returns:
            Name of next screen or None
        """
        return self.next_screen
    
    def draw_text_centered(self, text: str, font: pygame.font.Font, 
                          color: tuple[int, int, int], y: int) -> None:
        """Draw centered text.
        
        Args:
            text: Text to draw
            font: Font to use
            color: RGB color
            y: Y position
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw_button(self, text: str, font: pygame.font.Font, 
                   rect: pygame.Rect, bg_color: tuple[int, int, int], 
                   text_color: tuple[int, int, int]) -> None:
        """Draw a button.
        
        Args:
            text: Button text
            font: Font to use
            rect: Button rectangle
            bg_color: Background color
            text_color: Text color
        """
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)  # Border
        
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def is_point_in_rect(self, point: tuple[int, int], rect: pygame.Rect) -> bool:
        """Check if point is inside rectangle.
        
        Args:
            point: (x, y) coordinates
            rect: Rectangle to check
            
        Returns:
            True if point is inside rectangle
        """
        return rect.collidepoint(point)
