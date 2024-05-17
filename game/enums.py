from enum import Enum, auto


class ResourceBoundaryValueType(Enum):
    LOWER = auto()
    UPPER = auto()


class ResourceType(Enum):

    MINE = auto()
    MONASTERY = auto()
    BARRACKS = auto()
    ORE = auto()
    MANA = auto()
    SQUADS = auto()
    TOWER = auto()
    WALL = auto()


class CardAdditionalFeature(Enum):

    PLAY_AGAIN = auto()
    DISCARD_AND_PLAY_AGAIN = auto()


class CardImpactType(Enum):

    RESOURCE = auto()
    DAMAGE = auto()


class CardImpactSide(Enum):

    SELF = auto()
    OPPONENT = auto()
    BOTH = auto()


class CardImpactAction(Enum):

    INCREASE = auto()
    DECREASE = auto()
    MAKE_EQUAL_TO_OPPONENT = auto()
    MAKE_EQUAL_TO_GREATER = auto()
    SWAP = auto()


class CardImpactConditionValue(Enum):

    GREATER_THAN = auto()
    LESS_THAN = auto()
    EQUAL = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN_OR_EQUAL = auto()


class PlayerCardAction(Enum):

    APPLY = auto()
    DISCARD = auto()

    @staticmethod
    def all_actions():
        return [action for action in PlayerCardAction]

    @staticmethod
    def discard_actions():
        return [PlayerCardAction.DISCARD]
