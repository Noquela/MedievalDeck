"""
Sistema de botões para o jogo Medieval Deck
"""

import pygame
from config import *

class Button:
    def __init__(self, x, y, width, height, text, color=WHITE, hover_color=GRAY):
        """
        Inicializa um botão
        
        Args:
            x, y: Posição do botão
            width, height: Dimensões do botão
            text: Texto do botão
            color: Cor normal do botão
            hover_color: Cor quando o mouse está sobre o botão
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        """Desenha o botão na tela"""
        # Desenha o retângulo do botão
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Borda
        
        # Renderiza o texto
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        """Processa eventos do mouse para o botão"""
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def is_clicked(self, pos):
        """Verifica se o botão foi clicado"""
        return self.rect.collidepoint(pos) 