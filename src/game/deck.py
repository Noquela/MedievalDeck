"""
TODO Sprint 02:
□ Deck class com draw pile, discard pile, hand
□ Sistema de draw com reshuffle automático
□ Testes de mecânicas de deck
"""

from typing import List
import random
from .cards import Card


class Deck:
    """Manages the player's deck of cards.
    
    Handles draw pile, discard pile, and hand management.
    No pygame dependencies - pure game logic.
    """
    
    def __init__(self, cards: List[Card]) -> None:
        """Initialize deck with given cards.
        
        Args:
            cards: List of cards that make up the deck
        """
        self.draw_pile = cards.copy()
        self.discard_pile: List[Card] = []
        self.hand: List[Card] = []
        self.max_hand_size = 10
        
        # Shuffle the initial deck
        self.shuffle()
    
    def shuffle(self) -> None:
        """Shuffle the draw pile."""
        random.shuffle(self.draw_pile)
    
    def draw(self, n: int = 1) -> List[Card]:
        """Draw cards from the draw pile to hand.
        
        Args:
            n: Number of cards to draw
            
        Returns:
            List of cards that were actually drawn
        """
        drawn_cards = []
        
        for _ in range(n):
            # Check if hand is full
            if len(self.hand) >= self.max_hand_size:
                break
            
            # If draw pile is empty, reshuffle discard pile
            if not self.draw_pile and self.discard_pile:
                self.draw_pile = self.discard_pile.copy()
                self.discard_pile.clear()
                self.shuffle()
            
            # Draw a card if available
            if self.draw_pile:
                card = self.draw_pile.pop()
                self.hand.append(card)
                drawn_cards.append(card)
        
        return drawn_cards
    
    def discard(self, card: Card) -> bool:
        """Discard a card from hand.
        
        Args:
            card: Card to discard
            
        Returns:
            True if card was discarded, False if not in hand
        """
        if card in self.hand:
            self.hand.remove(card)
            self.discard_pile.append(card)
            return True
        return False
    
    def discard_hand(self) -> None:
        """Discard all cards in hand."""
        self.discard_pile.extend(self.hand)
        self.hand.clear()
    
    def play_card(self, card: Card) -> bool:
        """Play a card from hand (removes it from hand, adds to discard).
        
        Args:
            card: Card to play
            
        Returns:
            True if card was played, False if not in hand
        """
        return self.discard(card)
    
    def add_card(self, card: Card) -> None:
        """Add a card to the deck (goes to discard pile).
        
        Args:
            card: Card to add to deck
        """
        self.discard_pile.append(card)
    
    def remove_card(self, card_name: str) -> bool:
        """Remove all copies of a card from the entire deck.
        
        Args:
            card_name: Name of card to remove
            
        Returns:
            True if any cards were removed
        """
        removed_any = False
        
        # Remove from hand
        self.hand = [c for c in self.hand if c.name != card_name]
        
        # Remove from draw pile
        original_draw_size = len(self.draw_pile)
        self.draw_pile = [c for c in self.draw_pile if c.name != card_name]
        if len(self.draw_pile) < original_draw_size:
            removed_any = True
        
        # Remove from discard pile
        original_discard_size = len(self.discard_pile)
        self.discard_pile = [c for c in self.discard_pile if c.name != card_name]
        if len(self.discard_pile) < original_discard_size:
            removed_any = True
        
        return removed_any
    
    def get_total_cards(self) -> int:
        """Get total number of cards in entire deck.
        
        Returns:
            Total cards in hand + draw pile + discard pile
        """
        return len(self.hand) + len(self.draw_pile) + len(self.discard_pile)
    
    def get_hand_size(self) -> int:
        """Get current hand size.
        
        Returns:
            Number of cards in hand
        """
        return len(self.hand)
    
    def get_draw_pile_size(self) -> int:
        """Get draw pile size.
        
        Returns:
            Number of cards in draw pile
        """
        return len(self.draw_pile)
    
    def is_empty(self) -> bool:
        """Check if deck is completely empty.
        
        Returns:
            True if no cards remain in any pile
        """
        return self.get_total_cards() == 0
