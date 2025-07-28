"""
Medieval Deck - Jogo de Cartas Roguelike
Arquivo principal do jogo
"""

import pygame
import sys
from config import *
from screens.menu import mostrar_menu
from screens.selection import tela_selecao
from screens.gameplay import tela_combate

class Game:
    def __init__(self):
        """Inicializa o jogo e configurações básicas"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Medieval Deck")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = STATE_MENU
        
    def handle_events(self):
        """Processa eventos do Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Atualiza lógica do jogo"""
        pass
    
    def render(self):
        """Renderiza elementos na tela"""
        # Gerencia as diferentes telas do jogo
        if self.current_state == STATE_MENU:
            result = mostrar_menu(self.screen)
            if result == 'quit':
                self.running = False
            elif result == 'selection':
                self.current_state = STATE_SELECTION
            elif result == 'options':
                # TODO: Implementar tela de opções
                pass
        elif self.current_state == STATE_SELECTION:
            result = tela_selecao(self.screen)
            if result == 'quit':
                self.running = False
            elif result == 'menu':
                self.current_state = STATE_MENU
            elif result == 'gameplay':
                self.current_state = STATE_GAMEPLAY
        elif self.current_state == STATE_GAMEPLAY:
            result = tela_combate(self.screen)
            if result == 'quit':
                self.running = False
            elif result == 'menu':
                self.current_state = STATE_MENU
        else:
            # Tela padrão (preto)
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """Função principal que inicia o jogo"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 