import pretty_errors

from players import HumanPlayer, RandomPlayer, AIPlayer
from game import MatchManager, Game

def start():
    """Запуск игры"""

    # Провести серию матчей между двумя игроками
    manager = MatchManager(RandomPlayer("X"), AIPlayer("O"), 100)
    manager.run_matches()

    # Игровой цикл для одного матча между человеком и ботом
    while True:
        game = Game(HumanPlayer("X"), AIPlayer("O"))
        winner = game.play()
        if winner is None:
            print("Ничья!")
        else:
            print(f"Победил игрок: {winner}")
        
        play_again = input("Хотите сыграть еще раз? (y/n): ")
        if play_again.lower() != "y":
            break


if __name__ == "__main__":
    start()
