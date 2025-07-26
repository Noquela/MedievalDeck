"""
TODO Sprint 01:
□ Implementar FrameAnimation class
□ Implementar Tween class para interpolações
□ Testes de animação
"""

from typing import List, Optional
import pygame


class FrameAnimation:
    """Frame-based animation system for sprite sheets."""
    
    def __init__(self, frames: List[pygame.Surface], fps: int = 30, loop: bool = True) -> None:
        """Initialize frame animation.
        
        Args:
            frames: List of pygame surfaces representing animation frames
            fps: Frames per second for animation playback
            loop: Whether animation should loop when finished
        """
        self.frames = frames
        self.fps = fps
        self.loop = loop
        self.frame_duration = 1.0 / fps
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.finished = False
    
    def update(self, dt: float) -> None:
        """Update animation state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.finished and not self.loop:
            return
            
        self.time_accumulator += dt
        
        if self.time_accumulator >= self.frame_duration:
            self.time_accumulator -= self.frame_duration
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
    
    def current(self) -> pygame.Surface:
        """Get current animation frame.
        
        Returns:
            Current frame surface
        """
        if not self.frames:
            # Return empty surface if no frames
            return pygame.Surface((0, 0))
        return self.frames[self.current_frame]
    
    def reset(self) -> None:
        """Reset animation to beginning."""
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.finished = False


class Tween:
    """Simple tween/interpolation system."""
    
    def __init__(self, start_value: float, end_value: float, duration: float) -> None:
        """Initialize tween.
        
        Args:
            start_value: Starting value
            end_value: Target value
            duration: Tween duration in seconds
        """
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.current_time = 0.0
        self.finished = False
    
    def update(self, dt: float) -> None:
        """Update tween state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.finished:
            return
            
        self.current_time += dt
        if self.current_time >= self.duration:
            self.current_time = self.duration
            self.finished = True
    
    def value(self) -> float:
        """Get current interpolated value.
        
        Returns:
            Current tween value
        """
        if self.duration <= 0:
            return self.end_value
            
        t = self.current_time / self.duration
        # Linear interpolation
        return self.start_value + (self.end_value - self.start_value) * t
    
    def reset(self) -> None:
        """Reset tween to beginning."""
        self.current_time = 0.0
        self.finished = False
