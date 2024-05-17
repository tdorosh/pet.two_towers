from dataclasses import dataclass, field
from typing import Optional

from game.enums import *
from .resource import ResourceType


@dataclass(frozen=True)
class Card:

    resource_type: ResourceType
    title: str
    description: str
    price: int
    impacts: list["CardImpact"] = field(default_factory=list)
    additional_features: list[CardAdditionalFeature] = field(default_factory=list)

    def __string__(self):
        return f"{self.title} {self.description}"

    def has_additional_feature(self, additional_feature: CardAdditionalFeature):
        return additional_feature in self.additional_features


@dataclass(frozen=True)
class CardImpact:

    type: CardImpactType
    resource_type: ResourceType
    side: CardImpactSide
    action: CardImpactAction
    value: Optional[int] = None
    condition: Optional["CardImpactCondition"] = None

    @property
    def has_condition(self):
        return self.condition is not None


@dataclass(frozen=True)
class CardImpactCondition:

    first_resource_type: ResourceType
    first_resource_side: CardImpactSide
    condition_value: CardImpactConditionValue
    second_resource_type: Optional[ResourceType] = None
    second_resource_side: Optional[CardImpactSide] = None
    value: Optional[int] = None

    def get_condition_result(self, compared_value: int, value_to_compare: int):
        match self.condition_value:
            case CardImpactConditionValue.GREATER_THAN:
                return compared_value > value_to_compare
            case CardImpactConditionValue.LESS_THAN:
                return compared_value < value_to_compare
            case CardImpactConditionValue.EQUAL:
                return compared_value == value_to_compare
            case CardImpactConditionValue.GREATER_THAN_OR_EQUAL:
                return compared_value >= value_to_compare
            case CardImpactConditionValue.LESS_THAN_OR_EQUAL:
                return compared_value <= value_to_compare

    @property
    def is_single_resource(self):
        return (
            self.second_resource is None
            and self.second_resource_side is None
        )

    @property
    def is_single_player(self):
        return (
            self.first_resource_side == self.second_resource_side
            or self.value is not None
        )

    @property
    def is_current_player(self):
        return (
            self.is_single_player
            and self.first_resource_side == CardImpactSide.SELF
        )

    @property
    def is_opponent_player(self):
        return (
            self.is_single_player
            and self.first_resource_side == CardImpactSide.OPPONENT
        )
