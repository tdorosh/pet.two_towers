from types import MappingProxyType

from .resource import ResourceType, ResourceBoundaryValue, ResourceBoundaryValueType


RESOURCE_TYPE_MAPPING = MappingProxyType(
    {
        # Main resource: secondary resource
        ResourceType.MINE: ResourceType.ORE,
        ResourceType.MONASTERY: ResourceType.MANA,
        ResourceType.BARRACKS: ResourceType.SQUADS,
    }
)

DEFAULT_PLAYER_CARD_COUNT = 6
DEFAULT_INITIAL_TOWER_VALUE = 20
DEFAULT_INITIAL_WALL_VALUE = 5
DEFAULT_INITIAL_MAIN_RESOURCE_VALUE = 2
DEFAULT_INITIAL_SECONDARY_RESOURCE_VALUE = 5
DEFAULT_RESOURCE_BOUNDARY_VALUES = frozenset(
    (
        ResourceBoundaryValue(ResourceType.TOWER, ResourceBoundaryValueType.LOWER, 0),
        ResourceBoundaryValue(ResourceType.TOWER, ResourceBoundaryValueType.UPPER, 50),
    )
)
