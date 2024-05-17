import pygame

from .base import BaseSprite
from ..constants import (
    PLAYER_NAME_WIDTH_RATIO,
    PLAYER_NAME_HEIGHT_RATIO,
    RESOURCE_INFO_WIDTH_RATIO,
    RESOURCE_INFO_HEIGHT_RATIO,
    RESOURCE_IMAGES_MAPPING,
    RESOURCE_COLORS_MAPPING,
    RESOURCE_PATH,
)
from game.constants import RESOURCE_TYPE_MAPPING
from game.helpers import get_resource_subtype


class PlayerResourceInfoSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, player, *, is_first_player):
        self._player = player
        self._is_first_player = is_first_player
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        group = pygame.sprite.Group()
        group.add(self._get_player_name())

        for index, resource_type in enumerate(RESOURCE_TYPE_MAPPING):
            group.add(self._get_resource_info(index, resource_type))

        group.draw(self.image)

    def _get_player_name(self):
        player_name_surface = pygame.Surface(
            (
                self.image.get_width() / PLAYER_NAME_WIDTH_RATIO,
                self.image.get_height() / PLAYER_NAME_HEIGHT_RATIO,
            )
        )
        return PlayerNameSprite(
            self.image,
            player_name_surface,
            (0, 0),
            self._player,
            is_first_player=self._is_first_player,
        )

    def _get_resource_info(self, index, resource_type):
        resource_info_surface = pygame.Surface(
            (
                self.image.get_width() / RESOURCE_INFO_WIDTH_RATIO,
                self.image.get_height() / RESOURCE_INFO_HEIGHT_RATIO,
            )
        )
        resource_info_position = (
            0,
            self.image.get_height()
            / PLAYER_NAME_HEIGHT_RATIO
            + resource_info_surface.get_height() * index,
        )
        return ResourceInfoSprite(
            self.image,
            resource_info_surface,
            resource_info_position,
            self._player,
            resource_type,
            is_first_player=self._is_first_player,
        )


class PlayerNameSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, player, *, is_first_player):
        pygame.font.init()
        self._font = pygame.font.Font(pygame.font.get_default_font(), surface.get_height() // 2)
        self._player = player
        self._is_first_player = is_first_player
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        self._draw_player_name()

    def _draw_player_name(self):
        player_name = self._font.render(
            self._player.name,
            True,
            (255, 255, 255),
        )
        gradient = self._get_gradient(*self._get_gradient_colors())
        self.image.blit(gradient, (0, 0))
        self.image.blit(
            player_name,
            player_name.get_rect(center=self.image.get_rect().center),
        )

    def _get_gradient(self, color_1, color_2, color_3):
        empty_gradient = pygame.Surface((3, 1))
        pygame.draw.line(empty_gradient, color_1, (0, 0), (1, 0))
        pygame.draw.line(empty_gradient, color_2, (1, 0), (2, 0))
        pygame.draw.line(empty_gradient, color_3, (2, 0), (3, 0))
        return pygame.transform.smoothscale(empty_gradient, self.image.get_size())

    def _get_gradient_colors(self):
        return (
            (pygame.Color("#220000"), pygame.Color("#a92626"), pygame.Color("#220000"))
            if self._is_first_player
            else (pygame.Color("#000022"), pygame.Color("#2c4c96"), pygame.Color("#000022"))
        )


class ResourceInfoSprite(BaseSprite):

    def __init__(
        self,
        parent_surface,
        surface,
        position,
        player,
        resource_type,
        *,
        is_first_player,
    ):
        pygame.font.init()
        self._font = pygame.font.Font(pygame.font.get_default_font(), surface.get_height() // 6)
        self._player = player
        self._resource_type = resource_type
        self._is_first_player = is_first_player
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        resource_title = self._font.render(
            str(get_resource_subtype(self._resource_type).name),
            True,
            pygame.Color("#e2d18c"),
        )
        main_resource_value = self._font.render(
            f"+{self._player.get_resource_by_type(self._resource_type).value}",
            True,
            (255, 255, 255)
        )
        secondary_resource_value = self._font.render(
            str(self._player.get_resource_by_type(get_resource_subtype(self._resource_type)).value),
            True,
            (255, 255, 255)
        )
        gradient = self._get_gradient(
            *RESOURCE_COLORS_MAPPING[self._resource_type],
        )
        surface_image = pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / "resGlass.png"),
            (self.image.get_width(), self.image.get_height()),
        )
        resource_image = self._get_resource_image()
        self.image.blit(gradient, (0, 0))
        self.image.blit(surface_image, (0, 0))
        self.image.blit(
            resource_title,
            (
                self.image.get_width()
                / (self.image.get_width() / ((self.image.get_width() - resource_title.get_width()) / 2)),
                self.image.get_height() / 10,
            ),
        )
        self.image.blit(
            main_resource_value,
            (self.image.get_width() / 12, self.image.get_height() / 6),
        )
        self.image.blit(
            secondary_resource_value,
            (self.image.get_width() / 1.18, self.image.get_height() / 1.33),
        )
        self.image.blit(
            resource_image,
            resource_image.get_rect(center=self.image.get_rect().center),
        )

    def _get_resource_image(self):
        image = pygame.transform.smoothscale(
            pygame.image.load(
                RESOURCE_PATH
                / RESOURCE_IMAGES_MAPPING[self._resource_type]
            ),
            (self.image.get_width() / 1.3, self.image.get_height() / 1.3),
        )
        return (
            image if self._is_first_player
            else pygame.transform.flip(image, True, False)
        )

    def _get_gradient(self, color_1, color_2):
        empty_gradient = pygame.Surface((2, 2))
        pygame.draw.line(empty_gradient, color_1, (0, 1), (1, 1))
        pygame.draw.line(empty_gradient, color_2, (0, 0), (1, 0))
        return pygame.transform.smoothscale(empty_gradient, self.image.get_size())
