from .board import Board

class Game:
    """Класс для управления одной игрой в крестики-нолики"""
    
    def __init__(self, player_x, player_o, show=True):
        self.board = Board()
        self.player_x = player_x
        self.player_o = player_o
        self.player_x.set_symbol("X")
        self.player_o.set_symbol("O")
        
        # Сброс флагов перед игрой
        if hasattr(self.player_x, 'took_center'):
            self.player_x.took_center = False
        if hasattr(self.player_o, 'took_center'):
            self.player_o.took_center = False

        # Сброс блокировок перед КАЖДОЙ игрой
        self.player_x.blocked = 0
        self.player_o.blocked = 0
        
        self.current_player = self.player_x
        self.show = show

    def play_turn(self, board):
        """Ход игрока"""
        if self.show:
            board.display()
        
        position = self.current_player.make_move(self.board)

        opponent_symbol = 'O' if self.current_player.symbol == 'X' else 'X'

        # Отслеживание блокировки хода соперника
        if board.is_valid_move(position):
            board.board[position] = opponent_symbol
            if board.check_winner(opponent_symbol):
                self.current_player.blocked = getattr(self.current_player, 'blocked', 0) + 1
            board.board[position] = " "

        # Отслеживание взятия центра
        if position == 4:
            self.current_player.took_center = True
    
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