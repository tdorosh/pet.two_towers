import collections
import re

from .card import Card
from .constants import RESOURCE_TYPE_MAPPING
from .enums import PlayerCardAction
from .player import Player
from .resource import ResourceType


class StrToIntDict(collections.UserDict):

    def __setitem__(self, key, item):
        try:
            self.data[key] = int(item)
        except ValueError:
            super().__setitem__(key, item)


def get_resource_subtype(resource_type: ResourceType):
    return RESOURCE_TYPE_MAPPING[resource_type]


def can_card_be_applied(card: Card, player: Player):
    card_resource_subtype = get_resource_subtype(card.resource_type)
    return player.get_resource_by_type(card_resource_subtype).value >= card.price


def is_player_action_allowed(permitted_actions: list[PlayerCardAction], current_action: PlayerCardAction):
    return current_action in permitted_actions


def camel_case_to_snake_case(string: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
