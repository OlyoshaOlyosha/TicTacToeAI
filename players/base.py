class Player():
    """Базовый класс игрока"""
    def __init__(self):
        self.symbol = None
        
    def set_symbol(self, symbol):
        self.symbol = symbol