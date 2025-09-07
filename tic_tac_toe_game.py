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

class Game():
    def __init__(self, player_x, player_o):
        self.board = Board()
        self.player_x = player_x
        self.player_o = player_o
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
            if self.board.check_winner(self.current_player.symbol):
                return self.current_player.symbol
            elif self.board.is_full():
                return None
            
            # Смена игрока
            self.switch_player()


class MatchManager():
    """Класс для управления матчами"""
    def __init__(self, player_x, player_o, num_games):
        self.player_x = player_x
        self.player_o = player_o
        self.num_games = num_games
        self.scores = {"X": 0, "O": 0, "Draws": 0}

    def run_matches(self):
        """Запуск серии матчей"""
        for _ in range(self.num_games):
            game = Game(self.player_x, self.player_o)
            winner = game.play()
            if winner == "X":
                self.scores["X"] += 1
            elif winner == "O":
                self.scores["O"] += 1
            else:
                self.scores["Draws"] += 1
        self.print_stats()

    def print_stats(self):
        """Отображение статистики"""
        print(f"Всего игр: {self.num_games}")
        print("Счет:")
        print(f"X: {self.scores['X']}, O: {self.scores['O']}, Ничьи: {self.scores['Draws']}")
        print(f"Процент побед X: {self.scores['X'] / self.num_games * 100:.2f}%")
        print(f"Процент побед O: {self.scores['O'] / self.num_games * 100:.2f}%")
        print(f"Процент ничьих: {self.scores['Draws'] / self.num_games * 100:.2f}%")


def start():
    """Запуск игры"""

    # Провести серию матчей между двумя игроками
    manager = MatchManager(RandomPlayer("X"), RandomPlayer("O"), 100)
    manager.run_matches()

    # Игровой цикл для одного матча между человеком и ботом
    # while True:
    #     game = Game(RandomPlayer("X"), RandomPlayer("O"))
    #     game.play()
    #     play_again = input("Хотите сыграть еще раз? (y/n): ")
    #     if play_again.lower() != "y":
    #         break

if __name__ == "__main__":
    start()
