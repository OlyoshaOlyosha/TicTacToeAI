import random

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

        # Случайным образом назначаем символы игрокам
        players = [self.player_x, self.player_o]
        random.shuffle(players)  
        players[0].set_symbol("X")
        players[1].set_symbol("O")

        game = Game(players[0], players[1], show=self.show)
        winner = game.play()
        if winner == "X":
            self.scores["X"] += 1
        elif winner == "O":
            self.scores["O"] += 1
        else:
            self.scores["Draws"] += 1