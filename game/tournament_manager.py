from .match_manager import MatchManager

class TournamentManager:
    """Класс для управления турниром между множеством игроков"""
    def __init__(self, players):
        self.players = players
        self.results = {p: {"Wins": 0, "Losses": 0, "Draws": 0} for p in players}

    def run(self):
        """Запуск турнира: каждый играет с каждым"""
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                match = MatchManager(self.players[i], self.players[j], show=False)
                winner = match.run_match()

                # Обновление результатов
                if winner is None:
                    self.results[self.players[i]]["Draws"] += 1
                    self.results[self.players[j]]["Draws"] += 1
                elif winner == self.players[i]:
                    self.results[self.players[i]]["Wins"] += 1
                    self.results[self.players[j]]["Losses"] += 1
                else:
                    self.results[self.players[j]]["Wins"] += 1
                    self.results[self.players[i]]["Losses"] += 1

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
                print(f"Набрано очков: {stats['Wins'] * 1 + stats['Draws'] * 0.5}")