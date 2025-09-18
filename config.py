"""Конфигурационные настройки проекта"""

# Параметры эволюции
POPULATION_SIZE = 100
EPOCHS = 500
ELITE_PCT = 0.3
CROSSOVER_PCT = 0.6
RANDOM_PCT = 0.1
MUTATION_RATE = 0.003

# Параметры турнира
NUM_OPPONENTS_RATIO = 0.2  # 20% от размера популяции

# Параметры сохранения и тестирования
SAVE_TOP = 20
SAVE_FILENAME = "best.json"
TEST_GAMES = 1000

# Награда для подсчета очков
WIN_SCORE = 100
LOSS_SCORE = -150
DRAW_SCORE = 50
CENTER_BONUS = 30
BLOCK_BONUS = 60