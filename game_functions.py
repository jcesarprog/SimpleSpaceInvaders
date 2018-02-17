import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_events(ai_settings, screen, stats, sb, play_button,ship, aliens, bullets):
    '''Responde a eventos de teclas e mouse'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Inicia um novo jogo ao cliclar em Play'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reinicia as configuracoes originais
        ai_settings.initialize_dynamic_settings()

        # Oculta o cursor
        pygame.mouse.set_visible(False)

        # Reinicia os dados do jogo
        stats.reset_stats()
        stats.game_active = True

        # Reinicia as imagens do painel de pontuacao
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Esvazia a lista de aliens e de projeteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Responde a pressionamentos de tecla'''
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        # move para a direita
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # move para a esquerda
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    '''Responde a soltura de teclas'''
    if event.key == pygame.K_RIGHT:
        # para de mover para a direita
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # move para a esquerda
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Redesenha a tela a cada passagem do laco
    screen.fill(ai_settings.bg_color)

    # Redesenha todos os projeteis atrás da espaconave e dos alienigenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Deseha a informacao sobre a pontuacao
    sb.show_score()

    # Desenha o botao Play se o jogo estiver INATIVO
    if not stats.game_active:
        play_button.draw_button()

    # Deixa a tela mais recente visivel
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Atualiza a posicao dos projeteis e se livra dos antigos'''

    bullets.update()

    # Apaga os projeteis que sumiram da tela
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #print(len(bullets))


    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Trata Colisoes entre aliens e tiros'''
    # Verifica se algum projetil atingiu um alien
    # Caso tenha colidido, se livra do projetil e do alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroi os projeteis existentes e cria uma nova frota e inicia um novo nivel
        bullets.empty()
        ai_settings.increase_speed()

        # Aumenta o nivel
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
    '''Dispara um projetil se o limite nao tiver sido alcancado'''
    if len(bullets) < ai_settings.bullets_allowed:
        # cria um novo projetil e o adiciona ao grupo de projeteis
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)


def get_number_aliens_x(ai_settings, alien_width):
    '''Determina o numero de aliens que cabem em uma linha'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determina o numero de linhas com aliens q cabem na tela'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Cria um alien e o posiciona na linha e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    '''Cria a frota de Aliens'''
    # Cria um alien e calcula o numero de aliens em uma linha
    # O Espacamento entre os aliens é igual a largura de um alien
    # Cria um alien e calcula o numero de aliens em uma linha
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        # Cria a linha da frota
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    '''Faz toda a frota descer e muda a sua direcao'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    '''Responde apropeiadamente se algum alien alcancou uma borda'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Verifica se a frota esta em uma das bordas e
    Atualiza as posicoes de todos os aliens da frota'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Verifica colisoes entre aliens e a nave
    if pygame.sprite.spritecollideany(ship, aliens):
        #print("NAVE ACERTADA!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Responde quando a nave for atingida'''

    if stats.ships_left > 0:
        # Decrementa ships_left
        stats.ships_left -= 1

        # Atualiza as naves no painel
        sb.prep_ships()

        # Esvazia a lista de aliens e projeteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a nave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma pausa
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Verifica se algum alien chegou na parte inferior da tela'''
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata do mesmo jeito de quando a nave é atingida
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    '''Verifica se ha uma pontuacao maxima'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()