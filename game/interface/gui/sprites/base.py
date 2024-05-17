import pygame


class BaseSprite(pygame.sprite.Sprite):

    def __init__(self, parent_surface, surface, position, *args, **kwargs):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect().move(position)
        self._parent_surface = parent_surface
        self._draw_elements()

    def update(self):
        pass

    def draw(self):
        self._parent_surface.blit(self.image, self.rect)

    def _scale_image(self):
        pass

    def _draw_elements(self):
        raise NotImplemented
