#!/usr/bin/env python3
"""
Test script for Sprint 3 - Hero selection and AI background generation
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCREEN_WIDTH, SCREEN_HEIGHT, HEROES, BACKGROUNDS_DIR
from gen_assets.art_direction import ArtDirection
from gen_assets.generate_backgrounds import AssetGenerator
from screens.selection import SelectionScreen
from main import MedievalDeck, GameState

def test_art_direction_system():
    """Test art direction prompt generation"""
    try:
        # Test hero background prompts
        for hero in ['knight', 'mage', 'assassin']:
            prompt_config = ArtDirection.get_hero_background_prompt(hero)
            
            required_keys = ['positive', 'negative', 'width', 'height', 'seed', 'hero']
            for key in required_keys:
                if key not in prompt_config:
                    print(f"[FAIL] Missing key {key} in {hero} prompt config")
                    return False
                    
            print(f"[OK] Art direction for {hero}: {len(prompt_config['positive'])} chars")
            
        # Test sprite prompts
        sprite_config = ArtDirection.get_hero_sprite_prompt('knight')
        if 'character_desc' in sprite_config:
            print("[OK] Hero sprite prompts working")
        else:
            print("[FAIL] Hero sprite prompts missing description")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Art direction test failed: {e}")
        return False

def test_asset_generator_initialization():
    """Test AssetGenerator initialization"""
    try:
        generator = AssetGenerator()
        
        # Check if directories were created
        required_dirs = [BACKGROUNDS_DIR, "gen_assets/heroes", "gen_assets/ui", "gen_assets/cards"]
        for directory in required_dirs:
            if not os.path.exists(directory):
                print(f"[FAIL] Directory not created: {directory}")
                return False
                
        print("[OK] AssetGenerator initialized and directories created")
        
        # Test device detection
        if generator.device in ['cuda', 'cpu']:
            print(f"[OK] Device detected: {generator.device}")
        else:
            print(f"[FAIL] Invalid device: {generator.device}")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] AssetGenerator initialization failed: {e}")
        return False

def test_background_generation():
    """Test background generation (mock mode)"""
    try:
        generator = AssetGenerator(use_mock=True)
        
        # Test single hero background
        bg_path = generator.generate_hero_background('knight')
        
        if bg_path and os.path.exists(bg_path):
            print(f"[OK] Knight background generated: {os.path.basename(bg_path)}")
        else:
            print("[FAIL] Knight background generation failed")
            return False
            
        # Test cache functionality
        bg_path2 = generator.generate_hero_background('knight')
        if bg_path == bg_path2:
            print("[OK] Background caching working")
        else:
            print("[FAIL] Background caching not working")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Background generation test failed: {e}")
        return False

def test_selection_screen_creation():
    """Test SelectionScreen initialization"""
    try:
        pygame.init()
        
        class MockGame:
            def __init__(self):
                self.running = True
                self.selected_hero = None
                
        mock_game = MockGame()
        selection = SelectionScreen(mock_game)
        
        # Test hero positions calculated correctly
        if len(selection.hero_positions) == 3:
            print("[OK] Hero positions calculated for all 3 heroes")
        else:
            print(f"[FAIL] Wrong number of hero positions: {len(selection.hero_positions)}")
            return False
            
        # Test hero buttons created
        if len(selection.hero_buttons) == 3:
            print("[OK] Hero buttons created")
        else:
            print(f"[FAIL] Wrong number of hero buttons: {len(selection.hero_buttons)}")
            return False
            
        # Test confirm and back buttons
        if selection.confirm_button and selection.back_button:
            print("[OK] Confirm and back buttons created")
        else:
            print("[FAIL] Missing confirm or back buttons")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] SelectionScreen creation failed: {e}")
        return False
    finally:
        pygame.quit()

def test_hero_selection_logic():
    """Test hero selection and state changes"""
    try:
        pygame.init()
        pygame.display.set_mode((100, 100))  # Minimal display
        
        class MockGame:
            def __init__(self):
                self.running = True
                self.selected_hero = None
                
        mock_game = MockGame()
        selection = SelectionScreen(mock_game)
        
        # Test hero selection
        selection._select_hero('mage')
        
        if selection.selected_hero == 'mage':
            print("[OK] Hero selection working")
        else:
            print(f"[FAIL] Hero selection failed: {selection.selected_hero}")
            return False
            
        # Test selection change
        selection._select_hero('assassin')
        
        if selection.selected_hero == 'assassin':
            print("[OK] Hero selection change working")
        else:
            print("[FAIL] Hero selection change failed")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Hero selection logic test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_main_game_integration():
    """Test main game integration with selection screen"""
    try:
        pygame.init()
        pygame.display.set_mode((100, 100))  # Minimal display
        
        game = MedievalDeck()
        
        # Test selection screen registered
        if GameState.SELECTION in game.screens:
            print("[OK] Selection screen registered in main game")
        else:
            print("[FAIL] Selection screen not registered")
            return False
            
        # Test state transition capability
        game.change_state(GameState.SELECTION)
        
        if game.current_state == GameState.SELECTION:
            print("[OK] State transition to selection working")
        else:
            print(f"[FAIL] State transition failed: {game.current_state}")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Main game integration test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_hero_data_consistency():
    """Test hero data consistency with config"""
    try:
        # Test all heroes exist in config
        required_heroes = ['knight', 'mage', 'assassin']
        
        for hero in required_heroes:
            if hero not in HEROES:
                print(f"[FAIL] Hero {hero} not found in config")
                return False
                
            hero_data = HEROES[hero]
            required_fields = ['name', 'health', 'mana', 'description']
            
            for field in required_fields:
                if field not in hero_data:
                    print(f"[FAIL] Hero {hero} missing field {field}")
                    return False
                    
        print("[OK] All hero data consistent")
        
        # Test ultrawide resolution settings
        if SCREEN_WIDTH == 3440 and SCREEN_HEIGHT == 1440:
            print("[OK] Ultrawide resolution maintained")
        else:
            print(f"[FAIL] Wrong resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Hero data consistency test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("MEDIEVAL DECK - SPRINT 3 TEST")
    print("Hero Selection + AI Background Generation")
    print("=" * 70)
    
    tests = [
        test_hero_data_consistency,
        test_art_direction_system,
        test_asset_generator_initialization,
        test_background_generation,
        test_selection_screen_creation,
        test_hero_selection_logic,
        test_main_game_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"[ERROR] Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 70)
    print(f"SPRINT 3 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] Sprint 3 complete - Hero selection with AI backgrounds!")
        print("Features implemented:")
        print("- Hero selection screen with 3 heroes")
        print("- AI background generation with SDXL")
        print("- Gothic medieval art direction system")
        print("- Dynamic background loading per hero")
        print("- Complete navigation: Menu -> Selection -> (Combat)")
        print("- Ultrawide optimization maintained")
    else:
        print(f"[WARNING] {total - passed} tests failed - Review implementation")
    print("=" * 70)