"""
TODO Sprint 05:
□ Enemy class com HP e intents
□ Sistema de Intent enum
□ Geração procedural de intents
"""

from enum import Enum
from typing import List, Tuple, Optional
import random


class IntentType(Enum):
    """Types of enemy intents."""
    ATTACK = "attack"
    DEFEND = "defend"
    BUFF = "buff"
    DEBUFF = "debuff"
    HEAL = "heal"


class Intent:
    """Represents an enemy's planned action."""
    
    def __init__(self, intent_type: IntentType, value: int, description: str = "") -> None:
        """Initialize intent.
        
        Args:
            intent_type: Type of intent
            value: Numerical value (damage, block, etc.)
            description: Human readable description
        """
        self.type = intent_type
        self.value = value
        self.description = description or self._generate_description()
    
    def _generate_description(self) -> str:
        """Generate description based on intent type and value."""
        if self.type == IntentType.ATTACK:
            return f"Attack for {self.value} damage"
        elif self.type == IntentType.DEFEND:
            return f"Gain {self.value} block"
        elif self.type == IntentType.BUFF:
            return f"Buff (+{self.value})"
        elif self.type == IntentType.DEBUFF:
            return f"Debuff (-{self.value})"
        elif self.type == IntentType.HEAL:
            return f"Heal {self.value} HP"
        return "Unknown intent"


class Enemy:
    """Represents an enemy in combat."""
    
    def __init__(self, name: str, hp: int, intents: List[Tuple[IntentType, int]]) -> None:
        """Initialize enemy.
        
        Args:
            name: Enemy name
            hp: Starting hit points
            intents: List of possible intents as (type, value) tuples
        """
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.block = 0
        self.intent_pool = intents
        self.current_intent: Optional[Intent] = None
        self.turn_count = 0
        
        # Generate first intent
        self.generate_next_intent()
    
    def generate_next_intent(self) -> None:
        """Generate the next intent for this enemy."""
        if not self.intent_pool:
            return
        
        intent_type, value = random.choice(self.intent_pool)
        self.current_intent = Intent(intent_type, value)
        self.turn_count += 1
    
    def take_damage(self, damage: int) -> int:
        """Apply damage to enemy, accounting for block.
        
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
        """Add block to enemy.
        
        Args:
            block_amount: Amount of block to add
        """
        if block_amount > 0:
            self.block += block_amount
    
    def heal(self, heal_amount: int) -> int:
        """Heal the enemy.
        
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
    
    def execute_intent(self) -> Tuple[IntentType, int]:
        """Execute current intent and generate next one.
        
        Returns:
            Tuple of (intent_type, value) that was executed
        """
        if not self.current_intent:
            return IntentType.ATTACK, 0
        
        executed_type = self.current_intent.type
        executed_value = self.current_intent.value
        
        # Generate next intent for next turn
        self.generate_next_intent()
        
        return executed_type, executed_value
    
    def start_turn(self) -> None:
        """Called at start of enemy turn."""
        # Block expires at start of turn
        self.block = 0
    
    def is_dead(self) -> bool:
        """Check if enemy is dead.
        
        Returns:
            True if HP <= 0
        """
        return self.hp <= 0
    
    def get_hp_ratio(self) -> float:
        """Get HP as ratio of max HP.
        
        Returns:
            Current HP / Max HP as float between 0 and 1
        """
        if self.max_hp <= 0:
            return 0.0
        return self.hp / self.max_hp


# Predefined enemies
def create_goblin() -> Enemy:
    """Create a goblin enemy."""
    intents = [
        (IntentType.ATTACK, 5),
        (IntentType.ATTACK, 7),
        (IntentType.DEFEND, 4),
    ]
    return Enemy("Goblin Scout", hp=15, intents=intents)


def create_skeleton() -> Enemy:
    """Create a skeleton enemy."""
    intents = [
        (IntentType.ATTACK, 6),
        (IntentType.ATTACK, 8),
        (IntentType.BUFF, 2),
    ]
    return Enemy("Skeleton Warrior", hp=22, intents=intents)


def create_orc() -> Enemy:
    """Create an orc enemy."""
    intents = [
        (IntentType.ATTACK, 10),
        (IntentType.ATTACK, 12),
        (IntentType.DEFEND, 6),
        (IntentType.HEAL, 8),
    ]
    return Enemy("Orc Brute", hp=35, intents=intents)


def create_dark_wizard() -> Enemy:
    """Create a dark wizard mini-boss."""
    intents = [
        (IntentType.ATTACK, 8),
        (IntentType.DEFEND, 6),
        (IntentType.DEBUFF, 2),
        (IntentType.BUFF, 3),
    ]
    return Enemy("Dark Wizard", hp=60, intents=intents)


def create_dragon() -> Enemy:
    """Create the dragon boss."""
    intents = [
        (IntentType.ATTACK, 14),
        (IntentType.ATTACK, 20),  # Multi-hit represented as higher damage
        (IntentType.BUFF, 3),
        (IntentType.HEAL, 10),
    ]
    return Enemy("Ancient Dragon", hp=120, intents=intents)
