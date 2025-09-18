import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Stats:
    """Класс для сбора и отображения статистики эволюции"""

    def __init__(self):
        # Статистика лучшего игрока
        self.best_wins = []
        self.best_losses = []
        self.best_draws = []
        self.best_win_rates = []
        self.best_loss_rates = []
        self.best_draw_rates = []

        # Статистика очков популяции
        self.max_scores = []
        self.avg_scores = []
        self.min_scores = []
        self.std_scores = []
        self.top10_avg_scores = []
        self.population_wins = []
        self.population_losses = []

        # Специальная статистика
        self.center_counts = []
        self.block_counts = []
        self.population_diversity = []
        self.best_player_stability = []

        # История весов и совместимость
        self.w1_history = []
        self.w2_history = []
        self.win_rates = []

    def _calculate_diversity(self, population):
        """Вычисляет разнообразие популяции по весам"""
        if len(population) < 2:
            return 0
        
        weights = []
        for player in population:
            flat_weights = [w for row in player.w1[:5] for w in row[:5]]
            weights.append(flat_weights)
        
        return np.mean(np.std(np.array(weights), axis=0))

    def _calculate_stability(self, current_best, epoch):
        """
        Вычисляет скорость роста лучшего результата за последние 5 эпох.
        
        Возвращает разность между текущим и предыдущим результатом.
        Положительные значения = улучшение, отрицательные = ухудшение.
        """
        if len(self.max_scores) < 2:
            return 0
        
        # Простая разность между текущим и предыдущим результатом
        current_score = self.max_scores[-1]
        previous_score = self.max_scores[-2]
        
        return current_score - previous_score

    def log(self, wins, losses, draws, scores, population, tournament_results):
        """Записывает статистику текущей эпохи"""
        best_player_index = scores.index(max(scores))
        best_player = population[best_player_index]

        # Сохраняем веса и специальную статистику
        self.w1_history.append([row[:] for row in best_player.w1])
        self.w2_history.append([row[:] for row in best_player.w2])
        self.center_counts.append(tournament_results[best_player].get("CenterBonus", 0))
        self.block_counts.append(tournament_results[best_player].get("BlockBonus", 0))

        # Результаты лучшего игрока
        best_wins = wins[best_player_index]
        best_losses = losses[best_player_index]
        best_draws = draws[best_player_index]
        
        self.best_wins.append(best_wins)
        self.best_losses.append(best_losses)
        self.best_draws.append(best_draws)

        # Процентные данные лучшего игрока
        total_games = best_wins + best_losses + best_draws
        if total_games > 0:
            self.best_win_rates.append(best_wins / total_games)
            self.best_loss_rates.append(best_losses / total_games)
            self.best_draw_rates.append(best_draws / total_games)
        else:
            self.best_win_rates.extend([0, 0, 0])
            self.best_loss_rates.extend([0, 0, 0])
            self.best_draw_rates.extend([0, 0, 0])
        
        self.win_rates.append(self.best_win_rates[-1] * 100)

        # Статистика популяции
        self.max_scores.append(max(scores))
        self.avg_scores.append(np.mean(scores))
        self.min_scores.append(min(scores))
        self.std_scores.append(np.std(scores))
        self.top10_avg_scores.append(np.mean(sorted(scores, reverse=True)[:10]))
        self.population_wins.append(sum(wins))
        self.population_losses.append(sum(losses))

        # Метрики эволюции
        self.population_diversity.append(self._calculate_diversity(population))
        self.best_player_stability.append(self._calculate_stability(best_player, len(self.max_scores) - 1))

    def _moving_average(self, data, window=5):
        """Вычисляет скользящее среднее"""
        if len(data) < window:
            return data
        return [np.mean(data[max(0, i-window+1):i+1]) for i in range(len(data))]

    def _plot_raw_and_trend(self, ax, epochs, data, label, color, window=5):
        """Рисует сырые данные и тренд"""
        ax.plot(epochs, data, alpha=0.3, color=color)
        trend = self._moving_average(data, window)
        ax.plot(epochs, trend, label=f"{label} (тренд)", color=color, linewidth=2)
    
    def _setup_axis(self, ax, title, xlabel="Эпоха", ylabel=None):
        """Настраивает оси графика"""
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True)

    def plot(self):
        """Отображает расширенную статистику"""
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        epochs = list(range(1, len(self.max_scores) + 1))

        # Центрируем окно
        mngr = fig.canvas.manager
        mngr.window.wm_geometry("+200+100")
        
        # 1. Результаты лучшего игрока
        ax = axes[0, 0]
        self._plot_raw_and_trend(ax, epochs, self.best_win_rates, "% побед", 'green')
        self._plot_raw_and_trend(ax, epochs, self.best_loss_rates, "% поражений", 'red')
        self._plot_raw_and_trend(ax, epochs, self.best_draw_rates, "% ничьих", 'blue')
        ax.set_ylim(0, 1)
        self._setup_axis(ax, "Результаты лучшего игрока", ylabel="Процент результатов (0-1)")
        
        # 2. Разнообразие и стабильность
        ax = axes[0, 1]
        ax.plot(epochs, self.population_diversity, color='purple')
        ax.set_ylabel("Разнообразие весов", color='purple')
        ax.tick_params(axis='y', labelcolor='purple')
        ax.set_ylim(0, 1)

        ax_twin = ax.twinx()
        self._plot_raw_and_trend(ax_twin, epochs, self.best_player_stability, "Скорость роста", 'red')
        ax_twin.set_ylabel("Скорость роста", color='red')
        ax_twin.tick_params(axis='y', labelcolor='red')
        self._setup_axis(ax, "Разнообразие и стабильность")

        # 3. Распределение очков
        ax = axes[0, 2]
        ax.fill_between(epochs, self.min_scores, self.max_scores, alpha=0.3, label="Диапазон")
        ax.plot(epochs, self.max_scores, label="Максимум", color='green')
        ax.plot(epochs, self.avg_scores, label="Среднее", color='blue')
        ax.plot(epochs, self.top10_avg_scores, label="Топ-10", color='orange')
        self._setup_axis(ax, "Распределение очков", ylabel="Очки")

        # 4. Тренды обучения
        ax = axes[1, 0]
        max_trend = self._moving_average(self.max_scores, 10)
        avg_trend = self._moving_average(self.avg_scores, 10)
        ax.plot(epochs, max_trend, label="Тренд лучшего", color='green', linewidth=2)
        ax.plot(epochs, avg_trend, label="Тренд среднего", color='blue', linewidth=2)
        self._setup_axis(ax, "Тренды обучения", ylabel="Очки (сглаженные)")

        # 5. Вариативность результатов
        ax = axes[1, 1]
        self._plot_raw_and_trend(ax, epochs, self.std_scores, "Разброс очков", 'red')
        self._setup_axis(ax, "Вариативность результатов", ylabel="Стандартное отклонение")

        # 6. Стратегические метрики
        ax = axes[1, 2]
        self._plot_raw_and_trend(ax, epochs, self.center_counts, "Центр взят", 'red')
        self._plot_raw_and_trend(ax, epochs, self.block_counts, "Блокировки", 'blue')
        self._setup_axis(ax, "Стратегические метрики", ylabel="Количество раз")

        plt.tight_layout()
        plt.show()

    def print_summary(self):
        """Выводит сводку по обучению"""
        if not self.max_scores:
            return
            
        print("\n=== СВОДКА ПО ОБУЧЕНИЮ ===")
        print(f"Эпох завершено: {len(self.max_scores)}")
        print(f"Лучший результат: {max(self.max_scores):.1f} очков")
        print(f"Средний прогресс: {(self.max_scores[-1] - self.max_scores[0]):.1f} очков")
        print(f"Финальный % побед лучшего: {self.win_rates[-1]:.1f}%")
        print(f"Среднее разнообразие: {np.mean(self.population_diversity):.3f}")
        
        recent_stability = np.mean(self.best_player_stability[-10:]) if len(self.best_player_stability) >= 10 else np.mean(self.best_player_stability)
        print(f"Стабильность (последние эпохи): {recent_stability:.2f}")

    def animate_weights(self):
        """Создает анимацию изменения весов лучшего игрока по эпохам"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Центрируем окно анимации
        mngr = fig.canvas.manager
        mngr.window.wm_geometry("+450+300")

        def update_frame(epoch_index):
            ax1.clear()
            ax2.clear()
            
            # W1: 10 строк (скрытые нейроны) x 18 столбцов (входные нейроны)
            ax1.imshow(self.w1_history[epoch_index], cmap='RdBu', vmin=-1, vmax=1)
            ax1.set_title(f'Эпоха {epoch_index + 1} - Веса W1')
            ax1.set_xlabel('Скрытые нейроны (1-18)')
            ax1.set_ylabel('Входные нейроны (1-10)')
            ax1.set_xticks(range(18))
            ax1.set_xticklabels(range(1, 19))
            ax1.set_yticks(range(10))
            ax1.set_yticklabels(range(1, 11))
            
            # W2: 18 строк (скрытые нейроны) x 9 столбцов (выходные нейроны)
            ax2.imshow(self.w2_history[epoch_index], cmap='RdBu', vmin=-1, vmax=1).set_aspect('equal')
            ax2.set_title(f'Эпоха {epoch_index + 1} - Веса W2')
            ax2.set_xlabel('Выходные нейроны (1-8)')
            ax2.set_ylabel('Скрытые нейроны (1-18)')
            ax2.set_xticks(range(9))
            ax2.set_xticklabels(range(1, 10))
            ax2.set_yticks(range(18))
            ax2.set_yticklabels(range(1, 19))

        animation = FuncAnimation(
            fig, update_frame, 
            frames=len(self.w1_history), 
            interval=50, 
            repeat=True
        )
        plt.show()
        return animation