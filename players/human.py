from .base import Player

class HumanPlayer(Player):
    """Класс игрока-человека"""
    
    def make_move(self, board):
        """Запрашивает ход у пользователя"""
        while True:
            try:
                user_input = input("Введите ваш ход (1-9): ")
                position = int(user_input) - 1
                
                if 0 <= position <= 8 and board.is_valid_move(position):
                    return position
                else:
                    print("Неверный ход. Выберите свободную клетку от 1 до 9.")
                    
            except ValueError:
                print("Пожалуйста, введите число от 1 до 9.")