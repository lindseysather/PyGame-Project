class GameStats:
    '''Track statistics for Alien Invasion'''

    def __init__(self, ai_game):
        '''Initialize statistics'''
        self.settings = ai_game.settings
        self.reset_stats()

        #Start alien invasion in an active state
        self.game_active = False

        #High score should never be reset - why we initialize it in __init__ rather than in reset_stats
        self.high_score = 0

    #to reset statistics each time the player starts a new game
    def reset_stats(self):
        '''Initialize statistics that can change during the game'''
        self.ships_left = self.settings.ship_limit
        self.score = 10000
        self.level = 1