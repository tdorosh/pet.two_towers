import pygame

from .base import BaseSprite
from .buildings import PlayerBuildingSprite
from .deck import DeckSprite
from .resource import PlayerResourceInfoSprite
from ..constants import (
    CARD_WIDTH_RATIO,
    CARD_HEIGHT_RATIO,
    PLAYER_RESOURCE_INFO_WIDTH_RATIO,
    PLAYER_RESOURCE_INFO_HEIGHT_RATIO,
    PLAYER_BUILDINGS_WIDTH_RATIO,
    PLAYER_BUILDINGS_HEIGHT_RATIO,
    RESOURCE_PATH,
)


class TopComponentSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, first_player, second_player):
        self._first_player = first_player
        self._second_player = second_player
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        self._draw_background()
        group = pygame.sprite.Group()
        group.add(self._get_deck())
        group.add(self._get_player_resource_info(self._first_player, is_first_player=True))
        group.add(self._get_player_resource_info(self._second_player, is_first_player=False))
        group.add(self._get_player_buildings(self._first_player, is_first_player=True))
        group.add(self._get_player_buildings(self._second_player, is_first_player=False))
        group.draw(self.image)

    def _draw_background(self):
        background_image = pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / "bgField2.jpg").convert(),
            self.image.get_size(),
        )
        self.image.blit(background_image, (0, 0))

    def _get_deck(self):
        deck_surface = pygame.Surface(
            (
                (self.image.get_width() / CARD_WIDTH_RATIO * 2),
                self.image.get_height() / CARD_HEIGHT_RATIO,
            ),
            pygame.SRCALPHA,
        )
        return DeckSprite(
            self.image,
            deck_surface,
            (
                (self.image.get_width() - deck_surface.get_width()) / 2,
                (self.image.get_height() - deck_surface.get_height()) / 2,
            ),
        )

    def _get_player_resource_info(self, player, *, is_first_player):
        resource_info_surface = pygame.Surface(
            (
                self.image.get_width() / PLAYER_RESOURCE_INFO_WIDTH_RATIO,
                self.image.get_height() / PLAYER_RESOURCE_INFO_HEIGHT_RATIO,
            ),
            pygame.SRCALPHA,
        )
        resource_info_position = (
            (0, 0) if is_first_player
            else (self.image.get_width() - resource_info_surface.get_width(), 0)
        )
        return PlayerResourceInfoSprite(
            self.image,
            resource_info_surface,
            resource_info_position,
            player,
            is_first_player=is_first_player,
        )

    def _get_player_buildings(self, player, *, is_first_player):
        player_buildings_surface = pygame.Surface(
            (
                self.image.get_width() / PLAYER_BUILDINGS_WIDTH_RATIO,
                self.image.get_height() / PLAYER_BUILDINGS_HEIGHT_RATIO,
            ),
            pygame.SRCALPHA,
        )
        resource_info_sprite_width = self.image.get_width() / PLAYER_RESOURCE_INFO_WIDTH_RATIO
        player_buildings_position = (
            (resource_info_sprite_width, 0) if is_first_player
            else (
                self.image.get_width()
                - resource_info_sprite_width
                - player_buildings_surface.get_width(),
                0,
            )
        )
        return PlayerBuildingSprite(
            self.image,
            player_buildings_surface,
            player_buildings_position,
            player,
            is_first_player=is_first_player,
        )
