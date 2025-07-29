"""
RTX 5070 Optimization System for Medieval Deck
Sprint 4 Implementation: Maximum quality with optimized performance
"""

import torch
import gc
import psutil
import os
from contextlib import contextmanager

class RTX5070Optimizer:
    """
    Advanced optimization system specifically tuned for RTX 5070
    Balances quality and performance for SDXL generation
    """
    
    def __init__(self):
        """Initialize RTX 5070 specific optimizations"""
        self.device = self._detect_optimal_device()
        self.memory_fraction = 0.95  # Use 95% of VRAM for generation
        self.compile_mode = "reduce-overhead"  # Best for RTX 5070
        
        print(f"RTX 5070 Optimizer initialized")
        print(f"Device: {self.device}")
        print(f"CUDA Version: {torch.version.cuda if torch.cuda.is_available() else 'N/A'}")
        
        self._setup_memory_management()
        self._setup_cuda_optimizations()
        
    def _detect_optimal_device(self):
        """Detect and configure optimal device settings"""
        if not torch.cuda.is_available():
            print("CUDA not available, using CPU")
            return "cpu"
            
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"GPU: {gpu_name}")
        print(f"VRAM: {vram_gb:.1f} GB")
        
        # RTX 5070 specific optimizations
        if "RTX" in gpu_name and "5070" in gpu_name:
            print("RTX 5070 detected - applying specialized optimizations")
            return "cuda"
        elif "RTX" in gpu_name:
            print("RTX GPU detected - applying RTX optimizations")
            return "cuda"
        else:
            print("Non-RTX GPU detected - using standard CUDA")
            return "cuda"
    
    def _setup_memory_management(self):
        """Configure advanced memory management for RTX 5070"""
        if self.device == "cuda":
            # RTX 5070 has 12GB VRAM - optimize usage
            torch.cuda.set_per_process_memory_fraction(self.memory_fraction)
            torch.cuda.empty_cache()
            
            # Enable memory-efficient attention
            torch.backends.cuda.enable_flash_sdp(True)
            
            print("Memory management configured for RTX 5070")
            print(f"VRAM allocation: {self.memory_fraction * 100}%")
    
    def _setup_cuda_optimizations(self):
        """Setup CUDA-specific optimizations"""
        if self.device == "cuda":
            # Enable cuDNN benchmarking for consistent input sizes
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False  # For speed
            
            # RTX 5070 supports these optimizations
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            print("CUDA optimizations enabled for RTX 5070")
    
    def optimize_pipeline(self, pipeline):
        """
        Apply comprehensive optimizations to SDXL pipeline
        
        Args:
            pipeline: Diffusers SDXL pipeline
            
        Returns:
            Optimized pipeline
        """
        if self.device == "cpu":
            return pipeline
            
        print("Applying RTX 5070 optimizations to pipeline...")
        
        # Move to GPU with optimal dtype
        pipeline = pipeline.to("cuda", torch_dtype=torch.float16)
        
        # Enable memory efficient attention
        pipeline.enable_attention_slicing(1)
        pipeline.enable_model_cpu_offload()
        
        # RTX 5070 specific optimizations
        try:
            # Enable xformers if available (major speedup)
            pipeline.enable_xformers_memory_efficient_attention()
            print("xFormers memory efficient attention enabled")
        except Exception as e:
            print(f"xFormers not available: {e}")
        
        try:
            # Compile UNet for RTX 5070 (PyTorch 2.0+ feature)
            pipeline.unet = torch.compile(
                pipeline.unet,
                mode=self.compile_mode,
                dynamic=False
            )
            print("UNet compiled with torch.compile")
        except Exception as e:
            print(f"Torch compile not available: {e}")
        
        # VAE optimizations
        try:
            pipeline.vae.enable_slicing()
            pipeline.vae.enable_tiling()
            print("VAE slicing and tiling enabled")
        except Exception as e:
            print(f"VAE optimizations failed: {e}")
        
        return pipeline
    
    def get_optimal_generation_params(self, resolution=(3440, 1440)):
        """
        Get optimal generation parameters for RTX 5070
        
        Args:
            resolution: Target resolution tuple
            
        Returns:
            dict: Optimal parameters
        """
        width, height = resolution
        
        # RTX 5070 can handle high resolution efficiently
        params = {
            'num_inference_steps': 30,  # Good quality/speed balance
            'guidance_scale': 7.5,      # Standard for SDXL
            'width': width,
            'height': height,
            'generator': None,  # Will be set per generation
        }
        
        # Adjust based on resolution for memory optimization
        total_pixels = width * height
        if total_pixels > 3840 * 2160:  # 4K+
            params['num_inference_steps'] = 25  # Reduce for very high res
        elif total_pixels < 1920 * 1080:  # Below 1080p
            params['num_inference_steps'] = 35  # Increase for small images
            
        return params
    
    @contextmanager
    def optimized_generation(self):
        """Context manager for optimized generation session"""
        if self.device == "cuda":
            # Pre-generation optimizations
            torch.cuda.empty_cache()
            gc.collect()
            
            # Monitor VRAM usage
            vram_before = torch.cuda.memory_allocated() / 1024**3
            print(f"VRAM before generation: {vram_before:.2f} GB")
        
        try:
            yield
        finally:
            if self.device == "cuda":
                # Post-generation cleanup
                torch.cuda.empty_cache()
                gc.collect()
                
                vram_after = torch.cuda.memory_allocated() / 1024**3
                print(f"VRAM after cleanup: {vram_after:.2f} GB")
    
    def benchmark_generation(self, pipeline, prompt, num_runs=3):
        """
        Benchmark generation performance
        
        Args:
            pipeline: SDXL pipeline
            prompt: Test prompt
            num_runs: Number of benchmark runs
            
        Returns:
            dict: Benchmark results
        """
        import time
        
        print(f"Benchmarking generation performance ({num_runs} runs)...")
        
        params = self.get_optimal_generation_params((1024, 1024))  # Standard test size
        times = []
        
        # Warm-up run
        with self.optimized_generation():
            _ = pipeline(prompt, **params)
        
        # Benchmark runs
        for i in range(num_runs):
            with self.optimized_generation():
                start_time = time.time()
                _ = pipeline(prompt, **params)
                end_time = time.time()
                
                generation_time = end_time - start_time
                times.append(generation_time)
                print(f"Run {i+1}: {generation_time:.2f}s")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        results = {
            'average_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'times': times
        }
        
        print(f"Benchmark Results:")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s") 
        print(f"  Max: {max_time:.2f}s")
        
        return results
    
    def get_memory_info(self):
        """Get current memory usage information"""
        info = {
            'system_ram_gb': psutil.virtual_memory().total / 1024**3,
            'system_ram_used_gb': psutil.virtual_memory().used / 1024**3,
        }
        
        if self.device == "cuda":
            info.update({
                'vram_total_gb': torch.cuda.get_device_properties(0).total_memory / 1024**3,
                'vram_allocated_gb': torch.cuda.memory_allocated() / 1024**3,
                'vram_cached_gb': torch.cuda.memory_reserved() / 1024**3,
            })
        
        return info
    
    def print_system_info(self):
        """Print comprehensive system information"""
        print("\n" + "="*60)
        print("RTX 5070 OPTIMIZATION SYSTEM INFO")
        print("="*60)
        
        memory_info = self.get_memory_info()
        
        print(f"System RAM: {memory_info['system_ram_used_gb']:.1f}/{memory_info['system_ram_gb']:.1f} GB")
        
        if self.device == "cuda":
            print(f"GPU VRAM: {memory_info['vram_allocated_gb']:.1f}/{memory_info['vram_total_gb']:.1f} GB")
            print(f"CUDA Version: {torch.version.cuda}")
            print(f"PyTorch Version: {torch.__version__}")
            
            # Check for optimization libraries
            try:
                import xformers
                print(f"xFormers: {xformers.__version__}")
            except ImportError:
                print("xFormers: Not installed")
                
            try:
                import flash_attn
                print(f"Flash Attention: Available")
            except ImportError:
                print("Flash Attention: Not installed")
        
        print("="*60)