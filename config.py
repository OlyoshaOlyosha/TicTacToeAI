"""Конфигурационные настройки проекта"""

# Параметры эволюции
POPULATION_SIZE = 100
EPOCHS = 50
ELITE_PCT = 0.3
CROSSOVER_PCT = 0.5
RANDOM_PCT = 0.2
MUTATION_RATE = 0.05

# Параметры турнира
NUM_OPPONENTS_RATIO = 0.2  # 20% от размера популяции

# Параметры сохранения и тестирования
SAVE_TOP = 20
SAVE_FILENAME = "best.json"
TEST_GAMES = 500

# Награда для подсчета очков
WIN_SCORE = 5
LOSS_SCORE = -3
DRAW_SCORE = 2
CENTER_BONUS = 15
BLOCK_BONUS = 15