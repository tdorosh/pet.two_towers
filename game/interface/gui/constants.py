import pathlib
from types import MappingProxyType

import pygame

from game.resource import ResourceType


RESOURCE_PATH = pathlib.Path(__file__).absolute().parent / "resources"

CARD_RESOURCE_BACKGROUND_MAPPING = MappingProxyType({
    ResourceType.MINE: "cardRed2.jpg",
    ResourceType.MONASTERY: "cardBlue2.jpg",
    ResourceType.BARRACKS: "cardGreen2.jpg",
})
CARD_IMAGE_MAPPING = MappingProxyType({
    ResourceType.MINE: "red",
    ResourceType.MONASTERY: "blue",
    ResourceType.BARRACKS: "green",
})

RESOURCE_IMAGES_MAPPING = MappingProxyType(
    {
        ResourceType.MINE: "res_mine.png",
        ResourceType.MONASTERY: "res_monastery.png",
        ResourceType.BARRACKS: "res_barracks.png",
    }
)
RESOURCE_COLORS_MAPPING = MappingProxyType(
    {
        ResourceType.MINE: (pygame.Color("#651b19"), pygame.Color("#8c2523")),
        ResourceType.MONASTERY: (pygame.Color("#193965"), pygame.Color("#23548c")),
        ResourceType.BARRACKS: (pygame.Color("#346519"), pygame.Color("#418c23")),
    }
)

BOTTOM_COMPONENT_WIDTH_RATIO = 1
BOTTOM_COMPONENT_HEIGHT_RATIO = 2
TOP_COMPONENT_WIDTH_RATIO = 1
TOP_COMPONENT_HEIGHT_RATIO = 2

PLAYER_RESOURCE_INFO_WIDTH_RATIO = 9
PLAYER_RESOURCE_INFO_HEIGHT_RATIO = 1
PLAYER_BUILDINGS_WIDTH_RATIO = 9
PLAYER_BUILDINGS_HEIGHT_RATIO = 1

PLAYER_NAME_WIDTH_RATIO = 1
PLAYER_NAME_HEIGHT_RATIO = 12

RESOURCE_INFO_WIDTH_RATIO = 1
RESOURCE_INFO_HEIGHT_RATIO = 3.5

PLAYER_BUILDINGS_CURRENT_VALUES_WIDTH_RATIO = 2
PLAYER_BUILDINGS_CURRENT_VALUES_HEIGHT_RATIO = 15

CARD_WIDTH_RATIO = 9
CARD_HEIGHT_RATIO = 1.5
