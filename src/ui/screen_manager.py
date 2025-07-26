"""Screen management system for handling screen transitions."""

from typing import List, Optional
import pygame
from .screen_base import ScreenBase


class ScreenManager:
    """Manages screen stack and transitions."""
    
    def __init__(self) -> None:
        """Initialize the screen manager."""
        self._stack: List[ScreenBase] = []
    
    def push(self, screen: ScreenBase) -> None:
        """Push a new screen onto the stack.
        
        Args:
            screen: Screen to push
        """
        screen.start_fade_in()
        self._stack.append(screen)
    
    def pop(self) -> None:
        """Pop the current screen from the stack."""
        if len(self._stack) > 1:
            self._stack.pop()
            # Start fade-in for the previous screen
            if self._stack:
                self._stack[-1].start_fade_in()
    
    def current(self) -> Optional[ScreenBase]:
        """Get the current screen.
        
        Returns:
            Current screen or None if stack is empty
        """
        return self._stack[-1] if self._stack else None
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle event on current screen."""
        current_screen = self.current()
        if current_screen:
            current_screen.handle_event(event)
    
    def update(self, dt: float) -> None:
        """Update current screen."""
        current_screen = self.current()
        if current_screen:
            current_screen.update(dt)
            current_screen.update_fade()
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw current screen."""
        current_screen = self.current()
        if current_screen:
            current_screen.draw(surface)
            current_screen.draw_fade(surface)
    
    def is_empty(self) -> bool:
        """Check if the screen stack is empty."""
        return len(self._stack) == 0
