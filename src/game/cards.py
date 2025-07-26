"""
TODO Sprint 03: ✅ EM PROGRESSO
✔ Card system expandido com tipos de carta
✔ Deck de 30 cartas para Knight
□ Mage e Archer decks únicos
□ Cartas especiais e combos
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class CardType(Enum):
    """Types of cards in the game."""
    ATTACK = "Attack"
    SKILL = "Skill" 
    POWER = "Power"
    SPECIAL = "Special"


@dataclass
class Card:
    """Represents a playable card in the game.
    
    This is a pure data class with no pygame dependencies.
    All game logic should be handled by other systems.
    """
    
    name: str
    cost: int
    card_type: CardType = CardType.ATTACK
    damage: int = 0
    block: int = 0
    heal: int = 0
    energy_gain: int = 0
    description: str = ""
    rarity: str = "Common"  # Common, Uncommon, Rare, Epic
    
    def __post_init__(self) -> None:
        """Validate card data after initialization."""
        if self.cost < 0:
            raise ValueError("Card cost cannot be negative")
        if self.damage < 0:
            raise ValueError("Card damage cannot be negative")
        if self.block < 0:
            raise ValueError("Card block cannot be negative")
        if self.heal < 0:
            raise ValueError("Card heal cannot be negative")
    
    def is_playable(self, available_energy: int) -> bool:
        """Check if card can be played with available energy.
        
        Args:
            available_energy: Current player energy
            
        Returns:
            True if card cost <= available energy
        """
        return self.cost <= available_energy
    
    def has_effect(self) -> bool:
        """Check if card has any effect.
        
        Returns:
            True if card has damage, block, heal or energy gain
        """
        return self.damage > 0 or self.block > 0 or self.heal > 0 or self.energy_gain > 0
    
    def get_type_color(self) -> tuple[int, int, int]:
        """Get RGB color for card type.
        
        Returns:
            RGB tuple for card type
        """
        colors = {
            CardType.ATTACK: (220, 50, 50),    # Red
            CardType.SKILL: (50, 150, 220),    # Blue  
            CardType.POWER: (150, 220, 50),    # Green
            CardType.SPECIAL: (200, 100, 255)  # Purple
        }
        return colors.get(self.card_type, (128, 128, 128))


# Knight-specific cards
KNIGHT_CARDS = [
    # Basic attacks
    Card(name="Strike", cost=1, card_type=CardType.ATTACK, damage=6, 
         description="Deal 6 damage.", rarity="Common"),
    Card(name="Heavy Strike", cost=2, card_type=CardType.ATTACK, damage=12,
         description="Deal 12 damage.", rarity="Common"),
    Card(name="Blade Flurry", cost=2, card_type=CardType.ATTACK, damage=4,
         description="Deal 4 damage 3 times.", rarity="Uncommon"),
    Card(name="Executioner's Blow", cost=3, card_type=CardType.ATTACK, damage=20,
         description="Deal 20 damage. High cost.", rarity="Rare"),
    
    # Defensive skills
    Card(name="Defend", cost=1, card_type=CardType.SKILL, block=5,
         description="Gain 5 Block.", rarity="Common"),
    Card(name="Shield Wall", cost=2, card_type=CardType.SKILL, block=12,
         description="Gain 12 Block.", rarity="Common"),
    Card(name="Guardian Stance", cost=1, card_type=CardType.SKILL, block=8,
         description="Gain 8 Block. Draw a card.", rarity="Uncommon"),
    Card(name="Fortress", cost=3, card_type=CardType.SKILL, block=20,
         description="Gain 20 Block. Immense defense.", rarity="Rare"),
    
    # Utility skills
    Card(name="Rest", cost=1, card_type=CardType.SKILL, heal=8,
         description="Heal 8 HP.", rarity="Common"),
    Card(name="Second Wind", cost=1, card_type=CardType.SKILL, energy_gain=2,
         description="Gain 2 Energy this turn.", rarity="Uncommon"),
    Card(name="Preparation", cost=0, card_type=CardType.SKILL,
         description="Draw 2 cards.", rarity="Uncommon"),
    
    # Power cards (permanent effects)
    Card(name="Sword Mastery", cost=2, card_type=CardType.POWER,
         description="Attacks deal +2 damage.", rarity="Uncommon"),
    Card(name="Armor Training", cost=1, card_type=CardType.POWER,
         description="Gain +3 Block from Defend cards.", rarity="Uncommon"),
    Card(name="Battle Fury", cost=3, card_type=CardType.POWER,
         description="Deal +1 damage for each attack played.", rarity="Rare"),
    
    # Special combos
    Card(name="Shield Bash", cost=1, card_type=CardType.SPECIAL, damage=3, block=3,
         description="Deal 3 damage and gain 3 Block.", rarity="Common"),
    Card(name="Counter Attack", cost=2, card_type=CardType.SPECIAL, damage=8, block=8,
         description="Deal 8 damage and gain 8 Block.", rarity="Uncommon"),
    Card(name="Knight's Valor", cost=2, card_type=CardType.SPECIAL, heal=6, energy_gain=1,
         description="Heal 6 HP and gain 1 Energy.", rarity="Rare"),
]


def create_knight_deck() -> list[Card]:
    """Create a balanced 30-card Knight deck.
    
    Returns:
        List of 30 cards for Knight class
    """
    deck = []
    
    # Basic cards (20 cards)
    for _ in range(7):
        deck.append(Card(name="Strike", cost=1, card_type=CardType.ATTACK, damage=6, 
                        description="Deal 6 damage.", rarity="Common"))
    
    for _ in range(5):
        deck.append(Card(name="Defend", cost=1, card_type=CardType.SKILL, block=5,
                        description="Gain 5 Block.", rarity="Common"))
    
    for _ in range(3):
        deck.append(Card(name="Shield Bash", cost=1, card_type=CardType.SPECIAL, damage=3, block=3,
                        description="Deal 3 damage and gain 3 Block.", rarity="Common"))
    
    for _ in range(3):
        deck.append(Card(name="Heavy Strike", cost=2, card_type=CardType.ATTACK, damage=12,
                        description="Deal 12 damage.", rarity="Common"))
    
    for _ in range(2):
        deck.append(Card(name="Rest", cost=1, card_type=CardType.SKILL, heal=8,
                        description="Heal 8 HP.", rarity="Common"))
    
    # Uncommon cards (7 cards)
    for _ in range(2):
        deck.append(Card(name="Guardian Stance", cost=1, card_type=CardType.SKILL, block=8,
                        description="Gain 8 Block. Draw a card.", rarity="Uncommon"))
    
    for _ in range(2):
        deck.append(Card(name="Second Wind", cost=1, card_type=CardType.SKILL, energy_gain=2,
                        description="Gain 2 Energy this turn.", rarity="Uncommon"))
    
    deck.append(Card(name="Blade Flurry", cost=2, card_type=CardType.ATTACK, damage=4,
                    description="Deal 4 damage 3 times.", rarity="Uncommon"))
    
    deck.append(Card(name="Counter Attack", cost=2, card_type=CardType.SPECIAL, damage=8, block=8,
                    description="Deal 8 damage and gain 8 Block.", rarity="Uncommon"))
    
    deck.append(Card(name="Preparation", cost=0, card_type=CardType.SKILL,
                    description="Draw 2 cards.", rarity="Uncommon"))
    
    # Rare cards (3 cards)
    deck.append(Card(name="Executioner's Blow", cost=3, card_type=CardType.ATTACK, damage=20,
                    description="Deal 20 damage. High cost.", rarity="Rare"))
    
    deck.append(Card(name="Battle Fury", cost=3, card_type=CardType.POWER,
                    description="Deal +1 damage for each attack played.", rarity="Rare"))
    
    deck.append(Card(name="Knight's Valor", cost=2, card_type=CardType.SPECIAL, heal=6, energy_gain=1,
                    description="Heal 6 HP and gain 1 Energy.", rarity="Rare"))
    
    return deck


def create_starter_deck() -> list[Card]:
    """Create the default starting deck (for compatibility).
    
    Returns:
        List of cards that make up the starter deck
    """
    return create_knight_deck()[:10]  # Return first 10 cards for testing


def create_card_by_name(name: str) -> Optional[Card]:
    """Create a card instance by name.
    
    Args:
        name: Name of the card to create
        
    Returns:
        Card instance or None if name not found
    """
    # Build registry from KNIGHT_CARDS
    card_registry = {card.name: card for card in KNIGHT_CARDS}
    
    # Add legacy cards for compatibility
    legacy_cards = {
        "Bash": Card(name="Bash", cost=2, card_type=CardType.ATTACK, damage=8, 
                    description="Deal 8 damage.", rarity="Common"),
        "Heal": Card(name="Heal", cost=1, card_type=CardType.SKILL, heal=5, 
                    description="Heal 5 HP.", rarity="Common"),
        "Power Strike": Card(name="Power Strike", cost=2, card_type=CardType.ATTACK, damage=12, 
                           description="Deal 12 damage.", rarity="Common"),
        "Iron Wall": Card(name="Iron Wall", cost=2, card_type=CardType.SKILL, block=12, 
                         description="Gain 12 Block.", rarity="Common"),
    }
    
    card_registry.update(legacy_cards)
    return card_registry.get(name)
