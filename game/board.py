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
        
    def make_move(self, symbol, position):
        """Поставить символ игрока в указанную клетку"""
        self.board[position] = symbol