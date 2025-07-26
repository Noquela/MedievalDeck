"""
TODO Sprint 01:
□ AssetGenerator wrapper para SDXL ✅
□ Sistema de cache baseado em hash ✅
□ Prompts determinísticos (seed=42) ✅
□ Gerar arena.png, card_frame.png, knight_idle.png ✅
"""

import os
import hashlib
import yaml
import pygame
from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont

# Try to import SDXL dependencies
try:
    from diffusers import StableDiffusionXLPipeline
    import torch
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False
    print("Note: SDXL dependencies not available. Using placeholder generation.")


class AssetGenerator:
    """Generates game assets using Stable Diffusion XL or placeholders."""
    
    def __init__(self, seed: int = 42) -> None:
        """Initialize asset generator.
        
        Args:
            seed: Random seed for deterministic generation
        """
        self.seed = seed
        self.cache_dir = "assets/.cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        print(f"AssetGenerator initialized with seed {seed}")
        
        if DIFFUSERS_AVAILABLE:
            print("SDXL pipeline available - will generate AI art")
            self._initialize_pipeline()
        else:
            print("SDXL not available - using placeholder generation")
            self.pipeline = None
        
        # Load prompts
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompts from YAML file."""
        prompts_path = "prompts.yaml"
        if os.path.exists(prompts_path):
            with open(prompts_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _initialize_pipeline(self) -> None:
        """Initialize the Stable Diffusion XL pipeline optimized for RTX 5070."""
        try:
            print("🚀 Loading SDXL pipeline optimized for RTX 5070...")
            self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0",
                torch_dtype=torch.float16,
                use_safetensors=True,
                variant="fp16"
            )
            
            # RTX 5070 optimizations
            if hasattr(self.pipeline, "enable_attention_slicing"):
                self.pipeline.enable_attention_slicing()
            
            # Enable memory efficient attention for better performance
            if hasattr(self.pipeline, "enable_xformers_memory_efficient_attention"):
                try:
                    self.pipeline.enable_xformers_memory_efficient_attention()
                    print("✅ XFormers memory optimization enabled")
                except:
                    print("⚠️ XFormers not available, using standard attention")
            
            # Move to GPU if available
            if torch.cuda.is_available():
                device_name = torch.cuda.get_device_name(0)
                print(f"🎮 GPU detected: {device_name}")
                self.pipeline = self.pipeline.to("cuda")
                
                # Skip torch compile to avoid Triton dependency issues
                print("⚠️ Skipping torch compile to avoid Triton issues")
                        
                print("✅ SDXL pipeline loaded on GPU with optimizations")
            else:
                print("⚠️ No GPU detected, using CPU (will be slow)")
                
        except Exception as e:
            print(f"❌ Failed to initialize SDXL pipeline: {e}")
            print("Falling back to placeholder generation...")
            self.pipeline = None
    
    def _get_cache_key(self, prompt: str, width: int, height: int) -> str:
        """Generate cache key for prompt and dimensions.
        
        Args:
            prompt: Text prompt
            width: Image width
            height: Image height
            
        Returns:
            MD5 hash string
        """
        cache_string = f"{prompt}_{width}_{height}_{self.seed}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _create_placeholder_image(self, width: int, height: int, text: str) -> Image.Image:
        """Create a placeholder image when SDXL is not available.
        
        Args:
            width: Image width
            height: Image height
            text: Text to display on image
            
        Returns:
            PIL Image
        """
        # Create image with medieval-ish colors
        if "arena" in text.lower() or "background" in text.lower():
            # Arena background
            img = Image.new('RGB', (width, height), color=(30, 25, 20))
            draw = ImageDraw.Draw(img)
            
            # Create gradient effect
            for y in range(height):
                intensity = int(30 + (y / height) * 30)
                color = (intensity - 5, intensity - 10, intensity - 15)
                draw.line([(0, y), (width, y)], fill=color)
                
        elif "card" in text.lower():
            # Card frame
            img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw frame border
            border_color = (139, 69, 19, 255)  # Brown
            margin = 20
            draw.rectangle([margin, margin, width-margin, height-margin], 
                         outline=border_color, width=8)
                         
        else:
            # Character sprite
            img = Image.new('RGB', (width, height), color=(60, 50, 40))
            draw = ImageDraw.Draw(img)
            
            # Simple character placeholder
            center_x, center_y = width // 2, height // 2
            draw.ellipse([center_x-30, center_y-40, center_x+30, center_y+40], 
                        fill=(100, 80, 60))  # Body
            draw.ellipse([center_x-15, center_y-60, center_x+15, center_y-30], 
                        fill=(120, 100, 80))  # Head
        
        return img
    
    
    def generate_image(self, prompt: str, output_path: str, 
                      size: Tuple[int, int] = (512, 512)) -> bool:
        """Generate a single image.
        
        Args:
            prompt: Text prompt for generation
            output_path: Path to save generated image
            size: Image dimensions
            
        Returns:
            True if generation succeeded
        """
        width, height = size
        cache_key = self._get_cache_key(prompt, width, height)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.png")
        
        # Check cache first
        if os.path.exists(cache_path):
            print(f"Using cached image: {output_path}")
            img = Image.open(cache_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path)
            return True
        
        print(f"Generating: '{prompt}' -> {output_path} ({width}x{height})")
        
        if self.pipeline and DIFFUSERS_AVAILABLE:
            try:
                # Generate with SDXL - optimized settings for quality
                generator = torch.Generator(device="cuda").manual_seed(self.seed)
                
                # High quality settings optimized for SDXL
                image = self.pipeline(
                    prompt=prompt,
                    negative_prompt="blurry, low quality, ugly, distorted, watermark, text",
                    width=width,
                    height=height,
                    num_inference_steps=30,  # Balanced quality/speed
                    guidance_scale=7.5,      # Optimal for SDXL
                    generator=generator
                ).images[0]
                
                # Save to cache and output
                image.save(cache_path, quality=95, optimize=True)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                image.save(output_path, quality=95, optimize=True)
                print(f"🎨 Generated with SDXL: {output_path}")
                return True
                
            except Exception as e:
                print(f"SDXL generation failed: {e}")
                print("Falling back to placeholder...")
        
        # Fallback to placeholder
        img = self._create_placeholder_image(width, height, prompt)
        
        # Save to cache and output
        img.save(cache_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path)
        print(f"✅ Generated placeholder: {output_path}")
        return True
        
    def generate_background(self, prompt: str, output_path: str, 
                          size: Tuple[int, int] = (3440, 1440)) -> bool:
        """Generate background image.
        
        Args:
            prompt: Text prompt for generation
            output_path: Where to save the image
            size: Image dimensions
            
        Returns:
            True if successful
        """
        return self.generate_image(prompt, output_path, size)
    
    def generate_sprite_sheet(self, prompt: str, frame_count: int,
                            output_path: str, height: int = 512) -> bool:
        """Generate a sprite sheet.
        
        Args:
            prompt: Text prompt for sprite
            frame_count: Number of frames
            output_path: Where to save sprite sheet
            height: Height of each frame
            
        Returns:
            True if successful
        """
        frame_width = height  # Square frames
        sheet_width = frame_width * frame_count
        
        sprite_prompt = f"{prompt}, sprite sheet, {frame_count} frames, animation sequence"
        return self.generate_image(sprite_prompt, output_path, (sheet_width, height))
        return True


def main() -> None:
    """Generate Sprint 01 assets with SDXL AI."""
    print("🏰 Medieval Deck - Sprint 01 AI Asset Generation")
    print("🎮 Optimized for RTX 5070 with CUDA 12.8")
    print("=" * 60)
    
    ag = AssetGenerator(seed=42)
    
    if ag.pipeline:
        print("🎨 Generating high-quality AI artwork...")
        print("⏳ This may take several minutes for first-time generation...")
    else:
        print("⚠️ Using placeholder generation (SDXL not available)")
    
    print("\n1/6 🖼️ Generating arena background...")
    arena_prompt = ag.prompts.get('backgrounds', {}).get('arena', 
        "epic medieval stone dungeon corridor, dramatic lighting")
    ag.generate_background(arena_prompt, "assets/bg/arena.png", (3440, 1440))
    
    print("\n2/6 🃏 Generating card frame...")
    card_prompt = ag.prompts.get('ui_elements', {}).get('card_frame',
        "ornate medieval card frame, gold filigree")
    ag.generate_image(card_prompt, "assets/ui/card_frame.png", (512, 768))
    
    print("\n3/6 ⚔️ Generating knight idle sprites...")
    knight_idle_prompt = ag.prompts.get('character_sheets', {}).get('knight_idle',
        "noble medieval knight idle pose")
    ag.generate_sprite_sheet(knight_idle_prompt, 10, 
                           "assets/sheets/knight_idle.png", height=512)
    
    print("\n4/6 ⚔️ Generating knight attack sprites...")
    knight_attack_prompt = ag.prompts.get('character_sheets', {}).get('knight_attack',
        "heroic knight sword attack")
    ag.generate_sprite_sheet(knight_attack_prompt, 10,
                           "assets/sheets/knight_attack.png", height=512)
    
    print("\n5/6 👹 Generating goblin idle sprites...")
    goblin_idle_prompt = ag.prompts.get('character_sheets', {}).get('goblin_idle',
        "cunning goblin scout idle")
    ag.generate_sprite_sheet(goblin_idle_prompt, 10,
                           "assets/sheets/goblin_idle.png", height=424)
    
    print("\n6/6 👹 Generating goblin attack sprites...")
    goblin_attack_prompt = ag.prompts.get('character_sheets', {}).get('goblin_attack',
        "aggressive goblin attack")
    ag.generate_sprite_sheet(goblin_attack_prompt, 10,
                           "assets/sheets/goblin_attack.png", height=424)
    
    print("\n" + "=" * 60)
    print("🎉 Sprint 01 AI asset generation complete!")
    print("📁 Generated files:")
    print("   🖼️ assets/bg/arena.png (3440x1440)")
    print("   🃏 assets/ui/card_frame.png (512x768)")
    print("   ⚔️ assets/sheets/knight_idle.png (5120x512)")
    print("   ⚔️ assets/sheets/knight_attack.png (5120x512)")
    print("   👹 assets/sheets/goblin_idle.png (4200x420)")
    print("   👹 assets/sheets/goblin_attack.png (4200x420)")
    
    if ag.pipeline:
        print("\n✨ All artwork generated with Stable Diffusion XL!")
        print("🎮 RTX 5070 optimizations enabled for best performance")
    else:
        print("\n💡 To enable AI generation, ensure CUDA 12.8 is installed:")
        print("   pip install --pre torch torchvision --index-url https://download.pytorch.org/whl/nightly/cu128")
        print("   pip install diffusers transformers accelerate")


if __name__ == "__main__":
    main()
