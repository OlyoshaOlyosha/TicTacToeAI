import pretty_errors

class Board():
    """"""
    
    def __init__(self):
        self.board = [" "] * 9

    def display(self):
        """Отобразить доску"""
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")

    def make_move(self, current_player, position):
        """Сделать ход"""
        self.board[position] = current_player

    def check_winner(self, current_player):
        """Проверка победителя"""
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Горизонтали
                (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Вертикали
                (0, 4, 8), (2, 4, 6)]             # Диагонали
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] == current_player:
                return True
        return False
    
    def is_full(self):
        """Проверка на заполненность доски"""
        return " " not in self.board
    
    def is_valid_move(self, position):
        """Проверка, можно ли походить в клетку"""
        if self.board[position] == " ":
            return True


class Game():
    def __init__(self):
        self.board = Board()
        self.current_player = "X"

    def play_turn(self, current_player, board):
        """Ход игрока"""
        board.display()
        position = int(input(f"{current_player}, введите ваш ход (1-9): ")) - 1
        while not board.is_valid_move(position):
            print("Неверный ход. Попробуйте еще раз.")
            position = int(input(f"{current_player}, введите ваш ход (1-9): ")) - 1
        board.make_move(current_player, position)

    def switch_player(self, current_player):
        """Смена игрока"""
        if current_player == "X":
            return "O"
        else:
            return "X"
        
    def play(self):
        """Игровой цикл"""
        while True:
            self.play_turn(self.current_player, self.board)
            
            if self.board.check_winner(self.current_player):
                print(f"{self.current_player} победил!")
                break
            elif self.board.is_full():
                print("Ничья!")
                break
            self.current_player = self.switch_player(self.current_player)

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
