import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

def run_game():
    # Inicializa o jogo, as configuracoes e  cria o objeto tela
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption(ai_settings.screen_title)

    # Cria o botao Play
    play_button = Button(ai_settings, screen, "PLAY")

    # Cria um objeto para armazenar os dados do jogo
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # Cria a nave
    ship = Ship(ai_settings, screen)

    # Cria um grupo para os Tiros
    bullets = Group()

    # Cria um grupo para os Aliens
    aliens = Group()

    # Cria a frota de aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)


    # Laco principal do jogo
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()


