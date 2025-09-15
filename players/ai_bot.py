import math
import random

from .base import Player

class AIPlayer(Player):
    """Класс нейросети игрока"""
    
    def __init__(self, w1=None, w2=None):
        super().__init__()
        self.took_center = False
        self.took_center_count = 0
        
        if w1 is None:
            # Веса вход-скрытый слой (10x18)
            self.w1 = [[random.uniform(-1, 1) for _ in range(18)] 
                       for _ in range(10)]
            # Веса скрытый-выходной слой (18x9)
            self.w2 = [[random.uniform(-1, 1) for _ in range(9)] 
                       for _ in range(18)]
        else:
            self.w1 = w1
            self.w2 = w2

    def make_move(self, board):
        """Делает ход на основе нейронной сети"""
        # Подготовка входных данных
        inputs = []
        for cell in board.board:
            if cell == 'X':
                inputs.append(1)
            elif cell == 'O':
                inputs.append(-1)
            else:
                inputs.append(0)
        inputs.append(1 if self.symbol == 'X' else -1)
        
        # Скрытый слой
        hidden = []
        for j in range(18):
            z = sum(inputs[i] * self.w1[i][j] for i in range(10))
            hidden.append(tanh(z))

        # Выходной слой
        outputs = []
        for j in range(9):
            score = sum(hidden[i] * self.w2[i][j] for i in range(18))
            outputs.append(score)

        # Выбираем только доступные ходы
        available = [i for i in range(9) if board.is_valid_move(i)]
        position = max(available, key=lambda i: outputs[i])

        # Отслеживаем взятие центра
        if position == 4:
            self.took_center = True
            self.took_center_count += 1

        return position

def tanh(x):
    """Функция активации tanh"""
    return math.tanh(x)