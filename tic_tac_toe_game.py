import pretty_errors

class Player():
    """Класс игрока"""
    def __init__(self, symbol):
        self.symbol = symbol

class HumanPlayer(Player):
    """Класс человека"""
    def make_move(self, board):
        """Сделать ход"""
        position = int(input("Введите ваш ход (1-9): ")) - 1
        while not board.is_valid_move(position):
            print("Неверный ход. Попробуйте еще раз.")
            position = int(input("Введите ваш ход (1-9): ")) - 1
        return position

class RandomPlayer(Player):
    """Класс игрока через случайные ходы"""
    import random
    def make_move(self, board):
        """Сделать ход"""
        position = self.random.choice([i for i in range(9) if board.is_valid_move(i)])
        return position


class Board():
    """Класс доски"""
    def __init__(self):
        self.board = [" "] * 9

    def display(self):
        """Отобразить доску"""
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")

    def check_winner(self, current_player):
        """Проверка победителя"""
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтали
                (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикали
                (0, 4, 8), (2, 4, 6)]             # Диагонали
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] == current_player.symbol:
                return True
        return False
    
    def is_full(self):
        """Проверка на заполненность доски"""
        return " " not in self.board
    
    def is_valid_move(self, position):
        """Проверка, можно ли походить в клетку"""
        if self.board[position] == " ":
            return True
        
    def make_move(self, symbol, position):
        """Поставить символ игрока в указанную клетку"""
        self.board[position] = symbol

class Game():
    def __init__(self):
        self.board = Board()
        self.player_x = HumanPlayer("X")
        self.player_o = RandomPlayer("O")
        self.current_player = self.player_x

    def play_turn(self, board):
        """Ход игрока"""
        board.display()
        position = self.current_player.make_move(self.board)
        self.board.make_move(self.current_player.symbol, position)

    def switch_player(self):
        """Смена игрока"""
        if self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x
        
    def play(self):
        """Игровой цикл"""
        while True:
            # Ход игрока
            self.play_turn(self.board)
            
            # Проверка победителя или ничьи
            if self.board.check_winner(self.current_player):
                print(f"{self.current_player.symbol} победил!")
                break
            elif self.board.is_full():
                print("Ничья!")
                break
            
            # Смена игрока
            self.switch_player()


def start():
    """Запуск игры"""
    while True:
        game = Game()
        game.play()
        play_again = input("Хотите сыграть еще раз? (y/n): ")
        if play_again.lower() != "y":
            break

if __name__ == "__main__":
    start()
