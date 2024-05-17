import pygame

from .base import BaseSprite
from ..constants import CARD_IMAGE_MAPPING, CARD_RESOURCE_BACKGROUND_MAPPING, RESOURCE_PATH
from ..helpers import wrap_text


class CardSprite(BaseSprite):

    def __init__(self, parent_surface, surface, position, card):
        pygame.font.init()
        self._font = pygame.font.Font(
            pygame.font.get_default_font(),
            surface.get_height() // 15,
        )
        self._card = card
        super().__init__(parent_surface, surface, position)

    def _draw_elements(self):
        self._draw_background()
        self._draw_card_title()
        self._draw_card_image()
        self._draw_card_description()
        self._draw_discard_button()
        self._draw_price()

    def _draw_background(self):
        background_image = pygame.transform.smoothscale(
            pygame.image.load(
                RESOURCE_PATH
                / CARD_RESOURCE_BACKGROUND_MAPPING[self._card.resource_type]
            ),
            self.image.get_size(),
        )
        self.image.blit(background_image, (0, 0))

    def _draw_card_title(self):
        title_surface = pygame.Surface(
            (
                self.image.get_width() / 1.2,
                self.image.get_height() / 3,
            )
        )
        text_parts = wrap_text(
            self._card.title,
            (255, 255, 255),
            title_surface.get_rect(),
            self._font,
            additional_delimiter="-",
        )
        for index, surface in enumerate(text_parts):
            self.image.blit(
                surface,
                (
                    (self.image.get_width() - surface.get_width()) / 2,
                    self.image.get_height() / 18 + surface.get_height() * index,
                ),
            )

    def _draw_card_description(self):
        description_surface = pygame.Surface(
            (
                self.image.get_width() / 1.2,
                self.image.get_height() / 3,
            )
        )
        text_parts = wrap_text(
            self._card.description,
            (255, 255, 255),
            description_surface.get_rect(),
            self._font,
        )
        for index, surface in enumerate(text_parts):
            self.image.blit(
                surface,
                (
                    (self.image.get_width() - surface.get_width()) / 2,
                    self.image.get_height() / 1.8 + surface.get_height() * index,
                ),
            )

    def _draw_card_image(self):
        card_image = pygame.transform.smoothscale(
            pygame.image.load(
                RESOURCE_PATH
                / "cards"
                / CARD_IMAGE_MAPPING[self._card.resource_type]
                / f"{self._card.title}.jpg"
            ).convert(),
            (self.image.get_width() / 1.2, self.image.get_height() / 3),
        )
        self.image.blit(
            card_image,
            (self.image.get_width() / 11.5, self.image.get_height() / 5)
        )

    def _draw_discard_button(self):
        button_image = pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / "btn_minus.png"),
            (self.image.get_width() / 5, self.image.get_height() / 8),
        )
        self.image.blit(
            button_image,
            button_image.get_rect(bottomleft=self.image.get_rect().bottomleft),
        )

    def _draw_price(self):
        price_image = pygame.transform.smoothscale(
            pygame.image.load(RESOURCE_PATH / "btn_cardValue2r.png"),
            (self.image.get_width() / 5, self.image.get_height() / 8),
        )
        secondary_resource_value = self._font.render(
            str(self._card.price),
            True,
            (0, 0, 0)
        )
        price_image.blit(
            secondary_resource_value,
            secondary_resource_value.get_rect(center=price_image.get_rect().center),
        )
        self.image.blit(
            price_image,
            price_image.get_rect(bottomright=self.image.get_rect().bottomright),
        )
