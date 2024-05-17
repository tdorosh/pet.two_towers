from game.deck import DeckFromFileInitializer
from game.interface import GraphicalInterface
from game.game import Game, GameSettings
from game.player import Player


def main():
    game = Game(
        interface=GraphicalInterface(),
        settings=GameSettings(),
        deck_initializer=DeckFromFileInitializer(),
        first_player=Player("Player 1"),
        second_player=Player("Player 2"),
    )
    game.run()


if __name__ == "__main__":
    main()
