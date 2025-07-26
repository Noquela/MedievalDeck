"""
TODO Sprint 04:
□ CombatEngine com estado de luta
□ Sistema de energia e turno
□ Aplicação de efeitos de cartas
"""

from typing import Dict, Any, Optional
from .cards import Card
from .deck import Deck
from .enemy import Enemy, IntentType


class Player:
    """Represents the player character in combat."""
    
    def __init__(self, max_hp: int = 70, max_energy: int = 3) -> None:
        """Initialize player.
        
        Args:
            max_hp: Maximum hit points
            max_energy: Maximum energy per turn
        """
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_energy = max_energy
        self.energy = max_energy
        self.block = 0
    
    def take_damage(self, damage: int) -> int:
        """Apply damage to player, accounting for block.
        
        Args:
            damage: Incoming damage
            
        Returns:
            Actual damage dealt after block
        """
        if damage <= 0:
            return 0
        
        # Block reduces damage
        blocked_damage = min(damage, self.block)
        actual_damage = damage - blocked_damage
        self.block = max(0, self.block - damage)
        
        # Apply remaining damage to HP
        self.hp = max(0, self.hp - actual_damage)
        
        return actual_damage
    
    def add_block(self, block_amount: int) -> None:
        """Add block to player.
        
        Args:
            block_amount: Amount of block to add
        """
        if block_amount > 0:
            self.block += block_amount
    
    def heal(self, heal_amount: int) -> int:
        """Heal the player.
        
        Args:
            heal_amount: Amount to heal
            
        Returns:
            Actual amount healed
        """
        if heal_amount <= 0:
            return 0
        
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + heal_amount)
        return self.hp - old_hp
    
    def start_turn(self) -> None:
        """Called at start of player turn."""
        # Restore energy
        self.energy = self.max_energy
        # Block expires at start of turn
        self.block = 0
    
    def spend_energy(self, amount: int) -> bool:
        """Spend energy if available.
        
        Args:
            amount: Energy to spend
            
        Returns:
            True if energy was spent, False if insufficient
        """
        if self.energy >= amount:
            self.energy -= amount
            return True
        return False
    
    def is_dead(self) -> bool:
        """Check if player is dead.
        
        Returns:
            True if HP <= 0
        """
        return self.hp <= 0


class CombatEngine:
    """Manages combat state and mechanics."""
    
    def __init__(self, player_deck: Deck, enemy: Enemy) -> None:
        """Initialize combat.
        
        Args:
            player_deck: Player's deck
            enemy: Enemy to fight
        """
        self.deck = player_deck
        self.enemy = enemy
        self.player = Player()
        self.turn_count = 0
        self.combat_over = False
        self.player_won = False
        
        # Draw starting hand
        self.deck.draw(5)
    
    def play_card(self, card_index: int) -> Optional[Dict[str, Any]]:
        """Play a card from hand by index.
        
        Args:
            card_index: Index of card in hand to play
            
        Returns:
            Dictionary describing the effect, or None if card couldn't be played
        """
        if self.combat_over:
            return None
            
        if card_index < 0 or card_index >= len(self.deck.hand):
            return None
        
        card = self.deck.hand[card_index]
        
        # Check if player can afford the card
        if not self.player.spend_energy(card.cost):
            return None
        
        # Remove card from hand and add to discard
        self.deck.play_card(card)
        
        # Apply card effects
        effect = self._apply_card_effects(card)
        
        return effect
    
    def _apply_card_effects(self, card: Card) -> Dict[str, Any]:
        """Apply the effects of a played card.
        
        Args:
            card: Card to apply effects for
            
        Returns:
            Dictionary describing what happened
        """
        effects = {
            "card_name": card.name,
            "damage_dealt": 0,
            "block_gained": 0,
            "healing_done": 0
        }
        
        # Apply damage to enemy
        if card.damage > 0:
            damage_dealt = self.enemy.take_damage(card.damage)
            effects["damage_dealt"] = damage_dealt
        
        # Apply block to player
        if card.block > 0:
            self.player.add_block(card.block)
            effects["block_gained"] = card.block
        
        # Apply healing to player
        if card.heal > 0:
            healing_done = self.player.heal(card.heal)
            effects["healing_done"] = healing_done
        
        # Check if enemy died
        if self.enemy.is_dead():
            self.combat_over = True
            self.player_won = True
        
        return effects
    
    def end_turn(self) -> Dict[str, Any]:
        """End player turn and execute enemy turn.
        
        Returns:
            Dictionary describing enemy action
        """
        if self.combat_over:
            return {}
        
        # Discard hand and draw new cards
        self.deck.discard_hand()
        self.deck.draw(5)
        
        # Enemy turn
        enemy_action = self._execute_enemy_turn()
        
        # Start next player turn
        self.turn_count += 1
        self.player.start_turn()
        
        return enemy_action
    
    def _execute_enemy_turn(self) -> Dict[str, Any]:
        """Execute the enemy's turn.
        
        Returns:
            Dictionary describing enemy action
        """
        self.enemy.start_turn()
        
        intent_type, value = self.enemy.execute_intent()
        
        action = {
            "intent_type": intent_type.value,
            "value": value,
            "damage_dealt": 0
        }
        
        if intent_type == IntentType.ATTACK:
            damage_dealt = self.player.take_damage(value)
            action["damage_dealt"] = damage_dealt
            
            # Check if player died
            if self.player.is_dead():
                self.combat_over = True
                self.player_won = False
        
        elif intent_type == IntentType.DEFEND:
            self.enemy.add_block(value)
        
        elif intent_type == IntentType.HEAL:
            self.enemy.heal(value)
        
        elif intent_type == IntentType.BUFF:
            # Placeholder for buff effects
            pass
        
        elif intent_type == IntentType.DEBUFF:
            # Placeholder for debuff effects
            pass
        
        return action
    
    def can_play_any_card(self) -> bool:
        """Check if player can play any card in hand.
        
        Returns:
            True if at least one card in hand is playable
        """
        return any(card.is_playable(self.player.energy) for card in self.deck.hand)
    
    def get_playable_cards(self) -> list[int]:
        """Get indices of playable cards in hand.
        
        Returns:
            List of indices of cards that can be played
        """
        playable = []
        for i, card in enumerate(self.deck.hand):
            if card.is_playable(self.player.energy):
                playable.append(i)
        return playable
    
    def is_combat_over(self) -> bool:
        """Check if combat is finished.
        
        Returns:
            True if combat is over
        """
        return self.combat_over
    
    def did_player_win(self) -> bool:
        """Check if player won the combat.
        
        Returns:
            True if player won, False if lost or combat ongoing
        """
        return self.combat_over and self.player_won
