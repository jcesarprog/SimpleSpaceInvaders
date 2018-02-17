class Settings():
    # Classe para armazenar as configuracoes
    def __init__(self):
        # Inicializa as configuracoes do jogo

        # Configuracoes de tela
        self.screen_title = "Alien Invasion"
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Configuracoes da nave
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Configuracoes dos projeteis
        self.bullet_speed_factor = 3
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # Configuracoes dos aliens
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction = 1 é para a direita e -1 para a esquerda
        self.fleet_direction = 1

        # A taxa com que a velocidade do jogo aumenta
        self.speedup_scale = 1.2

        # A taxa com que os pontos de cada alien aumenta em cada nivel
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Configuracoes q mudam no decorrer do jogo'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # Fleet_direction = 1 -> Direita; Fleet_direction  = -1 -> Esquerda
        self.fleet_direction = 1

        # Pontuacao por alien
        self.alien_points = 50

    def increase_speed(self):
        '''Aumenta as configuracoes de velocidade e os pontos q cada alien fornece'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)