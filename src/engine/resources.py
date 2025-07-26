"""
TODO Sprint 01:
□ Sistema de cache de texturas
□ Função load_texture com memoização
□ Utilitários de carregamento de assets
"""

from typing import Dict, Optional
import pygame
import os


class ResourceManager:
    """Manages loading and caching of game resources."""
    
    def __init__(self) -> None:
        """Initialize resource manager."""
        self._texture_cache: Dict[str, pygame.Surface] = {}
        self._font_cache: Dict[str, pygame.font.Font] = {}
    
    def load_texture(self, path: str) -> pygame.Surface:
        """Load and cache a texture.
        
        Args:
            path: Path to image file
            
        Returns:
            Pygame surface containing the image
            
        Raises:
            FileNotFoundError: If image file doesn't exist
        """
        # Check cache first
        if path in self._texture_cache:
            return self._texture_cache[path]
        
        # Load from disk
        if not os.path.exists(path):
            raise FileNotFoundError(f"Texture not found: {path}")
            
        try:
            surface = pygame.image.load(path).convert_alpha()
            # Cache the loaded surface
            self._texture_cache[path] = surface
            return surface
        except pygame.error as e:
            raise RuntimeError(f"Failed to load texture {path}: {e}")
    
    def load_font(self, path: Optional[str] = None, size: int = 24) -> pygame.font.Font:
        """Load and cache a font.
        
        Args:
            path: Path to font file (None for default font)
            size: Font size
            
        Returns:
            Pygame font object
        """
        cache_key = f"{path}_{size}"
        
        # Check cache first
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Load font
        if path is None:
            font = pygame.font.Font(None, size)
        else:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Font not found: {path}")
            font = pygame.font.Font(path, size)
        
        # Cache the loaded font
        self._font_cache[cache_key] = font
        return font
    
    def load_sprite_sheet(self, path: str, frame_width: int, frame_height: int, 
                         frame_count: int) -> list[pygame.Surface]:
        """Load a sprite sheet and split into frames.
        
        Args:
            path: Path to sprite sheet image
            frame_width: Width of each frame
            frame_height: Height of each frame
            frame_count: Number of frames in the sheet
            
        Returns:
            List of pygame surfaces, one per frame
        """
        sheet = self.load_texture(path)
        frames = []
        
        for i in range(frame_count):
            x = i * frame_width
            if x + frame_width > sheet.get_width():
                break  # Don't go beyond sheet bounds
                
            frame_rect = pygame.Rect(x, 0, frame_width, frame_height)
            frame = sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        
        return frames
    
    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self._texture_cache.clear()
        self._font_cache.clear()
    
    def get_cache_size(self) -> int:
        """Get number of cached resources.
        
        Returns:
            Total number of cached textures and fonts
        """
        return len(self._texture_cache) + len(self._font_cache)


# Global resource manager instance
_resource_manager = ResourceManager()


def load_texture(path: str) -> pygame.Surface:
    """Convenience function to load texture using global resource manager.
    
    Args:
        path: Path to image file
        
    Returns:
        Pygame surface containing the image
    """
    return _resource_manager.load_texture(path)


def load_font(path: Optional[str] = None, size: int = 24) -> pygame.font.Font:
    """Convenience function to load font using global resource manager.
    
    Args:
        path: Path to font file (None for default font)
        size: Font size
        
    Returns:
        Pygame font object
    """
    return _resource_manager.load_font(path, size)


def load_sprite_sheet(path: str, frame_width: int, frame_height: int, 
                     frame_count: int) -> list[pygame.Surface]:
    """Convenience function to load sprite sheet using global resource manager.
    
    Args:
        path: Path to sprite sheet image
        frame_width: Width of each frame
        frame_height: Height of each frame
        frame_count: Number of frames in the sheet
        
    Returns:
        List of pygame surfaces, one per frame
    """
    return _resource_manager.load_sprite_sheet(path, frame_width, frame_height, frame_count)


def load_image(path: str, cache: bool = True) -> Optional[pygame.Surface]:
    """Load an image with optional caching.
    
    Args:
        path: Path to image file
        cache: Whether to use caching (ignored, always cached)
        
    Returns:
        Pygame surface or None if loading fails
    """
    try:
        return _resource_manager.load_texture(path)
    except (FileNotFoundError, RuntimeError):
        return None
