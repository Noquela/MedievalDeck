"""
TODO Sprint 01:
□ Implementar ParticleEmitter class
□ Sistema de partículas para efeitos visuais
□ Testes de partículas
"""

from typing import List, Tuple
import pygame
import random
import math


class Particle:
    """Individual particle for visual effects."""
    
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float, 
                 color: Tuple[int, int, int], life: float, size: float = 2.0) -> None:
        """Initialize particle.
        
        Args:
            x: Starting X position
            y: Starting Y position
            vel_x: X velocity
            vel_y: Y velocity
            color: RGB color tuple
            life: Particle lifetime in seconds
            size: Particle size in pixels
        """
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.alive = True
    
    def update(self, dt: float) -> None:
        """Update particle state.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.alive:
            return
            
        # Update position
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        
        # Apply gravity
        self.vel_y += 200.0 * dt  # Gravity acceleration
        
        # Update life
        self.life -= dt
        if self.life <= 0:
            self.alive = False
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw particle to surface.
        
        Args:
            surface: Target surface to draw on
        """
        if not self.alive:
            return
            
        # Calculate alpha based on remaining life
        alpha_ratio = self.life / self.max_life
        alpha = int(255 * alpha_ratio)
        alpha = max(0, min(255, alpha))
        
        # Create color with alpha
        color_with_alpha = (*self.color, alpha)
        
        # Draw particle as small circle
        current_size = max(1, int(self.size * alpha_ratio))
        pos = (int(self.x), int(self.y))
        
        # Create temporary surface for alpha blending
        temp_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, color_with_alpha, (current_size, current_size), current_size)
        
        surface.blit(temp_surface, (pos[0] - current_size, pos[1] - current_size), 
                    special_flags=pygame.BLEND_ALPHA_SDL2)


class ParticleEmitter:
    """Particle emitter for creating visual effects."""
    
    def __init__(self, pos: Tuple[float, float], n: int = 12, 
                 color: Tuple[int, int, int] = (255, 255, 255), life: float = 0.4) -> None:
        """Initialize particle emitter.
        
        Args:
            pos: Emitter position (x, y)
            n: Number of particles to emit
            color: Base color for particles
            life: Base lifetime for particles
        """
        self.pos = pos
        self.particles: List[Particle] = []
        
        # Emit particles
        for _ in range(n):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed - random.uniform(50, 100)  # Bias upward
            
            particle_life = life + random.uniform(-0.1, 0.2)
            particle_size = random.uniform(1.5, 3.0)
            
            # Add some color variation
            color_variation = 20
            varied_color = (
                max(0, min(255, color[0] + random.randint(-color_variation, color_variation))),
                max(0, min(255, color[1] + random.randint(-color_variation, color_variation))),
                max(0, min(255, color[2] + random.randint(-color_variation, color_variation)))
            )
            
            particle = Particle(pos[0], pos[1], vel_x, vel_y, varied_color, particle_life, particle_size)
            self.particles.append(particle)
    
    def update(self, dt: float) -> None:
        """Update all particles.
        
        Args:
            dt: Delta time in seconds
        """
        for particle in self.particles:
            particle.update(dt)
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.alive]
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all particles.
        
        Args:
            surface: Target surface to draw on
        """
        for particle in self.particles:
            particle.draw(surface)
    
    def is_finished(self) -> bool:
        """Check if all particles are dead.
        
        Returns:
            True if no particles remain alive
        """
        return len(self.particles) == 0
