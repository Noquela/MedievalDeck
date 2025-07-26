"""Character selection screen."""

import pygame
from typing import TYPE_CHECKING, Optional
from .screen_base import ScreenBase
from engine.resources import load_image

if TYPE_CHECKING:
    from .screen_manager import ScreenManager


class CharacterSelectScreen(ScreenBase):
    """Character selection screen."""
    
    def __init__(self, screen_manager: 'ScreenManager') -> None:
        """Initialize character selection screen.
        
        Args:
            screen_manager: Reference to screen manager for navigation
        """
        super().__init__()
        self.screen_manager = screen_manager
        
        # Load background with blur effect
        self.background = load_image("assets/bg/card_selection.png", cache=True)
        
        # Character options
        self.characters = [
            {"name": "Knight", "sprite_path": "assets/sheets/knight_idle.png", "description": "Heavily armored warrior with strong defense"},
            {"name": "Mage", "sprite_path": None, "description": "Magical spellcaster with powerful abilities"},  # Not yet generated
            {"name": "Archer", "sprite_path": None, "description": "Ranged fighter with precision attacks"}   # Not yet generated
        ]
        
        # Character selection
        self.selected_character = 0
        self.character_rects = []
        
        # Setup character card positions (3 cards horizontally centered)
        card_width = 400
        card_height = 600
        spacing = 100
        total_width = 3 * card_width + 2 * spacing
        start_x = (3440 - total_width) // 2
        
        for i in range(3):
            x = start_x + i * (card_width + spacing)
            y = (1440 - card_height) // 2
            self.character_rects.append(pygame.Rect(x, y, card_width, card_height))
        
        # Load character sprites
        self.character_sprites = []
        for char in self.characters:
            if char["sprite_path"] and load_image(char["sprite_path"], cache=True):
                sprite_sheet = load_image(char["sprite_path"], cache=True)
                # Extract first frame (assuming 512x512 per frame)
                sprite = sprite_sheet.subsurface((0, 0, 512, 512))
                sprite = pygame.transform.scale(sprite, (200, 200))
                self.character_sprites.append(sprite)
            else:
                self.character_sprites.append(None)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle character selection events."""
        if event.type == pygame.MOUSEMOTION:
            # Check which character is hovered
            for i, rect in enumerate(self.character_rects):
                if rect.collidepoint(event.pos):
                    self.selected_character = i
                    break
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicking on a character card
                for i, rect in enumerate(self.character_rects):
                    if rect.collidepoint(event.pos):
                        self._select_character(i)
                        break
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
            elif event.key == pygame.K_RIGHT:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_character(self.selected_character)
            elif event.key == pygame.K_ESCAPE:
                self.screen_manager.pop()  # Go back to menu
    
    def _select_character(self, character_index: int) -> None:
        """Select a character and proceed to combat.
        
        Args:
            character_index: Index of selected character
        """
        selected_char = self.characters[character_index]
        from .combat_screen import CombatScreen
        self.screen_manager.push(CombatScreen(self.screen_manager, selected_char))
    
    def update(self, dt: float) -> None:
        """Update character selection state."""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the character selection screen."""
        # Draw background with blur effect
        if self.background:
            scaled_bg = pygame.transform.scale(self.background, (3440, 1440))
            # Apply a slight blur effect by scaling down and up
            blur_bg = pygame.transform.smoothscale(scaled_bg, (1720, 720))
            blur_bg = pygame.transform.smoothscale(blur_bg, (3440, 1440))
            blur_bg.set_alpha(180)  # Make it semi-transparent
            surface.blit(blur_bg, (0, 0))
        else:
            surface.fill((35, 25, 45))  # Fallback dark purple background
        
        # Draw title
        title_text = self.font_title.render("Escolha seu Herói", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(1720, 150))
        surface.blit(title_text, title_rect)
        
        # Draw character cards
        for i, (char, rect) in enumerate(zip(self.characters, self.character_rects)):
            # Card background
            if i == self.selected_character:
                card_color = (80, 60, 40)
                border_color = (255, 215, 0)
                border_width = 5
            else:
                card_color = (50, 40, 30)
                border_color = (150, 120, 80)
                border_width = 2
            
            pygame.draw.rect(surface, card_color, rect)
            pygame.draw.rect(surface, border_color, rect, border_width)
            
            # Character sprite
            sprite_y = rect.y + 50
            if self.character_sprites[i]:
                sprite_rect = self.character_sprites[i].get_rect(center=(rect.centerx, sprite_y + 100))
                surface.blit(self.character_sprites[i], sprite_rect)
            else:
                # Placeholder for missing sprites
                placeholder_rect = pygame.Rect(rect.centerx - 100, sprite_y, 200, 200)
                pygame.draw.rect(surface, (100, 100, 100), placeholder_rect)
                placeholder_text = self.font_medium.render("?", True, (255, 255, 255))
                text_rect = placeholder_text.get_rect(center=placeholder_rect.center)
                surface.blit(placeholder_text, text_rect)
            
            # Character name
            name_text = self.font_large.render(char["name"], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(rect.centerx, sprite_y + 250))
            surface.blit(name_text, name_rect)
            
            # Character description (word wrap)
            desc_words = char["description"].split()
            lines = []
            current_line = []
            
            for word in desc_words:
                test_line = " ".join(current_line + [word])
                test_surface = self.font_small.render(test_line, True, (200, 200, 200))
                if test_surface.get_width() <= rect.width - 20:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Draw description lines
            for j, line in enumerate(lines):
                desc_text = self.font_small.render(line, True, (200, 200, 200))
                desc_rect = desc_text.get_rect(center=(rect.centerx, sprite_y + 300 + j * 25))
                surface.blit(desc_text, desc_rect)
        
        # Draw instructions
        instructions = [
            "Use as setas ou mouse para escolher",
            "ENTER/ESPAÇO para confirmar • ESC para voltar"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (180, 180, 180))
            inst_rect = inst_text.get_rect(center=(1720, 1300 + i * 30))
            surface.blit(inst_text, inst_rect)
