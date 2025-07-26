"""Tests for Sprint 02 - UI & Game Flow."""

import pytest
import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ui.screen_manager import ScreenManager
from ui.menu_screen import MenuScreen
from ui.character_select_screen import CharacterSelectScreen
from ui.combat_screen import CombatScreen


class TestSprint02:
    """Test suite for Sprint 02 features."""
    
    @classmethod
    def setup_class(cls):
        """Setup pygame for testing."""
        pygame.init()
        pygame.display.set_mode((100, 100))  # Small window for testing
    
    @classmethod
    def teardown_class(cls):
        """Cleanup pygame after testing."""
        pygame.quit()
    
    def test_screen_manager_creation(self):
        """Test that ScreenManager can be created."""
        manager = ScreenManager()
        assert manager is not None
        assert manager.is_empty()
    
    def test_screen_manager_push_pop(self):
        """Test basic screen stack operations."""
        manager = ScreenManager()
        menu_screen = MenuScreen(manager)
        
        # Test push
        manager.push(menu_screen)
        assert not manager.is_empty()
        assert manager.current() == menu_screen
        
        # Test multiple screens
        char_screen = CharacterSelectScreen(manager)
        manager.push(char_screen)
        assert manager.current() == char_screen
        
        # Test pop
        manager.pop()
        assert manager.current() == menu_screen
    
    def test_menu_screen_creation(self):
        """Test that MenuScreen creates properly."""
        manager = ScreenManager()
        menu_screen = MenuScreen(manager)
        
        assert menu_screen is not None
        assert hasattr(menu_screen, 'play_button_rect')
        assert menu_screen.screen_manager == manager
    
    def test_character_select_screen_creation(self):
        """Test that CharacterSelectScreen creates and has character options."""
        manager = ScreenManager()
        char_screen = CharacterSelectScreen(manager)
        
        assert char_screen is not None
        assert hasattr(char_screen, 'characters')
        assert len(char_screen.characters) >= 1  # At least one character
        assert char_screen.characters[0]['name'] == 'Knight'
        assert char_screen.selected_character == 0
    
    def test_combat_screen_creation(self):
        """Test that CombatScreen creates with character data."""
        manager = ScreenManager()
        selected_char = {"name": "Knight", "sprite_path": "assets/sheets/knight_idle.png"}
        combat_screen = CombatScreen(manager, selected_char)
        
        assert combat_screen is not None
        assert combat_screen.selected_character == selected_char
        assert hasattr(combat_screen, 'combat_engine')
        assert combat_screen.combat_engine.player.hp == 70  # Knight default HP
        assert combat_screen.combat_engine.enemy.hp > 0  # Enemy has health
    
    def test_screen_navigation_flow(self):
        """Test complete navigation flow: Menu → Character Select → Combat."""
        manager = ScreenManager()
        
        # Start with menu
        menu_screen = MenuScreen(manager)
        manager.push(menu_screen)
        assert manager.current() == menu_screen
        
        # Navigate to character selection
        char_screen = CharacterSelectScreen(manager)
        manager.push(char_screen)
        assert manager.current() == char_screen
        
        # Navigate to combat
        selected_char = char_screen.characters[0]  # Select first character
        combat_screen = CombatScreen(manager, selected_char)
        manager.push(combat_screen)
        assert manager.current() == combat_screen
        
        # Navigate back
        manager.pop()  # Back to character select
        assert manager.current() == char_screen
        
        manager.pop()  # Back to menu
        assert manager.current() == menu_screen
    
    def test_combat_screen_loads_arena_background(self):
        """Test that CombatScreen attempts to load arena background."""
        manager = ScreenManager()
        selected_char = {"name": "Knight", "sprite_path": None}
        combat_screen = CombatScreen(manager, selected_char)
        
        # Background should be loaded or None (if file doesn't exist)
        assert hasattr(combat_screen, 'background')
        # The background may be None if assets aren't available during testing
        # but the attribute should exist
    
    def test_fade_transition_system(self):
        """Test that screens support fade transitions."""
        manager = ScreenManager()
        menu_screen = MenuScreen(manager)
        
        # Test fade initialization
        menu_screen.start_fade_in()
        assert menu_screen.fade_alpha > 0
        assert menu_screen.fade_start_time > 0
        
        # Test fade update (should decrease alpha over time)
        initial_alpha = menu_screen.fade_alpha
        menu_screen.update_fade()
        # Alpha should be decreasing (or stay the same if time hasn't passed)
        assert menu_screen.fade_alpha <= initial_alpha


if __name__ == "__main__":
    pytest.main([__file__])
