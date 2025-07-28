"""
Medieval Deck - Jogo de Cartas Roguelike
Arquivo principal do jogo
"""

import pygame
import sys
from config import *

class Game:
    def __init__(self):
        """Inicializa o jogo e configurações básicas"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Medieval Deck")
        self.clock = pygame.time.Clock()
        self.running = True
        
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
        # Preenche a tela com preto (placeholder)
        self.screen.fill((0, 0, 0))
        
        # Aqui serão adicionadas as telas do jogo posteriormente
        
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