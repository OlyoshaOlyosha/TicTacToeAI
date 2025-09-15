from players import RandomPlayer
from game.match_manager import MatchManager

def test_best_vs_random(best_player, n_games=100):
    """Тестирует лучшего игрока против случайного игрока"""
    test_results = {"Wins": 0, "Losses": 0, "Draws": 0}

    for game_number in range(n_games):
        random_opponent = RandomPlayer()
        match = MatchManager(best_player, random_opponent, show=False)
        winner = match.run_match()
        
        if winner is None:
            test_results["Draws"] += 1
        elif winner == best_player.symbol:
            test_results["Wins"] += 1
        else:
            test_results["Losses"] += 1

    # Вывод результатов
    total_games = sum(test_results.values())
    print(f"\nТест против RandomPlayer ({n_games} игр):")
    print(f"Победы: {test_results['Wins']} "
          f"({test_results['Wins'] / total_games * 100:.1f}%)")
    print(f"Ничьи: {test_results['Draws']} "
          f"({test_results['Draws'] / total_games * 100:.1f}%)")
    print(f"Поражения: {test_results['Losses']} "
          f"({test_results['Losses'] / total_games * 100:.1f}%)")
    
    return test_results