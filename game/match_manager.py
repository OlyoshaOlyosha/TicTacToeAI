from .game import Game

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