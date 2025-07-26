"""
TODO Sprint 02:
□ Card dataclass com todos os campos
□ Tipos de carta (Attack, Skill, Power)
□ Validação de custos e efeitos
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Card:
    """Represents a playable card in the game.
    
    This is a pure data class with no pygame dependencies.
    All game logic should be handled by other systems.
    """
    
    name: str
    cost: int
    damage: int = 0
    block: int = 0
    heal: int = 0
    description: str = ""
    
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
            True if card has damage, block, or heal
        """
        return self.damage > 0 or self.block > 0 or self.heal > 0


# Predefined starter cards
STARTER_CARDS = [
    Card(name="Strike", cost=1, damage=6, description="Deal 6 damage."),
    Card(name="Defend", cost=1, block=5, description="Gain 5 Block."),
    Card(name="Bash", cost=2, damage=8, description="Deal 8 damage."),
]


def create_starter_deck() -> list[Card]:
    """Create the default starting deck.
    
    Returns:
        List of cards that make up the starter deck
    """
    deck = []
    
    # Add multiple copies of basic cards
    for _ in range(5):
        deck.append(Card(name="Strike", cost=1, damage=6, description="Deal 6 damage."))
    
    for _ in range(4):
        deck.append(Card(name="Defend", cost=1, block=5, description="Gain 5 Block."))
    
    # Add one bash
    deck.append(Card(name="Bash", cost=2, damage=8, description="Deal 8 damage."))
    
    return deck


def create_card_by_name(name: str) -> Optional[Card]:
    """Create a card instance by name.
    
    Args:
        name: Name of the card to create
        
    Returns:
        Card instance or None if name not found
    """
    card_registry = {
        "Strike": Card(name="Strike", cost=1, damage=6, description="Deal 6 damage."),
        "Defend": Card(name="Defend", cost=1, block=5, description="Gain 5 Block."),
        "Bash": Card(name="Bash", cost=2, damage=8, description="Deal 8 damage."),
        "Heal": Card(name="Heal", cost=1, heal=5, description="Heal 5 HP."),
        "Power Strike": Card(name="Power Strike", cost=2, damage=12, description="Deal 12 damage."),
        "Iron Wall": Card(name="Iron Wall", cost=2, block=12, description="Gain 12 Block."),
    }
    
    return card_registry.get(name)
