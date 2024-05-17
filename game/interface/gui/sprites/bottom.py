import pygame

from .base import BaseSprite
from .card import CardSprite
from ..constants import CARD_WIDTH_RATIO, CARD_HEIGHT_RATIO, RESOURCE_PATH


class BottomComponentSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, player):
        self._player = player
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        self._draw_background()
        self._draw_cards()

    def _draw_background(self):
        background_image = pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / "bgField1.jpg").convert(),
            self.image.get_size(),
        )
        self.image.blit(background_image, (0, 0))

    def _draw_cards(self):
        group = pygame.sprite.Group()
        for index, card in enumerate(self._player.cards):
            card_surface = self._get_card_surface()
            indent = (self.image.get_width() - card_surface.get_width() * 6) / 7
            position = (
                indent + (card_surface.get_width() + indent) * index,
                (self.image.get_height() - card_surface.get_height()) / 2,
            )
            card_sprite = CardSprite(self.image, card_surface, position, card)
            group.add(card_sprite)

        group.draw(self.image)

    def _get_card_surface(self):
        return pygame.Surface(
            (
                self.image.get_width() / CARD_WIDTH_RATIO,
                self.image.get_height() / CARD_HEIGHT_RATIO,
            )
        )
