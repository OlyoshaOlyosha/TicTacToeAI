import random

from players.ai_bot import AIPlayer

class GeneticAlgorithm:
    """Класс для реализации генетического алгоритма"""

    def __init__(self, population_size, elite_pct, crossover_pct, random_pct, mutation_rate):
        self.population_size = population_size
        self.elite_pct = elite_pct
        self.crossover_pct = crossover_pct
        self.random_pct = random_pct
        self.mutation_rate = mutation_rate

    def crossover(self, parent1, parent2):
        """Создает потомка путем скрещивания двух родителей"""
        # Кроссовер для весов w1
        child_w1 = self._crossover_matrix(parent1.w1, parent2.w1)
        
        # Кроссовер для весов w2
        child_w2 = self._crossover_matrix(parent1.w2, parent2.w2)

        return AIPlayer(w1=child_w1, w2=child_w2)
    
    def _crossover_matrix(self, matrix1, matrix2):
        """Скрещивает две матрицы весов (блочный кроссовер)"""
        result_matrix = []
        crossover_point = random.randint(0, len(matrix1))
        for i in range(len(matrix1)):
            if i < crossover_point:
                result_matrix.append(matrix1[i][:])
            else:
                result_matrix.append(matrix2[i][:])
        return result_matrix

    def mutate_matrix(self, matrix, mutation_rate, delta=0.05):
        """Применяет мутации к матрице весов с заданной вероятностью"""
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if random.random() < mutation_rate:
                    matrix[i][j] += random.uniform(-delta, delta)
                    # Ограничиваем веса в диапазоне [-1, 1]
                    matrix[i][j] = max(-1, min(1, matrix[i][j]))
        return matrix

    def mutate(self, player, mutation_rate):
        """Мутирует веса нейронной сети игрока"""
        player.w1 = self.mutate_matrix(player.w1, mutation_rate)
        player.w2 = self.mutate_matrix(player.w2, mutation_rate)
        return player

    def next_generation(self, ranked_players):
        """Создает новое поколение игроков на основе рейтинга"""
        # Предвычисляем размеры
        elite_size = int(self.population_size * self.elite_pct)
        crossover_size = int(self.population_size * self.crossover_pct)
        random_size = int(self.population_size * self.random_pct)
        
        new_population = []
        
        # Элитные игроки
        new_population.extend(ranked_players[:elite_size])
        
        # Потомки от скрещивания
        for _ in range(crossover_size):
            p1, p2 = random.sample(ranked_players[:elite_size], 2)
            child = self.crossover(p1, p2)
            child = self.mutate(child, self.mutation_rate)
            new_population.append(child)
        
        # Случайные новые игроки
        for _ in range(random_size):
            new_population.append(AIPlayer())

        return new_population