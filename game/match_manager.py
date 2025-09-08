from .game import Game

class MatchManager():
    """Класс для управления матчами"""
    def __init__(self, player_x, player_o, show=True):
        self.player_x = player_x
        self.player_o = player_o
        self.show = show
        self.scores = {"X": 0, "O": 0, "Draws": 0}

    def run_matches(self):
        """Запуск матча"""
        game = Game(self.player_x, self.player_o, show=self.show)
        winner = game.play()
        if winner == "X":
            self.scores["X"] += 1
        elif winner == "O":
            self.scores["O"] += 1
        else:
            self.scores["Draws"] += 1