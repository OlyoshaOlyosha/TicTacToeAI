from .base import Player

class HumanPlayer(Player):
    """Класс человека игрока"""
    def make_move(self, board):
        position = int(input("Введите ваш ход (1-9): ")) - 1
        while not board.is_valid_move(position):
            print("Неверный ход. Попробуйте еще раз.")
            position = int(input("Введите ваш ход (1-9): ")) - 1
        return position