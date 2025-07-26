"""
Basic tests for Sprint 00 - Foundations.
"""

import pytest
import pygame
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def test_pygame_initialization():
    """Test that pygame can be initialized."""
    pygame.init()
    assert pygame.get_init()
    pygame.quit()


def test_main_import():
    """Test that main module can be imported."""
    from main import Game
    assert Game is not None


def test_game_initialization():
    """Test that Game class can be instantiated."""
    os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Headless mode
    pygame.init()
    
    from main import Game
    game = Game()
    
    assert game.screen_width == 3440
    assert game.screen_height == 1440
    assert game.target_fps == 60
    assert game.running == True
    
    pygame.quit()


def test_assets_directory_exists():
    """Test that assets directory structure exists."""
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    assert os.path.exists(os.path.join(base_dir, 'assets'))
    assert os.path.exists(os.path.join(base_dir, 'assets', 'bg'))
    assert os.path.exists(os.path.join(base_dir, 'assets', 'sheets'))
    assert os.path.exists(os.path.join(base_dir, 'assets', 'ui'))


def test_scripts_directory_exists():
    """Test that scripts directory exists."""
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    assert os.path.exists(os.path.join(base_dir, 'scripts'))
    assert os.path.exists(os.path.join(base_dir, 'scripts', 'gen_assets.py'))


if __name__ == "__main__":
    pytest.main([__file__])
