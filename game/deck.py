from random import shuffle
from xml.etree import ElementTree

from .card import Card, CardImpact, CardImpactCondition
from .helpers import camel_case_to_snake_case, StrToIntDict
from .enums import *


class Deck:

    def __init__(self):
        self._cards: list[Card] = []

    def put_underneath(self, card: Card):
        self._cards.append(card)

    def get(self):
        return self._cards.pop(0)

    def shuffle(self):
        shuffle(self._cards)


class DeckFromFileInitializer:

    @staticmethod
    def initialize(deck: Deck):
        for card_element in ElementTree.parse('cards.xml').getroot():
            deck.put_underneath(
                DeckFromFileInitializer._build_card(card_element)
            )

    @staticmethod
    def _get_card_impacts(card_element: ElementTree.Element):
        return [
            DeckFromFileInitializer._build_card_impact(impact_element)
            for impact_element in card_element.findall("impact")
        ]

    @staticmethod
    def _get_card_impact_conditions(impact_element: ElementTree.Element):
        condition_list = [
            DeckFromFileInitializer._build_card_impact_condition(condition_element)
            for condition_element in impact_element.findall("condition")
        ]

        try:
            return condition_list[0]
        except IndexError:
            return None

    @staticmethod
    def _get_card_features(card_element: ElementTree.Element):
        return [
            CardAdditionalFeature[feature_element.attrib["name"]]
            for feature_element in card_element.findall("feature")
        ]

    @staticmethod
    def _build_card(card_element: ElementTree.Element):
        card = {
            "resource_type": ResourceType[card_element.attrib.pop("resource")],
            "impacts": DeckFromFileInitializer._get_card_impacts(card_element),
            "additional_features": DeckFromFileInitializer._get_card_features(card_element),
            **StrToIntDict(card_element.attrib),
        }
        return Card(**card)

    @staticmethod
    def _build_card_impact(impact_element: ElementTree.Element):
        value = impact_element.attrib.pop("value", None)
        return CardImpact(
            type=CardImpactType[impact_element.attrib.pop("type")],
            resource_type=ResourceType[impact_element.attrib.pop("resource")],
            side=CardImpactSide[impact_element.attrib.pop("side")],
            action=CardImpactAction[impact_element.attrib.pop("action")],
            value=int(value) if value else None,
            condition=DeckFromFileInitializer._get_card_impact_conditions(impact_element),
        )

    @staticmethod
    def _build_card_impact_condition(condition_element: ElementTree.Element):
        value = condition_element.attrib.pop("value", None)
        second_resource_type = condition_element.attrib.pop("secondResource", None)
        second_resource_side = condition_element.attrib.pop("secondResourceSide", None)
        return CardImpactCondition(
            first_resource_type=ResourceType[condition_element.attrib.pop("firstResource")],
            first_resource_side=CardImpactSide[condition_element.attrib.pop("firstResourceSide")],
            condition_value=CardImpactConditionValue[condition_element.attrib.pop("conditionValue")],
            second_resource_type=ResourceType[second_resource_type] if second_resource_side else None,
            second_resource_side=CardImpactSide[second_resource_side] if second_resource_side else None,
            value=int(value) if value else None
        )
