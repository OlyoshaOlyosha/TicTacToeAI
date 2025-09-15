import random

from .base import Player

class RandomPlayer(Player):
    """Класс игрока, делающего случайные ходы"""
    
    def make_move(self, board):
        """Выбирает случайный доступный ход"""
        available_positions = [i for i in range(9) if board.is_valid_move(i)]
        return random.choice(available_positions)