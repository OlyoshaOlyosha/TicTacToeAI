from .board import Board

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