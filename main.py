import json
import pretty_errors

from players import AIPlayer, HumanPlayer
from game import Game, TournamentManager, GeneticAlgorithm
from stats import Stats
from test_best_vs_random import test_best_vs_random
from config import *

# ============================================================================
# Функции сохранения/загрузки
# ============================================================================

def save_best(players, filename="best.json"):
    """Сохранение лучших игроков в файл"""
    data = [{"w1": p.w1, "w2": p.w2} for p in players]
    with open(filename, "w") as f:
        json.dump(data, f)

def load_best(filename="best.json"):
    """Загрузка лучших игроков из файла"""
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        from players.ai_bot import AIPlayer
        return [AIPlayer(w1=item["w1"], w2=item["w2"])
                for item in data]
    except FileNotFoundError:
        return []

def create_population(population_size, best_prev):
    """Создает начальную популяцию"""
    if best_prev:
        new_players_count = population_size - len(best_prev)
        return [AIPlayer() for _ in range(new_players_count)] + best_prev
    else:
        return [AIPlayer() for _ in range(population_size)]

# ============================================================================
# Функции расчетов
# ============================================================================

def calculate_scores(results, population):
    """Вычисляет очки для каждого игрока"""
    return [
          WIN_SCORE    * results[p]["Wins"]
        + LOSS_SCORE   * results[p]["Losses"]
        + DRAW_SCORE   * results[p]["Draws"]
        + CENTER_BONUS * results[p].get("CenterBonus", 0)
        + BLOCK_BONUS  * getattr(p, 'blocked', 0)
        for p in population
    ]

def calculate_percentages(results, population):
    """Вычисляет процентное соотношение побед/поражений/ничьих"""
    wins_percent, losses_percent, draws_percent = [], [], []

    for player in population:
        total_games = (results[player]["Wins"] + 
                    results[player]["Losses"] + 
                    results[player]["Draws"])
        
        if total_games > 0:
            wins_percent.append(results[player]["Wins"] / total_games * 100)
            losses_percent.append(results[player]["Losses"] / total_games * 100)
            draws_percent.append(results[player]["Draws"] / total_games * 100)
        else:
            wins_percent.append(0)
            losses_percent.append(0)
            draws_percent.append(0)
    
    return wins_percent, losses_percent, draws_percent

# ============================================================================
# Основные функции
# ============================================================================

def run_evolution():
    """Запускает процесс эволюции и возвращает лучшего игрока"""
    best_prev = load_best()
    population = create_population(POPULATION_SIZE, best_prev)
    ga = GeneticAlgorithm(POPULATION_SIZE, ELITE_PCT, CROSSOVER_PCT, RANDOM_PCT, MUTATION_RATE)
    stats = Stats()

    for epoch in range(EPOCHS):
        # Турнир
        num_opponents = int(POPULATION_SIZE * NUM_OPPONENTS_RATIO)
        tournament = TournamentManager(population, num_opponents=num_opponents)
        tournament.run()
        
        # Статистика
        ranked = tournament.ranked_players()
        scores = calculate_scores(tournament.results, population)
        wins_percent, losses_percent, draws_percent = calculate_percentages(tournament.results, population)
        
        print(f"Эпоха {epoch + 1}: "
              f"Лучший: {max(scores):.1f} "
              f"Средний: {sum(scores) / len(scores):.2f} "
              f"Процент W/L/D: {wins_percent[0]:.2f}/{losses_percent[0]:.2f}/{draws_percent[0]:.2f}")
        
        # Логирование
        wins = [tournament.results[p]["Wins"] for p in population]
        losses = [tournament.results[p]["Losses"] for p in population]
        draws = [tournament.results[p]["Draws"] for p in population]
        stats.log(wins, losses, draws, scores, population)
        
        # Новое поколение
        population = ga.next_generation(ranked)
    
    # Сохранение и отображение результатов
    save_best(ranked[:SAVE_TOP])
    test_best_vs_random(ranked[0], n_games=TEST_GAMES)
    stats.plot(3)
    stats.animate_weights()
    
    return ranked[0]

def play_with_human(best_ai):
    """Игровой цикл человек против ИИ"""
    while True:
        game = Game(HumanPlayer(), best_ai, show=True)
        winner = game.play()
        
        if winner is None:
            print("Ничья!")
        else:
            print(f"Победил игрок: {winner}")
        
        play_again = input("Хотите сыграть еще раз? (y/n): ")
        if play_again.lower() != "y":
            break

def main():
    best_ai = run_evolution()
    play_with_human(best_ai)

if __name__ == "__main__":
    main()