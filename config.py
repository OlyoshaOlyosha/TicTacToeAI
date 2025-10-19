"""Конфигурационные настройки проекта"""

# Параметры эволюции
POPULATION_SIZE = 30
EPOCHS = 100
ELITE_PCT = 0.2
CROSSOVER_PCT = 0.8
RANDOM_PCT = 0.0
MUTATION_RATE = 0.05

# Параметры турнира
NUM_OPPONENTS_RATIO = 0.5

# Параметры сохранения и тестирования
SAVE_TOP = 30
SAVE_FILENAME = "best.json"
TEST_GAMES = 1000

# Награда для подсчета очков
WIN_SCORE = 60
LOSS_SCORE = -50
DRAW_SCORE = 40
CENTER_BONUS = 20
BLOCK_BONUS = 30