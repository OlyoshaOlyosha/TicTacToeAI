import numpy as np
import random

from .base import Player

class AIPlayer(Player):
    """Класс нейросети игрока"""
    
    def __init__(self, w1=None, w2=None):
        super().__init__()
        self.took_center = False
        
        if w1 is None:
            # Веса вход-скрытый слой (10x20)
            self.w1 = [[random.uniform(-1, 1) for _ in range(20)] for _ in range(10)]
            # Веса скрытый-выходной слой (20x9)
            self.w2 = [[random.uniform(-1, 1) for _ in range(9)] for _ in range(20)]
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

    def predict_scores(self, board):
        """Вернуть сырые оценки (логиты) для каждой из 9 клеток.

        Возвращает список из 9 чисел (float). GUI использует это, чтобы показать
        относительные предпочтения. Метод не фильтрует доступность ходов — это
        делает GUI.
        """
        # Подготовка входных данных как в make_move
        inputs = np.array([1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in board.board] +
                          [1 if self.symbol == 'X' else -1])

        # Приведение весов к numpy-массивам на случай, если они хранятся как списки
        w1 = np.array(self.w1)
        w2 = np.array(self.w2)

        hidden = np.tanh(np.dot(inputs, w1))
        outputs = np.dot(hidden, w2)

        # Вернём простую list-структуру для удобства в GUI
        try:
            return list(map(float, outputs))
        except Exception:
            return [float(x) for x in outputs]