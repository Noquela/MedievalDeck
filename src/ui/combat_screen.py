"""Combat screen where the actual card game takes place."""

import pygame
from typing import TYPE_CHECKING, Dict, Any
from .screen_base import ScreenBase
from engine.resources import load_image

if TYPE_CHECKING:
    from .screen_manager import ScreenManager


class CombatScreen(ScreenBase):
    """Combat screen with arena background."""
    
    def __init__(self, screen_manager: 'ScreenManager', selected_character: Dict[str, Any]) -> None:
        """Initialize combat screen.
        
        Args:
            screen_manager: Reference to screen manager for navigation
            selected_character: Character data from selection screen
        """
        super().__init__()
        self.screen_manager = screen_manager
        self.selected_character = selected_character
        
        # Load arena background
        self.background = load_image("assets/bg/arena.png", cache=True)
        
        # Load card frame for UI elements
        self.card_frame = load_image("assets/ui/card_frame.png", cache=True)
        
        # Combat state
        self.player_health = 100
        self.enemy_health = 100
        
        # Load character sprite
        self.character_sprite = None
        if selected_character.get("sprite_path"):
            sprite_sheet = load_image(selected_character["sprite_path"], cache=True)
            if sprite_sheet:
                # Extract first frame
                self.character_sprite = sprite_sheet.subsurface((0, 0, 512, 512))
                self.character_sprite = pygame.transform.scale(self.character_sprite, (200, 200))
        
        # Placeholder enemy sprite (using goblin)
        self.enemy_sprite = None
        goblin_sheet = load_image("assets/sheets/goblin_idle.png", cache=True)
        if goblin_sheet:
            # Extract first frame (assuming 424x424 per frame based on the corrected dimensions)
            frame_width = 424  # 4240 / 10 frames
            self.enemy_sprite = goblin_sheet.subsurface((0, 0, frame_width, 424))
            self.enemy_sprite = pygame.transform.scale(self.enemy_sprite, (180, 180))
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle combat events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Go back to character selection
                self.screen_manager.pop()
            elif event.key == pygame.K_SPACE:
                # Placeholder combat action
                self._attack_enemy()
            elif event.key == pygame.K_q:
                # Quick quit to menu (for testing)
                # Pop twice to get back to menu
                self.screen_manager.pop()  # Back to character select
                self.screen_manager.pop()  # Back to menu
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Placeholder: click anywhere to attack
                self._attack_enemy()
    
    def _attack_enemy(self) -> None:
        """Placeholder attack function."""
        import random
        damage = random.randint(10, 25)
        self.enemy_health = max(0, self.enemy_health - damage)
        
        # Enemy counter-attack
        if self.enemy_health > 0:
            counter_damage = random.randint(8, 20)
            self.player_health = max(0, self.player_health - counter_damage)
    
    def update(self, dt: float) -> None:
        """Update combat state."""
        # Check for game over conditions
        if self.player_health <= 0 or self.enemy_health <= 0:
            # For now, just reset health (placeholder)
            if self.player_health <= 0:
                self.player_health = 100
            if self.enemy_health <= 0:
                self.enemy_health = 100
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the combat screen."""
        # Draw arena background
        if self.background:
            scaled_bg = pygame.transform.scale(self.background, (3440, 1440))
            surface.blit(scaled_bg, (0, 0))
        else:
            surface.fill((40, 30, 25))  # Fallback dark brown background
        
        # Draw UI overlay
        overlay = pygame.Surface((3440, 1440))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Draw character sprites
        if self.character_sprite:
            char_x = 800
            char_y = 600
            surface.blit(self.character_sprite, (char_x, char_y))
            
            # Character name and health
            char_name = self.font_large.render(self.selected_character["name"], True, (255, 255, 255))
            char_rect = char_name.get_rect(center=(char_x + 100, char_y - 50))
            surface.blit(char_name, char_rect)
            
            # Player health bar
            self._draw_health_bar(surface, char_x, char_y - 20, self.player_health, 100, (0, 255, 0))
        
        if self.enemy_sprite:
            enemy_x = 2400
            enemy_y = 600
            surface.blit(self.enemy_sprite, (enemy_x, enemy_y))
            
            # Enemy name and health
            enemy_name = self.font_large.render("Goblin Scout", True, (255, 255, 255))
            enemy_rect = enemy_name.get_rect(center=(enemy_x + 90, enemy_y - 50))
            surface.blit(enemy_name, enemy_rect)
            
            # Enemy health bar
            self._draw_health_bar(surface, enemy_x, enemy_y - 20, self.enemy_health, 100, (255, 0, 0))
        
        # Draw combat UI
        self._draw_combat_ui(surface)
        
        # Draw instructions
        instructions = [
            f"Combate: {self.selected_character['name']} vs Goblin Scout",
            "ESPAÇO ou clique para atacar",
            "ESC para voltar • Q para menu principal"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (255, 255, 255))
            inst_rect = inst_text.get_rect(center=(1720, 100 + i * 30))
            # Add shadow for better readability
            shadow_text = self.font_small.render(instruction, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(1722, 102 + i * 30))
            surface.blit(shadow_text, shadow_rect)
            surface.blit(inst_text, inst_rect)
    
    def _draw_health_bar(self, surface: pygame.Surface, x: int, y: int, 
                        current_health: int, max_health: int, color: tuple) -> None:
        """Draw a health bar.
        
        Args:
            surface: Surface to draw on
            x: X position
            y: Y position
            current_health: Current health value
            max_health: Maximum health value
            color: Bar color (R, G, B)
        """
        bar_width = 200
        bar_height = 20
        
        # Background bar
        bg_rect = pygame.Rect(x, y, bar_width, bar_height)
        pygame.draw.rect(surface, (50, 50, 50), bg_rect)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)
        
        # Health bar
        health_ratio = current_health / max_health
        health_width = int(bar_width * health_ratio)
        health_rect = pygame.Rect(x, y, health_width, bar_height)
        pygame.draw.rect(surface, color, health_rect)
        
        # Health text
        health_text = self.font_small.render(f"{current_health}/{max_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        surface.blit(health_text, text_rect)
    
    def _draw_combat_ui(self, surface: pygame.Surface) -> None:
        """Draw combat UI elements."""
        # Card hand area (bottom of screen)
        hand_y = 1200
        hand_height = 240
        
        # Semi-transparent hand background
        hand_bg = pygame.Surface((3440, hand_height))
        hand_bg.set_alpha(150)
        hand_bg.fill((20, 20, 20))
        surface.blit(hand_bg, (0, hand_y))
        
        # Placeholder cards in hand
        card_width = 150
        card_height = 200
        cards_count = 5
        spacing = 20
        total_width = cards_count * card_width + (cards_count - 1) * spacing
        start_x = (3440 - total_width) // 2
        
        for i in range(cards_count):
            card_x = start_x + i * (card_width + spacing)
            card_y = hand_y + 20
            
            # Draw card placeholder
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            pygame.draw.rect(surface, (60, 45, 30), card_rect)
            pygame.draw.rect(surface, (120, 90, 60), card_rect, 2)
            
            # Card number
            card_text = self.font_medium.render(str(i + 1), True, (255, 255, 255))
            text_rect = card_text.get_rect(center=card_rect.center)
            surface.blit(card_text, text_rect)
