#!/usr/bin/env python3
"""
Test script for Sprint 2 - Menu system and button functionality
"""

import pygame
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.buttons import Button, MenuButtonSet
from screens.menu import MenuScreen
from main import MedievalDeck, GameState

def test_button_creation():
    """Test button component creation"""
    try:
        pygame.init()
        font = pygame.font.Font(None, 50)
        button = Button(100, 100, 200, 50, "Test Button", font)
        
        print("[OK] Button created successfully")
        print(f"[OK] Button rect: {button.rect}")
        print(f"[OK] Button text: {button.text}")
        return True
    except Exception as e:
        print(f"[FAIL] Button creation failed: {e}")
        return False
    finally:
        pygame.quit()

def test_menu_button_set():
    """Test MenuButtonSet functionality"""
    try:
        pygame.init()
        font = pygame.font.Font(None, 50)
        button_set = MenuButtonSet(SCREEN_WIDTH, SCREEN_HEIGHT, font)
        
        # Add test buttons
        button_set.add_button("Test 1")
        button_set.add_button("Test 2")
        button_set.add_button("Test 3")
        
        print(f"[OK] MenuButtonSet created with {len(button_set.buttons)} buttons")
        
        # Test button retrieval
        button = button_set.get_button_by_text("Test 1")
        if button:
            print("[OK] Button retrieval working")
        else:
            print("[FAIL] Button retrieval failed")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] MenuButtonSet test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_menu_screen_creation():
    """Test MenuScreen initialization"""
    try:
        pygame.init()
        
        # Create a mock game instance
        class MockGame:
            def __init__(self):
                self.running = True
                
        mock_game = MockGame()
        menu = MenuScreen(mock_game)
        
        print("[OK] MenuScreen created successfully")
        print(f"[OK] Menu has {len(menu.button_set.buttons)} buttons")
        return True
    except Exception as e:
        print(f"[FAIL] MenuScreen creation failed: {e}")
        return False
    finally:
        pygame.quit()

def test_main_game_integration():
    """Test main game class with menu integration"""
    try:
        pygame.init()
        pygame.display.set_mode((100, 100))  # Minimal display for testing
        
        game = MedievalDeck()
        
        # Test initial state
        if game.current_state == GameState.MENU:
            print("[OK] Game starts in MENU state")
        else:
            print(f"[FAIL] Game starts in wrong state: {game.current_state}")
            return False
            
        # Test screen dictionary
        if GameState.MENU in game.screens:
            print("[OK] Menu screen registered in game")
        else:
            print("[FAIL] Menu screen not registered")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Main game integration test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_screen_rendering():
    """Test screen rendering functionality"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        class MockGame:
            def __init__(self):
                self.running = True
                
        mock_game = MockGame()
        menu = MenuScreen(mock_game)
        
        # Test rendering without crashing
        menu.render(screen)
        print("[OK] Menu screen renders without errors")
        
        return True
    except Exception as e:
        print(f"[FAIL] Screen rendering test failed: {e}")
        return False
    finally:
        pygame.quit()

def test_ultrawide_optimization():
    """Test ultrawide resolution support"""
    try:
        from config import SCREEN_WIDTH, SCREEN_HEIGHT, AI_IMAGE_SIZE
        
        if SCREEN_WIDTH == 3440 and SCREEN_HEIGHT == 1440:
            print("[OK] Ultrawide resolution configured correctly")
        else:
            print(f"[FAIL] Wrong resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
            return False
            
        if AI_IMAGE_SIZE == (3440, 1440):
            print("[OK] AI image size matches ultrawide resolution")
        else:
            print(f"[FAIL] AI image size mismatch: {AI_IMAGE_SIZE}")
            return False
            
        return True
    except Exception as e:
        print(f"[FAIL] Ultrawide optimization test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MEDIEVAL DECK - SPRINT 2 TEST")
    print("Menu System and Button Functionality")
    print("=" * 60)
    
    tests = [
        test_ultrawide_optimization,
        test_button_creation,
        test_menu_button_set,
        test_menu_screen_creation,
        test_main_game_integration,
        test_screen_rendering
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
    
    print("=" * 60)
    print(f"SPRINT 2 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] Sprint 2 complete - Menu system operational!")
        print("Features implemented:")
        print("- Interactive button system")
        print("- Menu screen with navigation")
        print("- Ultrawide-optimized UI")
        print("- Modular screen architecture")
    else:
        print(f"[WARNING] {total - passed} tests failed - Review implementation")
    print("=" * 60)