import pygame

from .base import BaseSprite
from ..constants import (
    PLAYER_BUILDINGS_CURRENT_VALUES_WIDTH_RATIO,
    PLAYER_BUILDINGS_CURRENT_VALUES_HEIGHT_RATIO,
    RESOURCE_PATH,
)
from game.resource import ResourceType


class PlayerBuildingSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, player, *, is_first_player):
        self._player = player
        self._is_first_player = is_first_player
        super().__init__(parent_surface, surface, position)
        # self.image.fill(pygame.Color(255, 255, 255), self.image.get_rect().inflate(-1, -1))

    def _draw_elements(self):
        group = pygame.sprite.Group()
        group.add(self._get_tower_building())
        group.add(self._get_wall_building())
        group.add(self._get_current_values())
        group.draw(self.image)

    def _get_current_values(self):
        current_values_surface = pygame.Surface(
            (
                self.image.get_width() / PLAYER_BUILDINGS_CURRENT_VALUES_WIDTH_RATIO,
                self.image.get_height() / PLAYER_BUILDINGS_CURRENT_VALUES_HEIGHT_RATIO,
            ),
        )
        current_values_position = (
            (
                (self.image.get_width() - current_values_surface.get_width()) / 2,
                self.image.get_height() - current_values_surface.get_height(),
            )
        )
        return BuildingValueSprite(
            self.image,
            current_values_surface,
            current_values_position,
            self._player,
            is_first_player=self._is_first_player,
        )

    def _get_tower_building(self):
        tower_building_surface = pygame.Surface(
            (
                self.image.get_width() / PlayerTowerSprite.WIDTH_RATIO,
                self.image.get_height(),
            ),
            pygame.SRCALPHA,
        )
        tower_building_position = (
            (0, 0) if self._is_first_player
            else (self.image.get_width() * 0.3, 0)
        )
        return PlayerTowerSprite(
            self.image,
            tower_building_surface,
            tower_building_position,
            self._player,
            is_first_player=self._is_first_player,
        )

    def _get_wall_building(self):
        wall_building_surface = pygame.Surface(
            (
                self.image.get_width() / PlayerWallSprite.WIDTH_RATIO,
                self.image.get_height(),
            ),
            pygame.SRCALPHA,
        )
        wall_building_position = (
            (self.image.get_width() * 0.3, 0)
            if self._is_first_player else (0, 0)
        )
        return PlayerWallSprite(
            self.image,
            wall_building_surface,
            wall_building_position,
            self._player,
            is_first_player=self._is_first_player,
        )


class BuildingSprite(BaseSprite):

    RESOURCE_TYPE: ResourceType
    WIDTH_RATIO: int
    MAX_HEIGHT: int

    def __init__(self, parent_surface, surface, position, player, *, is_first_player):
        self._player = player
        self._is_first_player = is_first_player
        super().__init__(parent_surface, surface, position)

    @property
    def current_value(self):
        return self._player.get_resource_by_type(self.RESOURCE_TYPE).value

    def _draw_elements(self):
        self.image.blit(
            self._get_image(),
            (0, self._get_height_destination()),
        )

    def _get_height_destination(self):
        max_height = self.image.get_height()
        division_value = max_height / self.MAX_HEIGHT * 1.5
        return max(0, max_height - self.current_value * division_value)

    def _get_image(self):
        return pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / self._get_image_name()),
            self.image.get_size(),
        )

    def _get_image_name(self):
        raise NotImplemented


class PlayerTowerSprite(BuildingSprite):

    RESOURCE_TYPE = ResourceType.TOWER
    WIDTH_RATIO = 1.3
    MAX_HEIGHT = 50

    def _get_image_name(self):
        return "BldTower1.png" if self._is_first_player else "BldTower2.png"


class PlayerWallSprite(BuildingSprite):

    RESOURCE_TYPE = ResourceType.WALL
    WIDTH_RATIO = 1.3
    MAX_HEIGHT = 50

    def _get_image_name(self):
        return "BldWall1.png" if self._is_first_player else "BldWall2.png"


class BuildingValueSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, player, *, is_first_player):
        pygame.font.init()
        self._font = pygame.font.Font(pygame.font.get_default_font(), surface.get_height() // 2)
        self._player = player
        self._is_first_player = is_first_player
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        value_text = self._font.render(
            self._get_current_value(),
            True,
            (0, 0, 0),
        )
        self.image.fill(pygame.Color("#d9d7a0"))
        self.image.blit(value_text, value_text.get_rect(center=self.image.get_rect().center))

    def _get_current_value(self):
        tower_current_value = self._player.get_resource_by_type(ResourceType.TOWER).value
        wall_current_value = self._player.get_resource_by_type(ResourceType.WALL).value
        return (
            f"{tower_current_value} | {wall_current_value}"
            if self._is_first_player
            else f"{wall_current_value} | {tower_current_value}"
        )
