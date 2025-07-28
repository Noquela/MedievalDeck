"""
Tela de seleção de personagem do jogo Medieval Deck
"""

import pygame
import os
from config import *
from utils.buttons import Button

# Dados dos heróis
HEROES = {
    'knight': {
        'nome': 'Knight',
        'descricao': 'Guerreiro equilibrado com boa defesa e ataque físico',
        'cor': (139, 69, 19),  # Marrom
        'posicao': (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    },
    'mage': {
        'nome': 'Mage',
        'descricao': 'Mago poderoso com magias devastadoras',
        'cor': (75, 0, 130),  # Roxo
        'posicao': (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    },
    'assassin': {
        'nome': 'Assassin',
        'descricao': 'Assassino ágil com ataques críticos',
        'cor': (47, 79, 79),  # Cinza escuro
        'posicao': (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    }
}

def tela_selecao(screen):
    """
    Exibe a tela de seleção de personagem
    
    Args:
        screen: Superfície do Pygame onde desenhar
        
    Returns:
        str: Estado para qual tela ir ('menu', 'gameplay', 'quit')
    """
    # Carrega backgrounds se existirem
    backgrounds = {}
    for hero_id in HEROES.keys():
        bg_path = os.path.join(BACKGROUNDS_PATH, f"bg_{hero_id}_hall.png")
        if os.path.exists(bg_path):
            try:
                backgrounds[hero_id] = pygame.image.load(bg_path)
                # Redimensiona para a tela
                backgrounds[hero_id] = pygame.transform.scale(backgrounds[hero_id], (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                backgrounds[hero_id] = None
        else:
            backgrounds[hero_id] = None
    # Configuração das fontes
    title_font = pygame.font.Font(None, 64)
    hero_font = pygame.font.Font(None, 48)
    desc_font = pygame.font.Font(None, 32)
    
    # Título
    title_text = title_font.render("Escolha seu Herói", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    
    # Botão confirmar
    confirm_btn = Button(
        SCREEN_WIDTH // 2 - 150, 
        SCREEN_HEIGHT - 150, 
        300, 80, 
        "Confirmar",
        color=(0, 100, 0),  # Verde
        hover_color=(0, 150, 0)
    )
    
    # Botão voltar
    voltar_btn = Button(
        50, 50, 150, 50, 
        "Voltar",
        color=(100, 0, 0),  # Vermelho
        hover_color=(150, 0, 0)
    )
    
    heroi_selecionado = None
    running = True
    
    while running:
        # Preenche a tela com preto
        screen.fill(BLACK)
        
        # Desenha background se disponível para o herói selecionado
        if heroi_selecionado and backgrounds.get(heroi_selecionado):
            screen.blit(backgrounds[heroi_selecionado], (0, 0))
        else:
            # Fundo padrão com gradiente escuro
            for y in range(SCREEN_HEIGHT):
                alpha = int(255 * (1 - y / SCREEN_HEIGHT))
                color = (0, 0, alpha // 4)
                pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
        
        # Desenha o título
        screen.blit(title_text, title_rect)
        
        # Desenha os heróis
        for hero_id, hero_data in HEROES.items():
            x, y = hero_data['posicao']
            cor = hero_data['cor']
            
            # Círculo do herói
            raio = 80
            if heroi_selecionado == hero_id:
                # Destaca o herói selecionado
                pygame.draw.circle(screen, WHITE, (x, y), raio + 10)
                pygame.draw.circle(screen, cor, (x, y), raio)
            else:
                pygame.draw.circle(screen, cor, (x, y), raio)
            
            # Nome do herói
            nome_text = hero_font.render(hero_data['nome'], True, WHITE)
            nome_rect = nome_text.get_rect(center=(x, y + 120))
            screen.blit(nome_text, nome_rect)
            
            # Descrição (apenas para o herói selecionado)
            if heroi_selecionado == hero_id:
                # Quebra a descrição em linhas
                descricao = hero_data['descricao']
                palavras = descricao.split()
                linhas = []
                linha_atual = ""
                
                for palavra in palavras:
                    if len(linha_atual + " " + palavra) < 30:
                        linha_atual += " " + palavra if linha_atual else palavra
                    else:
                        linhas.append(linha_atual)
                        linha_atual = palavra
                if linha_atual:
                    linhas.append(linha_atual)
                
                # Desenha as linhas da descrição
                for i, linha in enumerate(linhas):
                    desc_text = desc_font.render(linha, True, WHITE)
                    desc_rect = desc_text.get_rect(center=(x, y + 180 + i * 30))
                    screen.blit(desc_text, desc_rect)
        
        # Desenha os botões
        confirm_btn.draw(screen)
        voltar_btn.draw(screen)
        
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
            
            # Processa eventos dos botões
            if confirm_btn.handle_event(event):
                if heroi_selecionado:
                    return 'gameplay'
            elif voltar_btn.handle_event(event):
                return 'menu'
            
            # Processa clique nos heróis
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for hero_id, hero_data in HEROES.items():
                    x, y = hero_data['posicao']
                    # Verifica se clicou no círculo do herói
                    distancia = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
                    if distancia <= 80:
                        heroi_selecionado = hero_id
                        break
        
        pygame.display.flip()
    
    return 'menu' 