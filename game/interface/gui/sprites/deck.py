import pygame

from .base import BaseSprite
from ..constants import RESOURCE_PATH


class DeckSprite(BaseSprite):

    def _draw_elements(self):
        self._draw_deck()
        self._draw_current_card()

    def _draw_deck(self):
        background_image = pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / "cardBack3.jpg"),
            (self.image.get_width() / 2, self.image.get_height()),
        )
        self.image.blit(
            background_image,
            background_image.get_rect(left=self.image.get_rect().left),
        )

    def _draw_current_card(self):
        current_card_surface = pygame.Surface(
            (self.image.get_width() / 2, self.image.get_height()),
            pygame.SRCALPHA,
        )
        self.image.blit(
            current_card_surface,
            current_card_surface.get_rect(right=self.image.get_rect().right),
        )
