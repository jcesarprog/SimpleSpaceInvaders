import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Classe que adminstra os tiros'''

    def __init__(self, ai_settings, screen, ship):
        '''Cria o objeto do projetil na posicao atual da nave'''
        super(Bullet, self).__init__()
        self.screen = screen

        # Cria um retangulo para o projetil em (0,0) e em seguida, define a posical correta
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Armazena a posicao do projetil como um valor decimal
        self.y = float(self.rect.y)

        # Configuracoes do tiro
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        '''Move o projetil para cima da tela'''

        # Atualiza a posicao decimal do projetil
        self.y -= self.speed_factor
        # Atualiza a posicao de rect
        self.rect.y = self.y


    def draw_bullet(self):
        '''Desenha o projetil na Tela'''
        pygame.draw.rect(self.screen, self.color, self.rect)

