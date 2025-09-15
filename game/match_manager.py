import random

from .game import Game

class MatchManager:
    """Класс для управления отдельными матчами между двумя игроками"""

    def __init__(self, player_a, player_b, show=True):
        self.player_a = player_a
        self.player_b = player_b
        self.show = show

    def run_match(self):
        """Запускает матч между игроками"""
        # Случайным образом назначаем символы игрокам
        players = [self.player_a, self.player_b]
        random.shuffle(players)
        
        player_x = players[0]
        player_o = players[1]
        
        player_x.set_symbol("X")
        player_o.set_symbol("O")

        # Запускаем игру
        game = Game(player_x, player_o, show=self.show)
        winner_symbol = game.play()
        
        return winner_symbol