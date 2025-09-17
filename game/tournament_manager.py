import random
from .match_manager import MatchManager
from config import WIN_SCORE, LOSS_SCORE, DRAW_SCORE, CENTER_BONUS, BLOCK_BONUS

class TournamentManager:
    """Класс для управления турниром между множеством игроков"""

    def __init__(self, players, num_opponents=None):
        self.players = players
        self.results = {p: {"Wins": 0, "Losses": 0, "Draws": 0} for p in players}
        self.num_opponents = num_opponents

    def run(self):
        """Запуск турнира"""
        if self.num_opponents is None:
            # Классический "каждый с каждым"
            self._run_round_robin()
        else:
            # Каждый с N случайными соперниками
            self._run_random_opponents()

    def _run_round_robin(self):
        """Турнир каждый с каждым"""
        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                self._play_match(self.players[i], self.players[j])

    def _run_random_opponents(self):
        """Турнир с случайными соперниками"""
        players_count = len(self.players)
    
        for current_player_index, current_player in enumerate(self.players):
            # Создаем список индексов вместо копирования игроков
            other_indices = list(range(current_player_index)) + list(range(current_player_index + 1, players_count))
            
            # Выбираем случайные индексы
            opponent_indices = random.sample(
                other_indices,
                min(self.num_opponents, len(other_indices))
            )
            
            # Играем матчи
            for opponent_index in opponent_indices:
                self._play_match(current_player, self.players[opponent_index])

    def _process_bonuses(self, player1, player2):
        """Обрабатывает бонусы за центр и блокировки"""
        for player in (player1, player2):
            # Бонус за центр
            if getattr(player, "took_center", False):
                if "CenterBonus" not in self.results[player]:
                    self.results[player]["CenterBonus"] = 0
                self.results[player]["CenterBonus"] += 1
                player.took_center = False

            # Бонус за блокировки
            blocked_count = getattr(player, "blocked", 0)
            if blocked_count > 0:
                if "BlockBonus" not in self.results[player]:
                    self.results[player]["BlockBonus"] = 0
                self.results[player]["BlockBonus"] += blocked_count
            player.blocked = 0

    def _play_match(self, player1, player2):
        """Проводит матч и обновляет результаты"""
        match = MatchManager(player1, player2, show=False)
        winner = match.run_match()

        if winner is None:
            self.results[player1]["Draws"] += 1
            self.results[player2]["Draws"] += 1
        elif winner == player1:
            self.results[player1]["Wins"] += 1
            self.results[player2]["Losses"] += 1
        else:
            self.results[player2]["Wins"] += 1
            self.results[player1]["Losses"] += 1

        # Обработка бонусов
        self._process_bonuses(player1, player2)

    def ranked_players(self):
        """Отсортированный список игроков по очкам"""
        def score(p):
            return (
                WIN_SCORE * self.results[p]["Wins"] + 
                LOSS_SCORE * self.results[p]["Losses"] + 
                DRAW_SCORE * self.results[p]["Draws"] + 
                CENTER_BONUS * self.results[p].get("CenterBonus", 0) + 
                BLOCK_BONUS * self.results[p].get("BlockBonus", 0)
            )
        return sorted(self.players, key=score, reverse=True)

    def print_results(self):
        """Статистика итогов турнира"""
        total_tournament_games = sum(
            player_stats["Wins"] + player_stats["Losses"] + player_stats["Draws"] 
            for player_stats in self.results.values()
        ) // 2

        print("Счет:")
        print(f"Всего игр: {total_tournament_games}")

        for player_index, player in enumerate(self.players):
            player_stats = self.results[player]
            total_player_games = player_stats['Wins'] + player_stats['Losses'] + player_stats['Draws']
            
            print(f"\nИгрок {player_index + 1}:")
            print(f"Побед: {player_stats['Wins']}, "
                f"Поражений: {player_stats['Losses']}, "
                f"Ничьих: {player_stats['Draws']}")
            
            if total_player_games > 0:
                win_percentage = player_stats['Wins'] / total_player_games * 100
                loss_percentage = player_stats['Losses'] / total_player_games * 100
                draw_percentage = player_stats['Draws'] / total_player_games * 100
                total_points = player_stats['Wins'] * 1 + player_stats['Draws'] * 0.5
                
                print(f"Процент побед: {win_percentage:.2f}%")
                print(f"Процент поражений: {loss_percentage:.2f}%")
                print(f"Процент ничьих: {draw_percentage:.2f}%")
                print(f"Набрано очков: {total_points}")