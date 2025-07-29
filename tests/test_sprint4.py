#!/usr/bin/env python3
"""
Test script for Sprint 4 - RTX 5070 optimization and hero sprite generation
"""

import pygame
import sys
import os
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCREEN_WIDTH, SCREEN_HEIGHT, HEROES
from gen_assets.rtx_optimizer import RTX5070Optimizer
from gen_assets.generate_backgrounds import AssetGenerator
from gen_assets.art_direction import ArtDirection

def test_rtx_optimizer_initialization():
    """Test RTX5070Optimizer system initialization"""
    try:
        optimizer = RTX5070Optimizer()
        
        # Test device detection
        if optimizer.device in ['cuda', 'cpu']:
            print(f"[OK] RTX Optimizer initialized - Device: {optimizer.device}")
        else:
            print(f"[FAIL] Invalid device detected: {optimizer.device}")
            return False
        
        # Test memory management setup
        if optimizer.memory_fraction > 0 and optimizer.memory_fraction <= 1:
            print(f"[OK] Memory fraction configured: {optimizer.memory_fraction}")
        else:
            print(f"[FAIL] Invalid memory fraction: {optimizer.memory_fraction}")
            return False
        
        # Test compilation mode
        if optimizer.compile_mode:
            print(f"[OK] Compile mode set: {optimizer.compile_mode}")
        else:
            print("[FAIL] Compile mode not set")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] RTX Optimizer initialization failed: {e}")
        return False

def test_memory_info_collection():
    """Test system memory information collection"""
    try:
        optimizer = RTX5070Optimizer()
        memory_info = optimizer.get_memory_info()
        
        required_keys = ['system_ram_gb', 'system_ram_used_gb']
        for key in required_keys:
            if key not in memory_info:
                print(f"[FAIL] Missing memory info key: {key}")
                return False
        
        print(f"[OK] System RAM: {memory_info['system_ram_used_gb']:.1f}/{memory_info['system_ram_gb']:.1f} GB")
        
        if optimizer.device == 'cuda':
            cuda_keys = ['vram_total_gb', 'vram_allocated_gb', 'vram_cached_gb']
            for key in cuda_keys:
                if key not in memory_info:
                    print(f"[FAIL] Missing CUDA memory info key: {key}")
                    return False
            
            print(f"[OK] GPU VRAM: {memory_info['vram_allocated_gb']:.1f}/{memory_info['vram_total_gb']:.1f} GB")
        
        return True
    except Exception as e:
        print(f"[FAIL] Memory info collection failed: {e}")
        return False

def test_optimal_generation_params():
    """Test optimal parameter generation for different resolutions"""
    try:
        optimizer = RTX5070Optimizer()
        
        # Test different resolutions
        test_resolutions = [
            (1024, 1024),      # Standard
            (3440, 1440),      # Ultrawide
            (512, 512),        # Small
            (2048, 2048)       # Large
        ]
        
        for width, height in test_resolutions:
            params = optimizer.get_optimal_generation_params((width, height))
            
            required_keys = ['num_inference_steps', 'guidance_scale', 'width', 'height']
            for key in required_keys:
                if key not in params:
                    print(f"[FAIL] Missing parameter key: {key}")
                    return False
            
            if params['width'] != width or params['height'] != height:
                print(f"[FAIL] Resolution mismatch: expected {width}x{height}, got {params['width']}x{params['height']}")
                return False
        
        print("[OK] Optimal generation parameters working for all resolutions")
        return True
    except Exception as e:
        print(f"[FAIL] Optimal generation params test failed: {e}")
        return False

def test_asset_generator_rtx_integration():
    """Test AssetGenerator with RTX optimization"""
    try:
        generator = AssetGenerator(use_mock=True)  # Use mock for testing
        
        # Test RTX optimizer integration
        if hasattr(generator, 'optimizer'):
            print("[OK] RTX optimizer integrated into AssetGenerator")
        else:
            print("[FAIL] RTX optimizer not integrated")
            return False
        
        # Test device consistency
        if generator.device == generator.optimizer.device:
            print(f"[OK] Device consistency: {generator.device}")
        else:
            print(f"[FAIL] Device inconsistency: generator={generator.device}, optimizer={generator.optimizer.device}")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] AssetGenerator RTX integration test failed: {e}")
        return False

def test_enhanced_background_generation():
    """Test enhanced background generation with post-processing"""
    try:
        generator = AssetGenerator(use_mock=True)
        
        # Generate background with enhancements
        bg_path = generator.generate_hero_background('knight')
        
        if bg_path and os.path.exists(bg_path):
            print(f"[OK] Enhanced background generated: {os.path.basename(bg_path)}")
        else:
            print("[FAIL] Enhanced background generation failed")
            return False
        
        # Test image enhancement method exists
        if hasattr(generator, '_enhance_image_quality'):
            print("[OK] Image enhancement method available")
        else:
            print("[FAIL] Image enhancement method missing")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] Enhanced background generation test failed: {e}")
        return False

def test_hero_sprite_generation():
    """Test hero sprite generation system"""
    try:
        generator = AssetGenerator(use_mock=True)
        
        # Test sprite generation for each hero
        heroes = ['knight', 'mage', 'assassin']
        
        for hero in heroes:
            sprite_path = generator.generate_hero_sprite(hero)
            
            if sprite_path and os.path.exists(sprite_path):
                print(f"[OK] Sprite generated for {hero}: {os.path.basename(sprite_path)}")
            else:
                print(f"[FAIL] Sprite generation failed for {hero}")
                return False
        
        # Test sprite processing method
        if hasattr(generator, '_process_sprite'):
            print("[OK] Sprite processing method available")
        else:
            print("[FAIL] Sprite processing method missing")
            return False
        
        # Test batch sprite generation
        sprites = generator.generate_all_hero_sprites()
        
        if len(sprites) == 3:
            print("[OK] Batch sprite generation working")
        else:
            print(f"[FAIL] Batch sprite generation incomplete: {len(sprites)}/3")
            return False
        
        return True
    except Exception as e:
        print(f"[FAIL] Hero sprite generation test failed: {e}")
        return False

def test_art_direction_sprite_prompts():
    """Test enhanced art direction for sprites"""
    try:
        # Test sprite prompts for all heroes
        heroes = ['knight', 'mage', 'assassin']
        
        for hero in heroes:
            prompt_config = ArtDirection.get_hero_sprite_prompt(hero)
            
            # Check required fields
            required_fields = ['positive', 'negative', 'width', 'height', 'seed', 'hero', 'character_desc']
            for field in required_fields:
                if field not in prompt_config:
                    print(f"[FAIL] Sprite prompt missing field {field} for {hero}")
                    return False
            
            # Check sprite-specific dimensions
            if prompt_config['width'] != 1024 or prompt_config['height'] != 1024:
                print(f"[FAIL] Wrong sprite dimensions for {hero}: {prompt_config['width']}x{prompt_config['height']}")
                return False
        
        print("[OK] Art direction sprite prompts working for all heroes")
        return True
    except Exception as e:
        print(f"[FAIL] Art direction sprite prompts test failed: {e}")
        return False

def test_performance_optimization_context():
    """Test performance optimization context manager"""
    try:
        optimizer = RTX5070Optimizer()
        
        # Test optimization context
        with optimizer.optimized_generation():
            # Simulate some work
            time.sleep(0.1)
        
        print("[OK] Performance optimization context working")
        return True
    except Exception as e:
        print(f"[FAIL] Performance optimization context test failed: {e}")
        return False

def test_system_info_display():
    """Test system information display"""
    try:
        optimizer = RTX5070Optimizer()
        
        # This should not crash
        optimizer.print_system_info()
        
        print("[OK] System information display working")
        return True
    except Exception as e:
        print(f"[FAIL] System info display test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("MEDIEVAL DECK - SPRINT 4 TEST")
    print("RTX 5070 Optimization + Hero Sprite Generation")
    print("=" * 80)
    
    tests = [
        test_rtx_optimizer_initialization,
        test_memory_info_collection,
        test_optimal_generation_params,
        test_asset_generator_rtx_integration,
        test_enhanced_background_generation,
        test_hero_sprite_generation,
        test_art_direction_sprite_prompts,
        test_performance_optimization_context,
        test_system_info_display
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
    
    print("=" * 80)
    print(f"SPRINT 4 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("[SUCCESS] Sprint 4 complete - RTX 5070 optimization system ready!")
        print("Features implemented:")
        print("- RTX 5070 specific optimizations (xFormers, torch.compile, etc.)")
        print("- Advanced memory management and VRAM optimization")
        print("- High-quality hero sprite generation")
        print("- Post-processing for enhanced image quality")
        print("- Performance benchmarking system")
        print("- Optimized generation parameters")
        print("- GPU memory monitoring and cleanup")
    else:
        print(f"[WARNING] {total - passed} tests failed - Review implementation")
    print("=" * 80)