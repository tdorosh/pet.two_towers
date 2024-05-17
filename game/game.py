from dataclasses import dataclass
from typing import Optional

from .card import Card, CardImpact, CardImpactCondition
from .constants import *
from .deck import Deck, DeckFromFileInitializer
from .enums import *
from .interface import CommandLineInterface, GraphicalInterface
from .helpers import get_resource_subtype
from .player import Player
from .resource import Resource


@dataclass(frozen=True)
class GameSettings:

    player_card_count: int = DEFAULT_PLAYER_CARD_COUNT
    initial_tower_value: int = DEFAULT_INITIAL_TOWER_VALUE
    initial_wall_value: int = DEFAULT_INITIAL_WALL_VALUE
    initial_main_resource_value: int = DEFAULT_INITIAL_MAIN_RESOURCE_VALUE
    initial_secondary_resource_value: int = DEFAULT_INITIAL_SECONDARY_RESOURCE_VALUE
    resource_boundary_values: frozenset[ResourceBoundaryValue] = DEFAULT_RESOURCE_BOUNDARY_VALUES


class GameInitializer:

    def __init__(
        self,
        *,
        settings: GameSettings,
        deck: Deck,
        deck_initializer: DeckFromFileInitializer,
        first_player: Player,
        second_player: Player,
    ):
        self._settings = settings
        self._deck = deck
        self._deck_initializer = deck_initializer
        self._first_player = first_player
        self._second_player = second_player

    def initialize(self):
        self._initialize_deck()
        self._initialize_player_cards(self._first_player)
        self._initialize_player_cards(self._second_player)
        self._initializer_player_resources(self._first_player, is_first_player=True)
        self._initializer_player_resources(self._second_player, is_first_player=False)

    def _initialize_deck(self):
        self._deck_initializer.initialize(self._deck)
        self._deck.shuffle()

    def _initialize_player_cards(self, player: Player):
        cards = []
        for _ in range(self._settings.player_card_count):
            cards.append(self._deck.get())
        player.cards = cards

    def _initializer_player_resources(self, player: Player, *, is_first_player: bool):
        secondary_resource_value = (
            self._settings.initial_secondary_resource_value + self._settings.initial_main_resource_value
            if is_first_player
            else self._settings.initial_secondary_resource_value
        )
        player.resources = [
            Resource(ResourceType.MINE, self._settings.initial_main_resource_value),
            Resource(ResourceType.MONASTERY, self._settings.initial_main_resource_value),
            Resource(ResourceType.BARRACKS, self._settings.initial_main_resource_value),
            Resource(ResourceType.ORE, secondary_resource_value),
            Resource(ResourceType.MANA, secondary_resource_value),
            Resource(ResourceType.SQUADS, secondary_resource_value),
            Resource(ResourceType.TOWER, self._settings.initial_tower_value),
            Resource(ResourceType.WALL, self._settings.initial_wall_value),
        ]


class Game:

    def __init__(
        self,
        *,
        interface: CommandLineInterface | GraphicalInterface,
        settings: GameSettings,
        deck_initializer: DeckFromFileInitializer,
        first_player: Player,
        second_player: Player,
    ):
        self._interface = interface
        self._settings = settings
        self._deck_initializer = deck_initializer
        self._first_player = first_player
        self._second_player = second_player
        self._deck = Deck()
        self._is_current_player_move_completed = False
        self._is_current_player_action_completed = False
        self._current_player: Player

    def run(self):
        try:
            self._initialize()
            while not self._is_over():
                self._handle_player_move()
            self._interface.show_game_over_message(self._get_winner_player())
        except Exception as exception:
            self._interface.show_game_error_message(exception)

    def _initialize(self):
        initializer = GameInitializer(
            settings=self._settings,
            deck=self._deck,
            deck_initializer=self._deck_initializer,
            first_player=self._first_player,
            second_player=self._second_player,
        )
        initializer.initialize()
        self._current_player = self._first_player
        self._interface.set_players(self._current_player, self._get_opponent_to(self._current_player))

    def _handle_player_move(self):
        while True:
            self._handle_player_action(PlayerCardAction.all_actions())
            if self._is_current_player_move_completed:
                self._apply_move()
                break

    def _handle_player_action(self, permitted_actions: list[PlayerCardAction]):
        self._is_current_player_action_completed = False
        self._is_current_player_move_completed = False

        while not self._is_current_player_action_completed:
            self._interface.show_current_state()
            self._interface.show_current_player()
            card = self._interface.get_player_card(self._current_player)
            action = self._interface.get_player_card_action()
            if self._interface.is_player_input_valid(self._current_player, card, action, permitted_actions):
                match action:
                    case PlayerCardAction.APPLY:
                        self._apply_card(card)
                        self._apply_action(card)
                        if self._is_over():
                            break
                        self._handle_card_additional_features(card)
                    case PlayerCardAction.DISCARD:
                        self._apply_action(card)

    def _apply_action(self, card: Card):
        self._deck.put_underneath(card)
        self._current_player.add_card(self._deck.get(), self._current_player.get_card_index(card))
        self._is_current_player_action_completed = True
        self._is_current_player_move_completed = True

    def _apply_card(self, card: Card):
        Game._decrease_player_secondary_resources(self._current_player, card)
        card_applier = PlayerCardApplier(self._current_player, self._get_opponent_to(self._current_player))
        card_applier.apply_card(card)

    def _handle_card_additional_features(self, card: Card):
        if card.has_additional_feature(CardAdditionalFeature.DISCARD_AND_PLAY_AGAIN):
            self._handle_player_action(PlayerCardAction.discard_actions())
            self._handle_player_action(PlayerCardAction.all_actions())
        elif card.has_additional_feature(CardAdditionalFeature.PLAY_AGAIN):
            self._handle_player_action(PlayerCardAction.all_actions())

    def _apply_move(self):
        Game._increase_player_secondary_resources(self._get_opponent_to(self._current_player))
        self._current_player = self._get_opponent_to(self._current_player)
        self._interface.set_players(self._current_player, self._get_opponent_to(self._current_player))

    @staticmethod
    def _increase_player_secondary_resources(player: Player):
        for resource in player.resources:
            try:
                resource_sub_type = get_resource_subtype(resource.resource_type)
                player.get_resource_by_type(resource_sub_type).increase_value(resource.value)
            except KeyError:
                pass

    @staticmethod
    def _decrease_player_secondary_resources(player: Player, card: Card):
        resource_sub_type = get_resource_subtype(card.resource_type)
        player.get_resource_by_type(resource_sub_type).decrease_value(card.price)

    def _get_opponent_to(self, player: Player):
        if player == self._first_player:
            return self._second_player
        return self._first_player

    def _is_over(self):
        return (
            self._is_player_boundary_values_violated(self._current_player)
            or self._is_player_boundary_values_violated(self._get_opponent_to(self._current_player))
        )

    def _get_winner_player(self):
        if self._is_player_won(self._first_player):
            return self._first_player
        elif self._is_player_won(self._second_player):
            return self._second_player
        else:
            return None

    def _is_player_won(self, player: Player):
        return (
            self._is_player_resource_achieve_boundary_value(player, ResourceBoundaryValueType.UPPER)
            or self._is_player_resource_achieve_boundary_value(
                self._get_opponent_to(player),
                ResourceBoundaryValueType.LOWER,
            )
        )

    def _is_player_boundary_values_violated(self, player: Player):
        return (
            self._is_player_resource_achieve_boundary_value(player, ResourceBoundaryValueType.LOWER)
            or self._is_player_resource_achieve_boundary_value(player, ResourceBoundaryValueType.UPPER)
        )

    def _is_player_resource_achieve_boundary_value(
        self,
        player: Player,
        boundary_value_type: ResourceBoundaryValueType,
    ):
        for resource in player.resources:
            for boundary_value in self._settings.resource_boundary_values:
                if (
                    resource.resource_type == boundary_value.resource_type
                    and boundary_value.resource_boundary_value_type == boundary_value_type
                ):
                    match boundary_value_type:
                        case ResourceBoundaryValueType.LOWER:
                            return resource.value <= boundary_value.value
                        case ResourceBoundaryValueType.UPPER:
                            return resource.value >= boundary_value.value

        return False


class PlayerCardApplier:

    def __init__(self, first_player: Player, second_player: Player):
        self._current_player = first_player
        self._opponent_player = second_player

    def apply_card(self, card: Card):
        for impact in card.impacts:
            if impact.has_condition:
                self._apply_card_impact_with_condition(impact)
            else:
                self._apply_card_impact(impact)

    def _apply_card_impact_with_condition(self, impact: CardImpact):
        if (
            impact.condition.is_current_player
            and PlayerCardApplier._card_impact_condition_to_boolean(impact.condition, self._current_player)
        ):
            self._apply_card_impact(impact)
        elif (
            impact.condition.is_opponent_player
            and PlayerCardApplier._card_impact_condition_to_boolean(impact.condition, self._opponent_player)
        ):
            self._apply_card_impact(impact)
        elif (
            PlayerCardApplier._card_impact_condition_to_boolean(
                impact.condition,
                self._current_player,
                self._opponent_player,
            )
        ):
            self._apply_card_impact(impact)

    def _apply_card_impact(self, impact: CardImpact):
        match impact.side:
            case CardImpactSide.SELF:
                PlayerCardApplier._handle_card_impact(impact, self._current_player, self._opponent_player)
            case CardImpactSide.OPPONENT | CardImpactSide.BOTH:
                PlayerCardApplier._handle_card_impact(impact, self._opponent_player, self._current_player)

    @staticmethod
    def _handle_card_impact(impact: CardImpact, first_player: Player, second_player: Player):
        match impact.type:
            case CardImpactType.RESOURCE:
                PlayerCardApplier._handle_resource_card_impact(impact, first_player, second_player)
            case CardImpactType.DAMAGE:
                PlayerCardApplier._handle_damage_card_impact(impact, first_player)

    @staticmethod
    def _handle_resource_card_impact(impact: CardImpact, first_player: Player, second_player: Player):
        first_player_resource = first_player.get_resource_by_type(impact.resource_type)
        second_player_resource = second_player.get_resource_by_type(impact.resource_type)

        match impact.action:
            case CardImpactAction.INCREASE:
                first_player_resource.increase_value(impact.value)
            case CardImpactAction.DECREASE:
                first_player_resource.decrease_value(impact.value)
            case CardImpactAction.MAKE_EQUAL_TO_OPPONENT:
                first_player_resource.value = second_player_resource.value
            case CardImpactAction.MAKE_EQUAL_TO_GREATER:
                first_player_resource.value = max(
                    first_player_resource.value,
                    second_player_resource.value,
                )
            case CardImpactAction.SWAP:
                first_player_resource_value = first_player_resource.value
                second_player_resource_value = second_player_resource.value
                first_player_resource.value = second_player_resource_value
                second_player_resource.value = first_player_resource_value

    @staticmethod
    def _handle_damage_card_impact(impact: CardImpact, player: Player):
        wall_resource = player.get_resource_by_type(ResourceType.WALL)
        tower_resource = player.get_resource_by_type(ResourceType.TOWER)

        if impact.value > wall_resource.value:
            decrease_tower_resource_value = impact.value - wall_resource.value
            wall_resource.decrease_value(impact.value)
            tower_resource.decrease_value(decrease_tower_resource_value)
        else:
            wall_resource.decrease_value(impact.value)

    @staticmethod
    def _card_impact_condition_to_boolean(
        condition: CardImpactCondition,
        first_player: Player,
        second_player: Optional[Player] = None,
    ):
        if second_player is not None:
            return condition.get_condition_result(
                first_player.get_resource_by_type(condition.first_resource_type).value,
                second_player.get_resource_by_type(condition.second_resource_type).value,
            )
        else:
            compared_value = (
                condition.value if condition.is_single_resource
                else first_player.get_resource_by_type(condition.second_resource_type).value
            )
            return condition.get_condition_result(
                first_player.get_resource_by_type(condition.first_resource_type).value,
                compared_value,
            )
