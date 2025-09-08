import pretty_errors

from players import HumanPlayer, RandomPlayer, AIPlayer
from game import Game, TournamentManager

def start():
    """Запуск игры"""
    # Турнир между AI ботами
    players = [AIPlayer() for _ in range(10)]

    tournament = TournamentManager(players)
    tournament.run()
    tournament.print_results()

    # Игровой цикл для одного матча между человеком и нейросетью
    while True:
        game = Game(HumanPlayer(), AIPlayer(), show=True)
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