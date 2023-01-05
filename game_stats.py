class GameStats:
    def __init__(self, aigame):
        self.settings = aigame.settings
        self.reset_stats()
        self.game_active = False
        #najlepszy wynik
        self.high_score = 0
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1