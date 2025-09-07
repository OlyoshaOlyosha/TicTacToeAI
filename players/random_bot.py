import random

from .base import Player

class RandomPlayer(Player):
    """Класс компьютера игрока через случайные ходы"""
    def make_move(self, board):
        position = random.choice([i for i in range(9) if board.is_valid_move(i)])
        return position