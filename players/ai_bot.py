import numpy as np
import random

from .base import Player

class AIPlayer(Player):
    """Класс нейросети игрока"""
    
    def __init__(self, w1=None, w2=None):
        super().__init__()
        self.took_center = False
        
        if w1 is None:
            # Веса вход-скрытый слой (10x9)
            self.w1 = [[random.uniform(-1, 1) for _ in range(9)] for _ in range(10)]
            # Веса скрытый-выходной слой (9x9)
            self.w2 = [[random.uniform(-1, 1) for _ in range(9)] for _ in range(9)]
        else:
            self.w1 = w1
            self.w2 = w2

    def make_move(self, board):
        """Делает ход на основе нейронной сети"""
        # Подготовка входных данных
        inputs = np.array([1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in board.board] + 
                          [1 if self.symbol == 'X' else -1])
        
        # Скрытый слой
        hidden = np.tanh(np.dot(inputs, self.w1))

        # Выходной слой
        outputs = np.dot(hidden, self.w2)

        # Выбираем только доступные ходы
        available = [i for i in range(9) if board.is_valid_move(i)]
        return max(available, key=lambda i: outputs[i])