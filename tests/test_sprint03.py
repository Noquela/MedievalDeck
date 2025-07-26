"""
Tests for Sprint 03 - Card Game Mechanics
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from game.cards import Card, CardType, create_knight_deck, create_card_by_name
from game.deck import Deck
from game.combat import Player, CombatEngine
from game.enemy import create_goblin


class TestSprint03:
    """Test Sprint 03 - Card Game Mechanics."""
    
    def test_card_types_and_colors(self):
        """Test that cards have proper types and colors."""
        strike = create_card_by_name("Strike")
        defend = create_card_by_name("Defend") 
        
        assert strike.card_type == CardType.ATTACK
        assert defend.card_type == CardType.SKILL
        
        # Test color system
        attack_color = strike.get_type_color()
        skill_color = defend.get_type_color()
        
        assert attack_color == (220, 50, 50)  # Red for attacks
        assert skill_color == (50, 150, 220)  # Blue for skills
    
    def test_knight_deck_creation(self):
        """Test that Knight deck is properly balanced."""
        deck_cards = create_knight_deck()
        
        assert len(deck_cards) == 30  # Full 30-card deck
        
        # Count card types
        attack_cards = sum(1 for card in deck_cards if card.card_type == CardType.ATTACK)
        skill_cards = sum(1 for card in deck_cards if card.card_type == CardType.SKILL)
        
        assert attack_cards > 0
        assert skill_cards > 0
        
        # Check rarity distribution
        common_cards = sum(1 for card in deck_cards if card.rarity == "Common")
        uncommon_cards = sum(1 for card in deck_cards if card.rarity == "Uncommon")
        rare_cards = sum(1 for card in deck_cards if card.rarity == "Rare")
        
        assert common_cards >= 15  # Majority common
        assert uncommon_cards >= 5  # Some uncommon
        assert rare_cards >= 2     # Few rare
    
    def test_energy_system(self):
        """Test enhanced energy system with powers."""
        player = Player()
        
        # Test basic energy
        assert player.energy == 3
        assert player.max_energy == 3
        
        # Test energy spending
        assert player.spend_energy(2) == True
        assert player.energy == 1
        assert player.spend_energy(2) == False  # Not enough energy
        assert player.energy == 1  # Unchanged
        
        # Test energy gain
        player.add_energy(2)
        assert player.energy == 3
        
        # Test power system
        player.apply_power("energy_bonus", 1)
        player.start_turn()
        assert player.energy == 4  # 3 + 1 bonus
    
    def test_power_effects(self):
        """Test power card effects on player."""
        player = Player()
        
        # Test damage bonus
        player.apply_power("damage_bonus", 2)
        assert player.powers["damage_bonus"] == 2
        
        # Test block bonus
        player.apply_power("block_bonus", 3)
        player.add_block(5)  # Should be 5 + 3 = 8
        assert player.block == 8
    
    def test_combat_engine_integration(self):
        """Test that CombatEngine works with new card system."""
        deck = Deck(create_knight_deck())
        enemy = create_goblin()
        combat = CombatEngine(deck, enemy)
        
        # Test initial state
        assert len(combat.deck.hand) == 5  # Starting hand
        assert combat.player.energy == 3
        assert not combat.is_combat_over()
        
        # Test card playing
        initial_hand_size = len(combat.deck.hand)
        initial_energy = combat.player.energy
        
        # Find a playable card that doesn't draw additional cards
        simple_card_index = -1
        for i, card in enumerate(combat.deck.hand):
            if card.is_playable(combat.player.energy) and card.name not in ["Preparation", "Guardian Stance"]:
                simple_card_index = i
                break
        
        if simple_card_index >= 0:
            result = combat.play_card(simple_card_index)
            
            if result:  # If card was playable
                expected_hand_size = initial_hand_size - 1
                # Account for cards that draw additional cards
                expected_hand_size += result.get("cards_drawn", 0)
                
                assert len(combat.deck.hand) == expected_hand_size
                assert combat.player.energy < initial_energy  # Energy spent
    
    def test_special_card_effects(self):
        """Test special cards with unique effects."""
        # Test Blade Flurry (multi-hit)
        blade_flurry = create_card_by_name("Blade Flurry")
        assert blade_flurry.name == "Blade Flurry"
        assert blade_flurry.damage == 4
        assert blade_flurry.description == "Deal 4 damage 3 times."
        
        # Test Shield Bash (combo effect)
        shield_bash = create_card_by_name("Shield Bash")
        assert shield_bash.damage > 0
        assert shield_bash.block > 0
        assert shield_bash.card_type == CardType.SPECIAL
        
        # Test Second Wind (energy gain)
        second_wind = create_card_by_name("Second Wind")
        assert second_wind.energy_gain == 2
        assert second_wind.card_type == CardType.SKILL
    
    def test_deck_hand_management(self):
        """Test improved deck and hand management."""
        deck = Deck(create_knight_deck())
        
        # Test initial state
        assert len(deck.hand) == 0
        assert len(deck.draw_pile) == 30
        
        # Test drawing cards
        drawn = deck.draw(5)
        assert len(drawn) == 5
        assert len(deck.hand) == 5
        assert len(deck.draw_pile) == 25
        
        # Test playing cards (discard)
        if deck.hand:
            card = deck.hand[0]
            deck.play_card(card)
            assert len(deck.hand) == 4
            assert len(deck.discard_pile) == 1
        
        # Test end turn (discard all, draw new)
        deck.discard_hand()
        assert len(deck.hand) == 0
        assert len(deck.discard_pile) == 5
        
        new_cards = deck.draw(5)
        assert len(new_cards) == 5
        assert len(deck.hand) == 5
    
    def test_combat_flow_integration(self):
        """Test complete combat flow with new mechanics."""
        deck = Deck(create_knight_deck())
        enemy = create_goblin()
        combat = CombatEngine(deck, enemy)
        
        initial_player_hp = combat.player.hp
        initial_enemy_hp = combat.enemy.hp
        
        # Find and play an attack card
        attack_played = False
        for i, card in enumerate(combat.deck.hand):
            if card.card_type == CardType.ATTACK and card.is_playable(combat.player.energy):
                result = combat.play_card(i)
                if result and result["damage_dealt"] > 0:
                    attack_played = True
                    assert combat.enemy.hp < initial_enemy_hp
                break
        
        # End turn to trigger enemy action
        enemy_action = combat.end_turn()
        
        if enemy_action.get("damage_dealt", 0) > 0:
            assert combat.player.hp < initial_player_hp
        
        # Verify new turn started
        assert combat.turn_count > 0
        assert len(combat.deck.hand) == 5  # New hand drawn
    
    def test_card_playability(self):
        """Test card playability based on energy cost."""
        player = Player()
        
        # Create test cards
        cheap_card = Card("Test Strike", cost=1, damage=5)
        expensive_card = Card("Test Power", cost=4, damage=15)
        
        # Test with full energy
        assert cheap_card.is_playable(player.energy)
        assert not expensive_card.is_playable(player.energy)
        
        # Test after spending energy
        player.spend_energy(2)
        assert cheap_card.is_playable(player.energy)
        assert not expensive_card.is_playable(player.energy)
        
        # Test with no energy
        player.spend_energy(1)
        assert not cheap_card.is_playable(player.energy)
        assert not expensive_card.is_playable(player.energy)
