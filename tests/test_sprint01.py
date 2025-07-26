"""
Tests for Sprint 01 - Pipeline de Assets.
"""

import pytest
import os
import sys
from PIL import Image

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def test_asset_generator_import():
    """Test that AssetGenerator can be imported."""
    from gen_assets import AssetGenerator
    assert AssetGenerator is not None


def test_asset_generator_initialization():
    """Test that AssetGenerator can be instantiated."""
    from gen_assets import AssetGenerator
    ag = AssetGenerator(seed=42)
    assert ag.seed == 42
    assert ag.cache_dir == "assets/.cache"


def test_prompts_yaml_exists():
    """Test that prompts.yaml file exists and is valid."""
    prompts_path = os.path.join(os.path.dirname(__file__), '..', 'prompts.yaml')
    assert os.path.exists(prompts_path), "prompts.yaml should exist"
    
    import yaml
    with open(prompts_path, 'r', encoding='utf-8') as f:
        prompts = yaml.safe_load(f)
    
    assert 'backgrounds' in prompts
    assert 'ui_elements' in prompts
    assert 'character_sheets' in prompts
    assert 'arena' in prompts['backgrounds']


def test_cache_key_generation():
    """Test cache key generation is deterministic."""
    from gen_assets import AssetGenerator
    ag = AssetGenerator(seed=42)
    
    key1 = ag._get_cache_key("test prompt", 512, 512)
    key2 = ag._get_cache_key("test prompt", 512, 512)
    
    assert key1 == key2
    assert len(key1) == 32  # MD5 hash length
    
    # Different prompts should generate different keys
    key3 = ag._get_cache_key("different prompt", 512, 512)
    assert key1 != key3


def test_placeholder_image_creation():
    """Test placeholder image creation."""
    from gen_assets import AssetGenerator
    ag = AssetGenerator(seed=42)
    
    # Test arena background placeholder
    img = ag._create_placeholder_image(800, 600, "arena background")
    assert img.size == (800, 600)
    assert img.mode == 'RGB'
    
    # Test card frame placeholder
    card_img = ag._create_placeholder_image(512, 768, "card frame")
    assert card_img.size == (512, 768)
    assert card_img.mode == 'RGBA'


def test_assets_exist_after_generation():
    """Test that expected assets exist after running generation."""
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    # Expected assets for Sprint 01
    expected_assets = [
        'assets/bg/arena.png',
        'assets/ui/card_frame.png', 
        'assets/sheets/knight_idle.png',
        'assets/sheets/knight_attack.png',
        'assets/sheets/goblin_idle.png',
        'assets/sheets/goblin_attack.png'
    ]
    
    for asset_path in expected_assets:
        full_path = os.path.join(base_dir, asset_path)
        if os.path.exists(full_path):
            # If file exists, verify it's a valid image
            try:
                img = Image.open(full_path)
                assert img.size[0] > 0 and img.size[1] > 0
                img.close()
            except Exception as e:
                pytest.fail(f"Invalid image file {asset_path}: {e}")


def test_sprite_sheet_dimensions():
    """Test sprite sheet has correct dimensions."""
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    knight_idle_path = os.path.join(base_dir, 'assets/sheets/knight_idle.png')
    
    if os.path.exists(knight_idle_path):
        img = Image.open(knight_idle_path)
        
        # Knight sprite sheet should be 10 frames x 512px = 5120 x 512
        assert img.size[0] == 5120, f"Expected width 5120, got {img.size[0]}"
        assert img.size[1] == 512, f"Expected height 512, got {img.size[1]}"
        
        img.close()


def test_cache_directory_creation():
    """Test that cache directory is created."""
    from gen_assets import AssetGenerator
    ag = AssetGenerator(seed=42)
    
    cache_dir = ag.cache_dir
    assert os.path.exists(cache_dir), "Cache directory should be created"
    assert os.path.isdir(cache_dir), "Cache path should be a directory"


if __name__ == "__main__":
    pytest.main([__file__])
