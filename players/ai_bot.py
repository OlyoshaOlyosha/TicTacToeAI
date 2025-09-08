import random

from .base import Player

class AIPlayer(Player):
    """Класс нейросети игрока"""
    def __init__(self):
        self.weight = [random.random() for _ in range(9)]

    def make_move(self, board):
        available = [i for i in range(9) if board.is_valid_move(i)] # Список доступных ходов
        position = max(available, key=lambda i: self.weight[i]) # Выбор хода с максимальным весом
        
        return position