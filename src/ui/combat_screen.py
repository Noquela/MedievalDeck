"""Combat screen where the actual card game takes place."""

import pygame
from typing import TYPE_CHECKING, Dict, Any, Optional
from .screen_base import ScreenBase
from engine.resources import load_image
from game.combat import CombatEngine
from game.deck import Deck
from game.cards import create_knight_deck
from game.enemy import create_goblin

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
        
        # Initialize combat engine
        knight_deck = Deck(create_knight_deck())
        goblin_enemy = create_goblin()
        self.combat_engine = CombatEngine(knight_deck, goblin_enemy)
        
        # UI state
        self.selected_card_index = -1
        self.card_hover_index = -1
        self.end_turn_button_rect = pygame.Rect(3200, 1300, 200, 50)
        
        # Animation and feedback
        self.last_action_text = ""
        self.action_text_timer = 0
        self.show_enemy_intent = True
        
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
            elif event.key == pygame.K_e:
                # End turn
                self._end_turn()
            elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                # Play card by number key
                card_index = event.key - pygame.K_1
                self._play_card(card_index)
            elif event.key == pygame.K_q:
                # Quick quit to menu (for testing)
                self.screen_manager.pop()  # Back to character select
                self.screen_manager.pop()  # Back to menu
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if clicked on End Turn button
                if self.end_turn_button_rect.collidepoint(mouse_pos):
                    self._end_turn()
                    return
                
                # Check if clicked on a card
                card_index = self._get_card_at_position(mouse_pos)
                if card_index >= 0:
                    self._play_card(card_index)
        
        elif event.type == pygame.MOUSEMOTION:
            # Update card hover state
            mouse_pos = pygame.mouse.get_pos()
            self.card_hover_index = self._get_card_at_position(mouse_pos)
    
    def _get_card_at_position(self, pos: tuple[int, int]) -> int:
        """Get the index of the card at the given position.
        
        Args:
            pos: Mouse position (x, y)
            
        Returns:
            Card index or -1 if no card
        """
        x, y = pos
        hand_y = 1200
        card_width = 150
        card_height = 200
        cards_count = len(self.combat_engine.deck.hand)
        
        if y < hand_y or y > hand_y + card_height:
            return -1
        
        spacing = 20
        total_width = cards_count * card_width + (cards_count - 1) * spacing
        start_x = (3440 - total_width) // 2
        
        for i in range(cards_count):
            card_x = start_x + i * (card_width + spacing)
            if x >= card_x and x <= card_x + card_width:
                return i
        
        return -1
    
    def _play_card(self, card_index: int) -> None:
        """Play a card from hand.
        
        Args:
            card_index: Index of card to play
        """
        if self.combat_engine.is_combat_over():
            return
        
        result = self.combat_engine.play_card(card_index)
        if result:
            # Update action feedback
            card_name = result["card_name"]
            damage = result["damage_dealt"]
            block = result["block_gained"]
            heal = result["healing_done"]
            energy = result["energy_gained"]
            cards_drawn = result["cards_drawn"]
            
            feedback_parts = [f"Played {card_name}"]
            if damage > 0:
                feedback_parts.append(f"dealt {damage} damage")
            if block > 0:
                feedback_parts.append(f"gained {block} block")
            if heal > 0:
                feedback_parts.append(f"healed {heal} HP")
            if energy > 0:
                feedback_parts.append(f"gained {energy} energy")
            if cards_drawn > 0:
                feedback_parts.append(f"drew {cards_drawn} cards")
            
            self.last_action_text = ", ".join(feedback_parts)
            self.action_text_timer = 3.0  # Show for 3 seconds
            
            # Check if combat ended
            if self.combat_engine.is_combat_over():
                self._handle_combat_end()
    
    def _end_turn(self) -> None:
        """End the player's turn."""
        if self.combat_engine.is_combat_over():
            return
        
        enemy_action = self.combat_engine.end_turn()
        
        if enemy_action:
            # Show enemy action feedback
            intent = enemy_action["intent_type"]
            value = enemy_action["value"]
            damage = enemy_action.get("damage_dealt", 0)
            
            if intent == "Attack":
                if damage > 0:
                    self.last_action_text = f"Enemy attacked for {damage} damage!"
                else:
                    self.last_action_text = f"Enemy attack blocked!"
            elif intent == "Defend":
                self.last_action_text = f"Enemy gained {value} block"
            elif intent == "Heal":
                self.last_action_text = f"Enemy healed {value} HP"
            else:
                self.last_action_text = f"Enemy used {intent}"
            
            self.action_text_timer = 2.0
        
        # Check if combat ended
        if self.combat_engine.is_combat_over():
            self._handle_combat_end()
    
    def _handle_combat_end(self) -> None:
        """Handle the end of combat."""
        from .result_screen import ResultScreen
        
        won = self.combat_engine.did_player_win()
        result_screen = ResultScreen(self.screen_manager, won)
        self.screen_manager.push(result_screen)
    
    def update(self, dt: float) -> None:
        """Update combat state."""
        # Update action text timer
        if self.action_text_timer > 0:
            self.action_text_timer -= dt
        
        # Check if combat is over
        if self.combat_engine.is_combat_over():
            # Combat is handled in _handle_combat_end
            pass
    
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
        
        # Draw character sprites and combat info
        self._draw_combat_entities(surface)
        
        # Draw card hand and UI
        self._draw_combat_ui(surface)
        
        # Draw action feedback
        if self.action_text_timer > 0 and self.last_action_text:
            action_text = self.font_medium.render(self.last_action_text, True, (255, 255, 100))
            action_rect = action_text.get_rect(center=(1720, 800))
            
            # Draw background for text
            bg_rect = action_rect.copy()
            bg_rect.inflate_ip(20, 10)
            pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
            
            surface.blit(action_text, action_rect)
    
    def _draw_combat_entities(self, surface: pygame.Surface) -> None:
        """Draw player and enemy with health bars."""
        # Player info (left side)
        player = self.combat_engine.player
        player_x, player_y = 800, 600
        
        if self.character_sprite:
            surface.blit(self.character_sprite, (player_x, player_y))
        
        # Player name and stats
        char_name = self.font_large.render(self.selected_character["name"], True, (255, 255, 255))
        char_rect = char_name.get_rect(center=(player_x + 100, player_y - 50))
        surface.blit(char_name, char_rect)
        
        # Player health bar
        health_bar_width = 200
        health_bar_height = 20
        health_ratio = player.hp / player.max_hp
        
        health_bar_bg = pygame.Rect(player_x, player_y - 30, health_bar_width, health_bar_height)
        health_bar_fg = pygame.Rect(player_x, player_y - 30, int(health_bar_width * health_ratio), health_bar_height)
        
        pygame.draw.rect(surface, (60, 20, 20), health_bar_bg)
        pygame.draw.rect(surface, (200, 50, 50), health_bar_fg)
        pygame.draw.rect(surface, (255, 255, 255), health_bar_bg, 2)
        
        # Player health text
        health_text = self.font_small.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 255, 255))
        surface.blit(health_text, (player_x, player_y - 50))
        
        # Player block (if any)
        if player.block > 0:
            block_text = self.font_small.render(f"Block: {player.block}", True, (100, 150, 255))
            surface.blit(block_text, (player_x, player_y + 210))
        
        # Player energy
        energy_text = self.font_medium.render(f"Energy: {player.energy}/{player.max_energy}", True, (255, 255, 100))
        surface.blit(energy_text, (player_x, player_y + 230))
        
        # Enemy info (right side)
        enemy = self.combat_engine.enemy
        enemy_x, enemy_y = 2400, 600
        
        if self.enemy_sprite:
            surface.blit(self.enemy_sprite, (enemy_x, enemy_y))
        
        # Enemy name
        enemy_name = self.font_large.render("Goblin", True, (255, 255, 255))
        enemy_rect = enemy_name.get_rect(center=(enemy_x + 90, enemy_y - 50))
        surface.blit(enemy_name, enemy_rect)
        
        # Enemy health bar
        enemy_health_ratio = enemy.hp / enemy.max_hp
        enemy_health_bar_bg = pygame.Rect(enemy_x, enemy_y - 30, health_bar_width, health_bar_height)
        enemy_health_bar_fg = pygame.Rect(enemy_x, enemy_y - 30, int(health_bar_width * enemy_health_ratio), health_bar_height)
        
        pygame.draw.rect(surface, (60, 20, 20), enemy_health_bar_bg)
        pygame.draw.rect(surface, (200, 50, 50), enemy_health_bar_fg)
        pygame.draw.rect(surface, (255, 255, 255), enemy_health_bar_bg, 2)
        
        # Enemy health text
        enemy_health_text = self.font_small.render(f"HP: {enemy.hp}/{enemy.max_hp}", True, (255, 255, 255))
        surface.blit(enemy_health_text, (enemy_x, enemy_y - 50))
        
        # Enemy block (if any)
        if enemy.block > 0:
            enemy_block_text = self.font_small.render(f"Block: {enemy.block}", True, (100, 150, 255))
            surface.blit(enemy_block_text, (enemy_x, enemy_y + 190))
        
        # Enemy intent (what they plan to do next turn)
        if self.show_enemy_intent and enemy.current_intent:
            intent = enemy.current_intent
            intent_text = f"Intent: {intent.type.value} {intent.value}"
            intent_surface = self.font_small.render(intent_text, True, (255, 200, 100))
            surface.blit(intent_surface, (enemy_x, enemy_y + 210))
    
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
        
        # Draw actual cards in hand
        cards = self.combat_engine.deck.hand
        card_width = 150
        card_height = 200
        spacing = 20
        
        if cards:
            total_width = len(cards) * card_width + (len(cards) - 1) * spacing
            start_x = (3440 - total_width) // 2
            
            for i, card in enumerate(cards):
                card_x = start_x + i * (card_width + spacing)
                card_y = hand_y + 20
                
                # Check if card is playable
                is_playable = card.is_playable(self.combat_engine.player.energy)
                is_hovered = i == self.card_hover_index
                
                # Draw card background
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                
                if is_hovered:
                    # Hover effect
                    card_y -= 10
                    card_rect.y = card_y
                
                # Card color based on type and playability
                if is_playable:
                    card_color = card.get_type_color()
                else:
                    card_color = (60, 60, 60)  # Grayed out
                
                pygame.draw.rect(surface, card_color, card_rect)
                pygame.draw.rect(surface, (255, 255, 255), card_rect, 2)
                
                # Draw card frame if available
                if self.card_frame:
                    scaled_frame = pygame.transform.scale(self.card_frame, (card_width, card_height))
                    surface.blit(scaled_frame, card_rect)
                
                # Card name (truncated if too long)
                card_name = card.name
                if len(card_name) > 12:
                    card_name = card_name[:10] + "..."
                
                name_text = self.font_small.render(card_name, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 15))
                surface.blit(name_text, name_rect)
                
                # Card cost
                cost_text = self.font_medium.render(str(card.cost), True, (255, 255, 100))
                cost_rect = cost_text.get_rect(center=(card_x + 20, card_y + 20))
                pygame.draw.circle(surface, (0, 0, 0), cost_rect.center, 15)
                pygame.draw.circle(surface, (255, 255, 100), cost_rect.center, 15, 2)
                surface.blit(cost_text, cost_rect)
                
                # Card effects
                effects_y = card_y + 50
                
                if card.damage > 0:
                    damage_text = self.font_small.render(f"DMG: {card.damage}", True, (255, 100, 100))
                    surface.blit(damage_text, (card_x + 5, effects_y))
                    effects_y += 20
                
                if card.block > 0:
                    block_text = self.font_small.render(f"BLK: {card.block}", True, (100, 150, 255))
                    surface.blit(block_text, (card_x + 5, effects_y))
                    effects_y += 20
                
                if card.heal > 0:
                    heal_text = self.font_small.render(f"HEAL: {card.heal}", True, (100, 255, 100))
                    surface.blit(heal_text, (card_x + 5, effects_y))
                    effects_y += 20
                
                if card.energy_gain > 0:
                    energy_text = self.font_small.render(f"ENERGY: +{card.energy_gain}", True, (255, 255, 100))
                    surface.blit(energy_text, (card_x + 5, effects_y))
                    effects_y += 20
                
                # Card number for keyboard selection
                number_text = self.font_small.render(str(i + 1), True, (255, 255, 255))
                number_rect = number_text.get_rect(center=(card_x + card_width - 15, card_y + card_height - 15))
                pygame.draw.circle(surface, (0, 0, 0), number_rect.center, 12)
                surface.blit(number_text, number_rect)
                
                # Show description on hover
                if is_hovered and card.description:
                    desc_text = self.font_small.render(card.description, True, (255, 255, 255))
                    desc_rect = desc_text.get_rect(center=(card_x + card_width // 2, card_y - 25))
                    
                    # Background for description
                    bg_rect = desc_rect.copy()
                    bg_rect.inflate_ip(10, 5)
                    pygame.draw.rect(surface, (0, 0, 0, 200), bg_rect)
                    pygame.draw.rect(surface, (255, 255, 255), bg_rect, 1)
                    surface.blit(desc_text, desc_rect)
        
        # End Turn button
        pygame.draw.rect(surface, (100, 50, 50), self.end_turn_button_rect)
        pygame.draw.rect(surface, (255, 255, 255), self.end_turn_button_rect, 2)
        
        end_turn_text = self.font_medium.render("End Turn (E)", True, (255, 255, 255))
        end_turn_text_rect = end_turn_text.get_rect(center=self.end_turn_button_rect.center)
        surface.blit(end_turn_text, end_turn_text_rect)
        
        # Turn and deck info
        turn_text = self.font_medium.render(f"Turn: {self.combat_engine.turn_count + 1}", True, (255, 255, 255))
        surface.blit(turn_text, (50, 50))
        
        deck_info = f"Deck: {self.combat_engine.deck.get_draw_pile_size()} | Discard: {len(self.combat_engine.deck.discard_pile)}"
        deck_text = self.font_small.render(deck_info, True, (255, 255, 255))
        surface.blit(deck_text, (50, 80))
        
        # Instructions
        instructions = [
            "Click cards or press 1-9 to play • E to end turn",
            "ESC to go back • Q for menu"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.font_small.render(instruction, True, (255, 255, 255))
            inst_rect = inst_text.get_rect(center=(1720, 100 + i * 25))
            
            # Shadow for readability
            shadow_text = self.font_small.render(instruction, True, (0, 0, 0))
            shadow_rect = shadow_text.get_rect(center=(1722, 102 + i * 25))
            surface.blit(shadow_text, shadow_rect)
            surface.blit(inst_text, inst_rect)
