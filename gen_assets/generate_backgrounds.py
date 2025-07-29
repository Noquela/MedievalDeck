"""
AI Asset Generator for Medieval Deck
Sprint 3 Implementation: Hero backgrounds with SDXL
Following art direction for gothic medieval realism
"""

import os
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image
import hashlib
from config import AI_SEED, AI_IMAGE_SIZE, BACKGROUNDS_DIR
from .art_direction import ArtDirection

class AssetGenerator:
    """
    SDXL-based asset generator following Medieval Deck art direction
    Optimized for RTX 5070 with consistent styling
    """
    
    def __init__(self, use_mock=False):
        """Initialize SDXL pipeline with optimal settings"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = None
        self.cache_dir = "gen_assets"
        self.use_mock = use_mock
        
        print(f"AssetGenerator initialized - Device: {self.device}")
        print("Sprint 3: AI background generation with gothic medieval style")
        
        # Ensure directories exist
        os.makedirs(BACKGROUNDS_DIR, exist_ok=True)
        os.makedirs("gen_assets/heroes", exist_ok=True)
        os.makedirs("gen_assets/ui", exist_ok=True)
        os.makedirs("gen_assets/cards", exist_ok=True)
        
    def _initialize_pipeline(self):
        """Lazy initialization of SDXL pipeline"""
        if self.pipeline is None:
            if self.use_mock:
                print("Using mock pipeline for testing")
                self.pipeline = "mock"
                return
                
            try:
                print("Loading Stable Diffusion XL pipeline...")
                self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-xl-base-1.0",
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    use_safetensors=True
                )
                
                if self.device == "cuda":
                    self.pipeline = self.pipeline.to("cuda")
                    # RTX 5070 optimizations
                    self.pipeline.enable_model_cpu_offload()
                    self.pipeline.enable_attention_slicing()
                
                print("SDXL pipeline loaded successfully")
                
            except Exception as e:
                print(f"Warning: Could not load SDXL pipeline: {e}")
                print("Using mock generation for development")
                self.pipeline = "mock"
    
    def _get_cache_filename(self, prompt_config):
        """
        Generate consistent filename for caching
        
        Args:
            prompt_config: Prompt configuration dict
            
        Returns:
            str: Cache filename
        """
        content = f"{prompt_config['positive']}_{prompt_config['seed']}"
        hash_obj = hashlib.md5(content.encode())
        return f"{prompt_config['hero']}_{hash_obj.hexdigest()[:8]}.png"
    
    def _generate_image(self, prompt_config):
        """
        Generate image using SDXL or mock for development
        
        Args:
            prompt_config: Complete prompt configuration
            
        Returns:
            PIL.Image: Generated image
        """
        if self.pipeline == "mock":
            # Create mock image for development
            from PIL import Image, ImageDraw, ImageFont
            
            img = Image.new('RGB', (prompt_config['width'], prompt_config['height']), 
                          color=(64, 32, 96))  # Dark gothic color
            draw = ImageDraw.Draw(img)
            
            # Add mock content
            try:
                font = ImageFont.truetype("arial.ttf", 60)
            except:
                font = ImageFont.load_default()
                
            text = f"MOCK {prompt_config['hero'].upper()}\nBACKGROUND"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (prompt_config['width'] - text_width) // 2
            y = (prompt_config['height'] - text_height) // 2
            
            draw.text((x, y), text, fill=(200, 200, 200), font=font)
            
            # Add scene description
            scene_desc = prompt_config.get('scene_desc', 'Medieval scene')
            draw.text((50, 50), scene_desc, fill=(150, 150, 150), font=font)
            
            return img
        
        else:
            # Real SDXL generation
            generator = torch.Generator(device=self.device).manual_seed(prompt_config['seed'])
            
            image = self.pipeline(
                prompt=prompt_config['positive'],
                negative_prompt=prompt_config['negative'],
                width=prompt_config['width'],
                height=prompt_config['height'],
                num_inference_steps=30,
                guidance_scale=7.5,
                generator=generator
            ).images[0]
            
            return image
    
    def generate_hero_background(self, hero_type):
        """
        Generate background for specific hero following art direction
        
        Args:
            hero_type: 'knight', 'mage', or 'assassin'
            
        Returns:
            str: Path to generated image or None if failed
        """
        print(f"Generating background for {hero_type}...")
        
        # Get art direction
        prompt_config = ArtDirection.get_hero_background_prompt(hero_type)
        cache_filename = self._get_cache_filename(prompt_config)
        cache_path = os.path.join(BACKGROUNDS_DIR, cache_filename)
        
        # Check cache first
        if os.path.exists(cache_path):
            print(f"Using cached background: {cache_filename}")
            return cache_path
        
        try:
            # Initialize pipeline if needed
            self._initialize_pipeline()
            
            # Generate image
            image = self._generate_image(prompt_config)
            
            # Save with cache filename
            image.save(cache_path, "PNG", optimize=True)
            print(f"Background generated and saved: {cache_filename}")
            print(f"Scene: {prompt_config['scene_desc']}")
            
            return cache_path
            
        except Exception as e:
            print(f"Error generating background for {hero_type}: {e}")
            return None
    
    def generate_all_hero_backgrounds(self):
        """
        Generate backgrounds for all three heroes
        
        Returns:
            dict: Mapping of hero -> background path
        """
        heroes = ['knight', 'mage', 'assassin']
        backgrounds = {}
        
        print("Generating all hero backgrounds...")
        print("Art style: Gothic medieval realism with dramatic lighting")
        
        for hero in heroes:
            path = self.generate_hero_background(hero)
            if path:
                backgrounds[hero] = path
            else:
                print(f"Failed to generate background for {hero}")
        
        print(f"Generated {len(backgrounds)}/3 hero backgrounds")
        return backgrounds
    
    def generate_hero_sprite(self, hero_type):
        """
        Generate hero character sprite
        
        Args:
            hero_type: 'knight', 'mage', or 'assassin'
            
        Returns:
            str: Path to generated sprite or None if failed
        """
        print(f"Generating sprite for {hero_type}...")
        
        prompt_config = ArtDirection.get_hero_sprite_prompt(hero_type)
        cache_filename = f"sprite_{self._get_cache_filename(prompt_config)}"
        cache_path = os.path.join("gen_assets/heroes", cache_filename)
        
        # Check cache
        if os.path.exists(cache_path):
            print(f"Using cached sprite: {cache_filename}")
            return cache_path
        
        try:
            self._initialize_pipeline()
            image = self._generate_image(prompt_config)
            
            # Save sprite
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            image.save(cache_path, "PNG", optimize=True)
            print(f"Sprite generated: {cache_filename}")
            
            return cache_path
            
        except Exception as e:
            print(f"Error generating sprite for {hero_type}: {e}")
            return None
    
    def get_background_path(self, hero_type):
        """
        Get path to hero background, generate if needed
        
        Args:
            hero_type: Hero type
            
        Returns:
            str: Path to background image
        """
        return self.generate_hero_background(hero_type)
    
    def cleanup_cache(self):
        """Remove all cached generated assets"""
        import shutil
        
        directories = [BACKGROUNDS_DIR, "gen_assets/heroes", "gen_assets/ui", "gen_assets/cards"]
        
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)
                os.makedirs(directory, exist_ok=True)
                
        print("Asset cache cleared")