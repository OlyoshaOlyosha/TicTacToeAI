import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Stats:
    """Класс для сбора и отображения статистики эволюции"""

    def __init__(self):
        # Статистика лучшего игрока
        self.best_wins = []
        self.best_losses = []
        self.best_draws = []

        # Статистика очков популяции
        self.max_scores = []
        self.avg_scores = []
        self.min_scores = []

        # Специальная статистика
        self.center_counts = []

        # История весов лучшего игрока
        self.w1_history = []  # Матрицы 10x18
        self.w2_history = []  # Матрицы 18x9


    def log(self, wins, losses, draws, scores, population):
        """Записывает статистику текущей эпохи"""
        # Находим лучшего игрока по максимальному счету
        best_player_index = scores.index(max(scores))
        best_player = population[best_player_index]

        # Сохраняем копии весов лучшего игрока
        self.w1_history.append([row[:] for row in best_player.w1])
        self.w2_history.append([row[:] for row in best_player.w2])

        # Статистика лучшего игрока
        self.center_counts.append(best_player.took_center_count)
        self.best_wins.append(wins[best_player_index])
        self.best_losses.append(losses[best_player_index])
        self.best_draws.append(draws[best_player_index])

        # Статистика по очкам всей популяции
        self.max_scores.append(max(scores))
        self.avg_scores.append(sum(scores) / len(scores))
        self.min_scores.append(min(scores))

    def _group_data(self, data, group_size):
        """Группирует данные и возвращает средние значения по группам"""
        return [sum(data[i:i + group_size]) / len(data[i:i + group_size]) 
                for i in range(0, len(data), group_size)]

    def plot(self, group_size=5):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        # Группируем данные
        grouped_wins = self._group_data(self.best_wins, group_size)
        grouped_losses = self._group_data(self.best_losses, group_size)
        grouped_draws = self._group_data(self.best_draws, group_size)
        grouped_max_scores = self._group_data(self.max_scores, group_size)
        grouped_avg_scores = self._group_data(self.avg_scores, group_size)
        grouped_min_scores = self._group_data(self.min_scores, group_size)
        grouped_center = self._group_data(self.center_counts, group_size)
        
        epochs = [(i + 1) * group_size for i in range(len(grouped_wins))]
            
        # Победы/поражения/ничьи
        ax1.plot(epochs, grouped_wins, label="Победы лучшего", marker='o')
        ax1.plot(epochs, grouped_losses, label="Поражения лучшего", marker='s')
        ax1.plot(epochs, grouped_draws, label="Ничьи лучшего", marker='^')
        ax1.set_xlabel("Эпоха")
        ax1.set_ylabel("Количество")
        ax1.set_xticks(epochs)
        ax1.legend()
        ax1.grid(True)
        ax1.set_title("Результаты лучшего игрока")
        
        # Очки
        ax2.plot(epochs, grouped_max_scores, label="Максимальный", marker='o')
        ax2.plot(epochs, grouped_avg_scores, label="Средний", marker='s')
        ax2.plot(epochs, grouped_min_scores, label="Минимальный", marker='^')
        ax2.set_xlabel("Эпоха")
        ax2.set_ylabel("Очки")
        ax2.set_xticks(epochs)
        ax2.legend()
        ax2.grid(True)
        ax2.set_title("Статистика по очкам")

        # Статистика взятия центра лучшим игроком
        ax3.plot(epochs, grouped_center, label="Центр взят лучшим", marker='x', color='red')
        ax3.set_xlabel("Эпоха")
        ax3.set_ylabel("Количество")
        ax3.set_xticks(epochs)
        ax3.legend()
        ax3.grid(True)
        ax3.set_title("Статистика центра")
            
        plt.tight_layout()
        plt.show()
    
    def animate_weights(self):
        """Создает анимацию изменения весов лучшего игрока по эпохам"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        def update_frame(epoch_index):
            """Обновляет кадр анимации для указанной эпохи"""
            ax1.clear()
            ax2.clear()
            
            # Отображение весов первого слоя
            ax1.imshow(self.w1_history[epoch_index], cmap='gray', vmin=-1, vmax=1)
            ax1.set_title(f'Эпоха {epoch_index + 1} - Веса w1 (10x18)')
            
            # Отображение весов второго слоя
            ax2.imshow(self.w2_history[epoch_index], cmap='gray', vmin=-1, vmax=1)
            ax2.set_title(f'Эпоха {epoch_index + 1} - Веса w2 (18x9)')

        animation = FuncAnimation(
            fig, update_frame, 
            frames=len(self.w1_history), 
            interval=25, 
            repeat=True
        )
        plt.show()
        return animation