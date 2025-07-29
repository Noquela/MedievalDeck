"""
AI Asset Generator for Medieval Deck
Sprint 4 Implementation: RTX 5070 optimized SDXL with hero sprite generation
Following art direction for gothic medieval realism with maximum quality
"""

import os
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image, ImageFilter, ImageEnhance
import hashlib
import time
from config import AI_SEED, AI_IMAGE_SIZE, BACKGROUNDS_DIR
from .art_direction import ArtDirection
from .rtx_optimizer import RTX5070Optimizer

class AssetGenerator:
    """
    SDXL-based asset generator following Medieval Deck art direction
    Optimized for RTX 5070 with consistent styling
    """
    
    def __init__(self, use_mock=False):
        """Initialize RTX 5070 optimized SDXL pipeline"""
        self.use_mock = use_mock
        self.optimizer = RTX5070Optimizer()
        self.device = self.optimizer.device
        self.pipeline = None
        self.cache_dir = "gen_assets"
        
        print(f"AssetGenerator initialized - Device: {self.device}")
        print("Sprint 4: RTX 5070 optimized AI generation with maximum quality")
        
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
                print("Loading RTX 5070 optimized SDXL pipeline...")
                print("This may take a few minutes on first run...")
                
                # Load base SDXL model
                self.pipeline = StableDiffusionXLPipeline.from_pretrained(
                    "stabilityai/stable-diffusion-xl-base-1.0",
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    use_safetensors=True,
                    variant="fp16" if self.device == "cuda" else None
                )
                
                # Apply RTX 5070 optimizations
                if self.device == "cuda":
                    self.pipeline = self.optimizer.optimize_pipeline(self.pipeline)
                    self.optimizer.print_system_info()
                
                print("RTX 5070 optimized SDXL pipeline ready!")
                
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
            # RTX 5070 optimized SDXL generation
            generator = torch.Generator(device=self.device).manual_seed(prompt_config['seed'])
            
            # Get optimal parameters for RTX 5070
            optimal_params = self.optimizer.get_optimal_generation_params(
                (prompt_config['width'], prompt_config['height'])
            )
            optimal_params['generator'] = generator
            
            # Generate with optimization context
            with self.optimizer.optimized_generation():
                start_time = time.time()
                
                image = self.pipeline(
                    prompt=prompt_config['positive'],
                    negative_prompt=prompt_config['negative'],
                    **optimal_params
                ).images[0]
                
                generation_time = time.time() - start_time
                print(f"Generation completed in {generation_time:.2f}s")
            
            # Apply post-processing for enhanced quality
            image = self._enhance_image_quality(image)
            
            return image
    
    def _enhance_image_quality(self, image):
        """
        Apply post-processing to enhance image quality
        Optimized for medieval gothic art style
        
        Args:
            image: PIL Image to enhance
            
        Returns:
            PIL Image: Enhanced image
        """
        try:
            # Subtle sharpening for detail enhancement
            sharpening_filter = ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3)
            image = image.filter(sharpening_filter)
            
            # Enhance contrast for dramatic medieval look
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            
            # Slight color saturation boost for richness
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.05)
            
            print("Image quality enhanced with medieval gothic processing")
            return image
            
        except Exception as e:
            print(f"Warning: Image enhancement failed: {e}")
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
        Generate high-quality hero character sprite with RTX 5070 optimization
        
        Args:
            hero_type: 'knight', 'mage', or 'assassin'
            
        Returns:
            str: Path to generated sprite or None if failed
        """
        print(f"Generating RTX 5070 optimized sprite for {hero_type}...")
        
        prompt_config = ArtDirection.get_hero_sprite_prompt(hero_type)
        cache_filename = f"sprite_{self._get_cache_filename(prompt_config)}"
        cache_path = os.path.join("gen_assets/heroes", cache_filename)
        
        # Check cache
        if os.path.exists(cache_path):
            print(f"Using cached sprite: {cache_filename}")
            return cache_path
        
        try:
            self._initialize_pipeline()
            
            # Generate base sprite
            image = self._generate_image(prompt_config)
            
            # Apply sprite-specific post-processing
            image = self._process_sprite(image, hero_type)
            
            # Save sprite with high quality
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            image.save(cache_path, "PNG", optimize=True, quality=95)
            print(f"High-quality sprite generated: {cache_filename}")
            print(f"Character: {prompt_config['character_desc']}")
            
            return cache_path
            
        except Exception as e:
            print(f"Error generating sprite for {hero_type}: {e}")
            return None
    
    def _process_sprite(self, image, hero_type):
        """
        Apply sprite-specific processing for character clarity
        
        Args:
            image: Base sprite image
            hero_type: Hero type for specific adjustments
            
        Returns:
            PIL Image: Processed sprite
        """
        try:
            # Extra sharpening for character details
            sharpening_filter = ImageFilter.UnsharpMask(radius=2.0, percent=150, threshold=2)
            image = image.filter(sharpening_filter)
            
            # Hero-specific adjustments
            if hero_type == 'knight':
                # Enhance metallic details
                enhancer = ImageEnhance.Contrast(image)
                image = enhancer.enhance(1.15)
            elif hero_type == 'mage':
                # Enhance magical glow effects
                enhancer = ImageEnhance.Color(image)
                image = enhancer.enhance(1.2)
            elif hero_type == 'assassin':
                # Enhance shadow definition
                enhancer = ImageEnhance.Brightness(image)
                image = enhancer.enhance(0.95)
            
            print(f"Sprite processing applied for {hero_type}")
            return image
            
        except Exception as e:
            print(f"Warning: Sprite processing failed: {e}")
            return image
    
    def generate_all_hero_sprites(self):
        """
        Generate high-quality sprites for all heroes
        
        Returns:
            dict: Mapping of hero -> sprite path
        """
        heroes = ['knight', 'mage', 'assassin']
        sprites = {}
        
        print("Generating all hero sprites with RTX 5070 optimization...")
        print("Character art style: Gothic medieval realism with enhanced details")
        
        for hero in heroes:
            path = self.generate_hero_sprite(hero)
            if path:
                sprites[hero] = path
            else:
                print(f"Failed to generate sprite for {hero}")
        
        print(f"Generated {len(sprites)}/3 hero sprites")
        return sprites
    
    def benchmark_system(self):
        """
        Comprehensive benchmark of the RTX 5070 system
        
        Returns:
            dict: Benchmark results
        """
        if self.use_mock or self.device == "cpu":
            print("Benchmarking not available in mock/CPU mode")
            return None
            
        self._initialize_pipeline()
        
        test_prompt = "Medieval knight in ornate armor, dramatic lighting, highly detailed"
        results = self.optimizer.benchmark_generation(self.pipeline, test_prompt)
        
        # Add system info to results
        results['memory_info'] = self.optimizer.get_memory_info()
        results['device'] = self.device
        
        return results
    
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