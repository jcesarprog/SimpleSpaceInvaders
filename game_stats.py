class GameStats():
    '''Armazena os dados do jogo'''

    def __init__(self, ai_settings):
        '''Inicializa os dados estatisticos do jogo'''
        self.ai_settings = ai_settings
        self.reset_stats()

        # A pontuacao maxima jamais devera ser reiniciada
        self.high_score = 0

        # Inicia o jogo com status inativo
        self.game_active = False

    def reset_stats(self):
        '''Inicializa os dados que podem mudar durante o jogo'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
