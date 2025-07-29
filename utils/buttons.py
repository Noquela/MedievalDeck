"""
Button system for Medieval Deck
Reusable UI components optimized for 3440x1440 ultrawide resolution
"""

import pygame
from config import WHITE, BLACK, GRAY, DARK_GRAY, GOLD

class Button:
    """
    Reusable button class with hover effects and click detection
    Optimized for ultrawide display with appropriate sizing
    """
    
    def __init__(self, x, y, width, height, text, font, 
                 color=WHITE, bg_color=DARK_GRAY, hover_color=GRAY):
        """
        Initialize button with position, size, and styling
        
        Args:
            x, y: Button position
            width, height: Button dimensions
            text: Button text
            font: Pygame font object
            color: Text color
            bg_color: Background color
            hover_color: Hover state color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_clicked = False
        
        # Pre-render text for performance
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def handle_event(self, event):
        """
        Handle mouse events for button interaction
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if button was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_clicked = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_clicked = False
                
        return False
        
    def draw(self, screen):
        """
        Draw button with current state styling
        
        Args:
            screen: Pygame surface to draw on
        """
        # Choose color based on state
        current_bg = self.hover_color if self.is_hovered else self.bg_color
        
        # Draw button background
        pygame.draw.rect(screen, current_bg, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 3)  # Border
        
        # Draw text
        screen.blit(self.text_surface, self.text_rect)


class MenuButtonSet:
    """
    Manages a set of menu buttons with consistent styling and layout
    Optimized for ultrawide resolution with proper spacing
    """
    
    def __init__(self, screen_width, screen_height, font):
        """
        Initialize button set with screen dimensions and font
        
        Args:
            screen_width: Screen width for centering
            screen_height: Screen height for vertical positioning
            font: Font for button text
        """
        self.buttons = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        
        # Button dimensions optimized for ultrawide
        self.button_width = 400
        self.button_height = 80
        self.button_spacing = 100
        
    def add_button(self, text, callback=None):
        """
        Add a button to the set
        
        Args:
            text: Button text
            callback: Function to call when button is clicked
        """
        # Calculate position for centered vertical layout
        button_count = len(self.buttons)
        total_height = (button_count * self.button_height + 
                       (button_count - 1) * self.button_spacing)
        
        start_y = (self.screen_height - total_height) // 2
        button_y = start_y + button_count * (self.button_height + self.button_spacing)
        button_x = (self.screen_width - self.button_width) // 2
        
        button = Button(
            button_x, button_y, 
            self.button_width, self.button_height,
            text, self.font
        )
        
        self.buttons.append({
            'button': button,
            'callback': callback,
            'text': text
        })
        
    def handle_events(self, events):
        """
        Handle events for all buttons in the set
        
        Args:
            events: List of pygame events
            
        Returns:
            str: Text of clicked button, or None
        """
        for event in events:
            for button_data in self.buttons:
                if button_data['button'].handle_event(event):
                    if button_data['callback']:
                        button_data['callback']()
                    return button_data['text']
        return None
        
    def draw(self, screen):
        """
        Draw all buttons in the set
        
        Args:
            screen: Pygame surface to draw on
        """
        for button_data in self.buttons:
            button_data['button'].draw(screen)
            
    def get_button_by_text(self, text):
        """
        Get button object by its text
        
        Args:
            text: Button text to search for
            
        Returns:
            Button object or None
        """
        for button_data in self.buttons:
            if button_data['text'] == text:
                return button_data['button']
        return None