from .card import Card
from .exceptions import PlayerResourceNonFoundError
from .resource import Resource, ResourceType


class Player:

    def __init__(self, name: str):
        self._name = name
        self._resources: list[Resource] = []
        self._cards: list[Card] = []

    def __string__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, resources: list[Resource]):
        self._resources = resources

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards: list[Card]):
        self._cards = cards

    def add_card(self, card: Card, index: int):
        self.cards[index] = card

    def get_card_index(self, card: Card):
        return self.cards.index(card)

    def get_card_by_index(self, index: int):
        return self.cards[index]

    def get_resource_by_type(self, resource_type: ResourceType):
        for resource in self.resources:
            if resource.resource_type == resource_type:
                return resource

        raise PlayerResourceNonFoundError
