from .match_manager import MatchManager

class TournamentManager:
    """Класс для управления турниром между множеством игроков"""
    def __init__(self, players):
        self.players = players
        self.results = {player: {"Wins": 0, "Losses": 0, "Draws": 0} for player in players}

    def run(self):
        """Запуск турнира: каждый играет с каждым"""
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                player_x = self.players[i]
                player_o = self.players[j]

                match = MatchManager(player_x, player_o, show=False)
                match.run_matches()

                # Обновление результатов
                self.results[self.players[i]]["Wins"] += match.scores["X"] if self.players[i].symbol == "X" else match.scores["O"]
                self.results[self.players[i]]["Losses"] += match.scores["O"] if self.players[i].symbol == "X" else match.scores["X"]
                self.results[self.players[i]]["Draws"] += match.scores["Draws"]

                self.results[self.players[j]]["Wins"] += match.scores["X"] if self.players[j].symbol == "X" else match.scores["O"]
                self.results[self.players[j]]["Losses"] += match.scores["O"] if self.players[j].symbol == "X" else match.scores["X"]
                self.results[self.players[j]]["Draws"] += match.scores["Draws"]

    def print_results(self):
        """Статистика итогов турнира"""
        tournament_total_games = sum(stats["Wins"] + stats["Losses"] + stats["Draws"] for stats in self.results.values()) // 2

        print("Счет:")
        print(f"Всего игр: {tournament_total_games}")

        for i, player in enumerate(self.players):
            stats = self.results[player]
            total_games = stats['Wins'] + stats['Losses'] + stats['Draws']
            print(f"\nИгрок {i + 1}:")
            print(f"Побед: {stats['Wins']}, Поражений: {stats['Losses']}, Ничьих: {stats['Draws']}")
            if total_games > 0:
                print(f"Процент побед: {stats['Wins'] / total_games * 100:.2f}%")
                print(f"Процент поражений: {stats['Losses'] / total_games * 100:.2f}%")
                print(f"Процент ничьих: {stats['Draws'] / total_games * 100:.2f}%")
