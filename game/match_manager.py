import random

from .game import Game

class MatchManager():
    """Класс для управления матчами"""
    def __init__(self, player_a, player_b, show=True):
        self.player_a = player_a
        self.player_b = player_b
        self.show = show

    def run_match(self):
        """Запуск матча"""
        # Случайным образом назначаем символы игрокам
        players = [self.player_a, self.player_b]
        random.shuffle(players)  
        players[0].set_symbol("X")
        players[1].set_symbol("O")

        game = Game(players[0], players[1], show=self.show)
        winner = game.play()
        return winner