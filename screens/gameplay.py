"""
Tela de gameplay/combate do jogo Medieval Deck
"""

import pygame
from config import *

def tela_combate(screen):
    """
    Exibe a tela de combate (placeholder para Sprint 5)
    
    Args:
        screen: Superfície do Pygame onde desenhar
        
    Returns:
        str: Estado para qual tela ir ('menu', 'quit')
    """
    # Configuração da fonte
    font = pygame.font.Font(None, 48)
    
    # Texto placeholder
    text = font.render("Tela de Combate - Sprint 5", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Botão voltar
    voltar_btn = pygame.Rect(50, 50, 150, 50)
    
    running = True
    while running:
        # Preenche a tela com preto
        screen.fill(BLACK)
        
        # Desenha o texto placeholder
        screen.blit(text, text_rect)
        
        # Desenha botão voltar
        pygame.draw.rect(screen, RED, voltar_btn)
        voltar_text = font.render("Voltar", True, WHITE)
        voltar_text_rect = voltar_text.get_rect(center=voltar_btn.center)
        screen.blit(voltar_text, voltar_text_rect)
        
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_btn.collidepoint(event.pos):
                    return 'menu'
        
        pygame.display.flip()
    
    return 'menu' 