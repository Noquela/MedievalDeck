"""
Tela de menu principal do jogo Medieval Deck
"""

import pygame
from config import *
from utils.buttons import Button

def mostrar_menu(screen):
    """
    Exibe a tela de menu principal
    
    Args:
        screen: Superfície do Pygame onde desenhar
        
    Returns:
        str: Estado para qual tela ir ('selection', 'options', 'quit')
    """
    # Configuração da fonte para o título
    title_font = pygame.font.Font(None, 72)
    title_text = title_font.render("Medieval Deck", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    
    # Configuração dos botões
    button_width = 300
    button_height = 80
    button_x = (SCREEN_WIDTH - button_width) // 2
    
    # Posições dos botões (centralizados verticalmente)
    start_y = SCREEN_HEIGHT // 2
    spacing = 100
    
    jogar_btn = Button(button_x, start_y, button_width, button_height, "Jogar")
    opcoes_btn = Button(button_x, start_y + spacing, button_width, button_height, "Opções")
    sair_btn = Button(button_x, start_y + spacing * 2, button_width, button_height, "Sair")
    
    buttons = [jogar_btn, opcoes_btn, sair_btn]
    
    running = True
    while running:
        # Preenche a tela com preto
        screen.fill(BLACK)
        
        # Desenha o título
        screen.blit(title_text, title_rect)
        
        # Desenha os botões
        for button in buttons:
            button.draw(screen)
        
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
            
            # Processa eventos dos botões
            for i, button in enumerate(buttons):
                if button.handle_event(event):
                    if i == 0:  # Jogar
                        return 'selection'
                    elif i == 1:  # Opções
                        return 'options'
                    elif i == 2:  # Sair
                        return 'quit'
        
        pygame.display.flip()
    
    return 'quit' 