#!/usr/bin/env python3
"""
Medieval Deck - Complete Asset Generation
Gera todos os assets necessários para o jogo completo
Otimizado para RTX 5070 com CUDA 12.8
"""

import os
import sys
import yaml
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.gen_assets import AssetGenerator

def load_prompts():
    """Load prompts from YAML file."""
    prompts_file = project_root / "prompts.yaml"
    with open(prompts_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def ensure_directories():
    """Ensure all asset directories exist."""
    dirs = [
        "assets/bg",
        "assets/ui", 
        "assets/sheets",
        "assets/.cache"
    ]
    for dir_path in dirs:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Directory ensured: {dir_path}")

def generate_all_backgrounds(ag, prompts):
    """Generate all background assets."""
    print("\n🏰 GENERATING BACKGROUNDS")
    print("=" * 50)
    
    backgrounds = prompts.get('backgrounds', {})
    bg_configs = [
        ("arena", (3440, 1440)),
        ("menu", (3440, 1440)), 
        ("card_selection", (3440, 1440)),
        ("deck_builder", (3440, 1440)),
        ("battle_prep", (3440, 1440))
    ]
    
    for i, (bg_name, size) in enumerate(bg_configs, 1):
        print(f"\n{i}/5 🖼️ Generating {bg_name} background...")
        prompt = backgrounds.get(bg_name, f"medieval {bg_name} scene")
        output_path = f"assets/bg/{bg_name}.png"
        print(f"Generating: '{prompt}' -> {output_path} ({size[0]}x{size[1]})")
        ag.generate_image(prompt, output_path, size)

def generate_all_ui_elements(ag, prompts):
    """Generate all UI elements."""
    print("\n🎨 GENERATING UI ELEMENTS")
    print("=" * 50)
    
    ui_elements = prompts.get('ui_elements', {})
    ui_configs = [
        ("card_frame", (512, 768)),
        ("button_frame", (256, 64)),
        ("health_bar", (400, 32)),
        ("mana_bar", (400, 32))
    ]
    
    for i, (ui_name, size) in enumerate(ui_configs, 1):
        print(f"\n{i}/4 🔲 Generating {ui_name}...")
        prompt = ui_elements.get(ui_name, f"medieval {ui_name}")
        output_path = f"assets/ui/{ui_name}.png"
        print(f"Generating: '{prompt}' -> {output_path} ({size[0]}x{size[1]})")
        ag.generate_image(prompt, output_path, size)

def generate_all_character_sheets(ag, prompts):
    """Generate all character sprite sheets."""
    print("\n⚔️ GENERATING CHARACTER SPRITES")
    print("=" * 50)
    
    character_sheets = prompts.get('character_sheets', {})
    sprite_configs = [
        ("knight_idle", (5120, 512), 10),
        ("knight_attack", (5120, 512), 10),
        ("goblin_idle", (4200, 424), 10),
        ("goblin_attack", (4200, 424), 10),
        ("mage_idle", (5120, 512), 10),
        ("mage_attack", (5120, 512), 10),
        ("archer_idle", (5120, 512), 10),
        ("archer_attack", (5120, 512), 10)
    ]
    
    for i, (char_name, size, frames) in enumerate(sprite_configs, 1):
        print(f"\n{i}/8 🧙 Generating {char_name} sprites...")
        base_prompt = character_sheets.get(char_name, f"medieval {char_name}")
        sprite_prompt = f"{base_prompt}, sprite sheet, {frames} frames, animation sequence"
        output_path = f"assets/sheets/{char_name}.png"
        print(f"Generating: '{sprite_prompt}' -> {output_path} ({size[0]}x{size[1]})")
        
        # Use specialized sprite sheet generation
        frame_width = size[0] // frames
        ag.generate_sprite_sheet(sprite_prompt, frames, output_path, height=size[1])

def main():
    """Main generation function."""
    parser = argparse.ArgumentParser(description="Generate all Medieval Deck assets")
    parser.add_argument("--skip-backgrounds", action="store_true", help="Skip background generation")
    parser.add_argument("--skip-ui", action="store_true", help="Skip UI elements")
    parser.add_argument("--skip-sprites", action="store_true", help="Skip character sprites")
    parser.add_argument("--assets-only", help="Generate only specific asset type (backgrounds/ui/sprites)")
    
    args = parser.parse_args()
    
    print("🏰 Medieval Deck - Complete Asset Generation")
    print("🎮 Optimized for RTX 5070 with CUDA 12.8")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories()
    
    # Load prompts
    prompts = load_prompts()
    print("✅ Prompts loaded from prompts.yaml")
    
    # Initialize asset generator
    ag = AssetGenerator(seed=42)
    print("✅ AssetGenerator initialized")
    
    if ag.pipeline is None:
        print("❌ SDXL pipeline not available - cannot generate real assets")
        return
    
    print("🚀 Starting complete asset generation...")
    print("⏳ This will take approximately 30-45 minutes...")
    
    # Generate assets based on arguments
    if args.assets_only:
        if args.assets_only == "backgrounds":
            generate_all_backgrounds(ag, prompts)
        elif args.assets_only == "ui":
            generate_all_ui_elements(ag, prompts)
        elif args.assets_only == "sprites":
            generate_all_character_sheets(ag, prompts)
        else:
            print(f"❌ Unknown asset type: {args.assets_only}")
            return
    else:
        # Generate all assets unless skipped
        if not args.skip_backgrounds:
            generate_all_backgrounds(ag, prompts)
        
        if not args.skip_ui:
            generate_all_ui_elements(ag, prompts)
            
        if not args.skip_sprites:
            generate_all_character_sheets(ag, prompts)
    
    print("\n" + "=" * 60)
    print("🎉 Complete asset generation finished!")
    print("📁 All assets saved in assets/ directory")
    print("✨ Ready for Medieval Deck development!")
    print("🎮 All artwork generated with Stable Diffusion XL on RTX 5070")

if __name__ == "__main__":
    main()
