from types import MappingProxyType

from game.card import Card
from game.enums import PlayerCardAction
from game.helpers import is_player_action_allowed, can_card_be_applied, get_resource_subtype
from game.player import Player
from game.resource import ResourceType


class CommandLineInterface:

    PLAYER_CARD_ACTION_MAPPING = MappingProxyType(
        {
            "a": PlayerCardAction.APPLY,
            "d": PlayerCardAction.DISCARD,
        }
    )

    def __init__(self):
        self._current_player = None
        self._opponent_player = None

    def set_players(self, first_player: Player, second_player: Player):
        self._current_player = first_player
        self._opponent_player = second_player

    def show_current_state(self):
        self._show_player_resources(self._current_player)
        self._show_player_resources(self._opponent_player)
        self._show_player_cards(self._current_player)

    @staticmethod
    def get_player_card(player: Player):
        try:
            player_input = int(input("Choose card number: "))
            card = player.get_card_by_index(player_input - 1)
            print(f"Chosen card: {card}")
            return card
        except (IndexError, ValueError):
            return None

    @staticmethod
    def get_player_card_action():
        try:
            player_input = input("Choose 'a' for apply. Choose 'd' for discard: ")
            action = CommandLineInterface.PLAYER_CARD_ACTION_MAPPING[player_input]
            print(f"Chosen action: {action}")
            return action
        except KeyError:
            return None

    @staticmethod
    def is_player_input_valid(
        player: Player,
        card: Card,
        action: PlayerCardAction,
        permitted_actions: list[PlayerCardAction],
    ):
        if card is None:
            print("Chosen card number is incorrect.")
            return False
        if action is None:
            print("Choose 'Apply' or 'Discard'")
            return False
        if not is_player_action_allowed(permitted_actions, action):
            print("Action is not allowed.")
            return False
        if action == PlayerCardAction.APPLY and not can_card_be_applied(card, player):
            print("This card cannot be applied.")
            return False

        return True

    @staticmethod
    def _show_player_resources(player: Player):
        print(f"{player.name} resources: ")
        print(f"\tTower: {player.get_resource_by_type(ResourceType.TOWER).value}")
        print(f"\tWall: {player.get_resource_by_type(ResourceType.WALL).value}")
        print(f"\tMine: {player.get_resource_by_type(ResourceType.MINE).value}")
        print(f"\t\tOre: {player.get_resource_by_type(ResourceType.ORE).value}")
        print(f"\tMonastery: {player.get_resource_by_type(ResourceType.MONASTERY).value}")
        print(f"\t\tMana: {player.get_resource_by_type(ResourceType.MANA).value}")
        print(f"\tBarracks: {player.get_resource_by_type(ResourceType.BARRACKS).value}")
        print(f"\t\tSquads: {player.get_resource_by_type(ResourceType.SQUADS).value}")
        print()

    @staticmethod
    def _show_player_cards(player: Player):
        print(f"{player.name} cards: ")
        for index, card in enumerate(player.cards, start=1):
            print(f"Number: {index}")
            print(f"Resource type: {card.resource_type}")
            print(f"Title: {card.title}")
            print(f"Description: {card.description}")
            print(f"Price: {card.price}")
            print(f"Can be applied: {can_card_be_applied(card, player)}")
            print()

    def show_current_player(self):
        print(f"It's the {self._current_player.name}'s turn")

    @staticmethod
    def show_game_over_message(player: Player):
        print(f"{player.name} won.")

    @staticmethod
    def show_game_error_message(exception: Exception):
        print(f"Error was occurred: {exception}")
