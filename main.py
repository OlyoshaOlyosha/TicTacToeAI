import time
import json
import os
from datetime import datetime

from players import AIPlayer, HumanPlayer
from game import Game, TournamentManager, GeneticAlgorithm
from stats import Stats
from test_best_vs_random import test_best_vs_random
from config import  (
    POPULATION_SIZE, EPOCHS, ELITE_PCT, CROSSOVER_PCT, RANDOM_PCT, MUTATION_RATE,
    NUM_OPPONENTS_RATIO, SAVE_TOP, TEST_GAMES,
    WIN_SCORE, LOSS_SCORE, DRAW_SCORE, CENTER_BONUS, BLOCK_BONUS)

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

def save_experiment_results(summary_data, test_results):
    """Сохраняет результаты эксперимента в формате Markdown"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Подсчитываем номер эксперимента
    filename = "neural_network_tuning_log.md"
    experiment_num = 1
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            experiment_num = f.read().count("# ЭКСПЕРИМЕНТ") + 1
    
    # Формируем отчет в формате Markdown
    total_games = sum(test_results.values())
    win_pct = test_results["Wins"] / total_games * 100
    draw_pct = test_results["Draws"] / total_games * 100
    loss_pct = test_results["Losses"] / total_games * 100
    
    report = f"""
# ЭКСПЕРИМЕНТ №{experiment_num:03d}                                   
**Дата**: {timestamp}

## 🎯 РЕЗУЛЬТАТ vs RandomPlayer
**Победы**: {test_results["Wins"]} ({win_pct:.1f}%)  │  **Ничьи**: {test_results["Draws"]} ({draw_pct:.1f}%)  │  **Поражения**: {test_results["Losses"]} ({loss_pct:.1f}%)

## 📊 ОБУЧЕНИЕ
**Эпохи**: {summary_data["epochs_completed"]}  │  **Лучший результат**: {summary_data["best_score"]:.0f} очков  │  **Средний прогресс**: {summary_data["progress"]:.0f}  
**% Побед Лучшего**: {summary_data["final_win_rate"]:.1f}%  │  **Разнообразие**: {summary_data["avg_diversity"]:.3f}  │  **Стабильность**: {summary_data["recent_stability"]:.2f}


## ⚙️ Параметры для config.py

```python
# Параметры эволюции
POPULATION_SIZE = {POPULATION_SIZE}
EPOCHS = {EPOCHS}
ELITE_PCT = {ELITE_PCT}
CROSSOVER_PCT = {CROSSOVER_PCT}
RANDOM_PCT = {RANDOM_PCT}
MUTATION_RATE = {MUTATION_RATE}

# Параметры турнира
NUM_OPPONENTS_RATIO = {NUM_OPPONENTS_RATIO}

# Награда для подсчета очков
WIN_SCORE = {WIN_SCORE}
LOSS_SCORE = {LOSS_SCORE}
DRAW_SCORE = {DRAW_SCORE}
CENTER_BONUS = {CENTER_BONUS}
BLOCK_BONUS = {BLOCK_BONUS}
```

---

"""
    
    # Добавляем в общий файл
    with open(filename, "a", encoding="utf-8") as f:
        f.write(report)
    
    print(f"Результаты эксперимента добавлены в {filename}")

# ============================================================================
# Функции расчетов
# ============================================================================

def calculate_scores(results, population):
    """Вычисляет очки для каждого игрока"""
    return [WIN_SCORE * results[p]["Wins"] + 
            LOSS_SCORE * results[p]["Losses"] + 
            DRAW_SCORE * results[p]["Draws"] + 
            CENTER_BONUS * results[p].get("CenterBonus", 0) + 
            BLOCK_BONUS * results[p].get("BlockBonus", 0)
            for p in population]

def finish_training(ranked, stats):
    """Завершает обучение: сохраняет, тестирует и показывает статистику"""
    save_best(ranked[:SAVE_TOP])
    test_results = test_best_vs_random(ranked[0], n_games=TEST_GAMES)
    summary_data = stats.print_summary()

    # Сохраняем результаты эксперимента
    save_experiment_results(summary_data, test_results)

    stats.plot()
    stats.animate_weights()

# ============================================================================
# Основные функции
# ============================================================================

def run_evolution():
    """Запускает процесс эволюции и возвращает лучшего игрока"""
    
    start_time = time.time()
    best_prev = load_best()
    population = create_population(POPULATION_SIZE, best_prev)
    ga = GeneticAlgorithm(POPULATION_SIZE, ELITE_PCT, CROSSOVER_PCT, RANDOM_PCT, MUTATION_RATE)
    stats = Stats()

    # Предвычисляем константы
    num_opponents = int(POPULATION_SIZE * NUM_OPPONENTS_RATIO)

    completed_epochs = 0
    try:
        for epoch in range(EPOCHS):
            epoch_start = time.time()

            # Турнир
            tournament = TournamentManager(population, num_opponents=num_opponents)
            tournament.run()
            
            # Статистика
            ranked = tournament.ranked_players()
            scores = calculate_scores(tournament.results, population)

            first_result = tournament.results[ranked[0]]
            first_total = first_result["Wins"] + first_result["Losses"] + first_result["Draws"]
            if first_total > 0:
                first_win_pct = first_result["Wins"] / first_total * 100
                first_loss_pct = first_result["Losses"] / first_total * 100
                first_draw_pct = first_result["Draws"] / first_total * 100
            else:
                first_win_pct = first_loss_pct = first_draw_pct = 0

            epoch_time = time.time() - epoch_start
            
            print(f"Эпоха {epoch + 1}: "
                f"Лучший: {max(scores):.1f} "
                f"Средний: {sum(scores) / len(scores):.2f} "
                f"Процент W/L/D: {first_win_pct:.2f}/{first_loss_pct:.2f}/{first_draw_pct:.2f} "
                f"Время: {epoch_time:.3f}с")
            
            # Логирование
            wins = []
            losses = []
            draws = []
            for p in population:
                result = tournament.results[p]
                wins.append(result["Wins"])
                losses.append(result["Losses"])
                draws.append(result["Draws"])
            
            stats.log(wins, losses, draws, scores, population, tournament.results)
            
            # Новое поколение
            population = ga.next_generation(ranked)
            completed_epochs = epoch + 1
    
    except KeyboardInterrupt:
        print("\n\nОбучение остановлено пользователем!")
        print(f"Завершено эпох: {epoch + 1}")

    total_time = time.time() - start_time
    print(f"\nОбщее время обучения: {total_time:.3f}с")
    print(f"Среднее время на эпоху: {total_time / completed_epochs:.3f}с")
    
    # Сохранение и отображение результатов
    finish_training(ranked, stats)
    return ranked[0]

def play_with_human(best_ai):
    """Игровой цикл человек против ИИ"""
    play_game = input("Хотите сыграть против ИИ? (y/n): ")
    if play_game.lower() != "y":
        return

    try:
        from ui.gui_play import GUIPlay
        gui = GUIPlay(ai_player=best_ai)
        gui.start()
        return
    except Exception:
        pass

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