#!/usr/bin/env python3
"""
Test script for Sprint 1 - Basic functionality verification
"""

import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def test_pygame_init():
    """Test pygame initialization"""
    try:
        pygame.init()
        print("[OK] Pygame initialization successful")
        return True
    except Exception as e:
        print(f"[FAIL] Pygame initialization failed: {e}")
        return False

def test_display_creation():
    """Test display mode creation"""
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        print(f"[OK] Display created successfully: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        pygame.quit()
        return True
    except Exception as e:
        print(f"[FAIL] Display creation failed: {e}")
        return False

def test_config_import():
    """Test config module import"""
    try:
        from config import HEROES, AI_SEED, AI_IMAGE_SIZE
        print(f"[OK] Config imported - Heroes: {len(HEROES)}, AI Seed: {AI_SEED}")
        print(f"[OK] AI Image Size: {AI_IMAGE_SIZE}")
        return True
    except Exception as e:
        print(f"[FAIL] Config import failed: {e}")
        return False

def test_main_import():
    """Test main module import"""
    try:
        from main import MedievalDeck, GameState
        print("[OK] Main module imported successfully")
        print(f"[OK] Game states available: {[attr for attr in dir(GameState) if not attr.startswith('_')]}")
        return True
    except Exception as e:
        print(f"[FAIL] Main module import failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("MEDIEVAL DECK - SPRINT 1 TEST")
    print("=" * 50)
    
    tests = [
        test_config_import,
        test_main_import, 
        test_pygame_init,
        test_display_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"SPRINT 1 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] Sprint 1 complete - All systems operational!")
    else:
        print("[WARNING] Some tests failed - Review implementation")
    print("=" * 50)