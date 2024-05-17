import sys

import pygame

from game.interface.gui.constants import (
    BOTTOM_COMPONENT_WIDTH_RATIO,
    BOTTOM_COMPONENT_HEIGHT_RATIO,
    TOP_COMPONENT_WIDTH_RATIO,
    TOP_COMPONENT_HEIGHT_RATIO,
)
from .sprites.bottom import BottomComponentSprite
from .sprites.top import TopComponentSprite


class GraphicalInterface:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Two Towers")
        self._screen = pygame.display.set_mode(
            (
                pygame.display.Info().current_w / 1.5,
                pygame.display.Info().current_h / 1.5
            ),
            pygame.RESIZABLE,
        )
        self._clock = pygame.time.Clock()
        self._current_player = None
        self._opponent_player = None
        self._running = True

    def set_players(self, first_player, second_player):
        self._current_player = first_player
        self._opponent_player = second_player

    def show_current_state(self):
        game_board = self._get_game_board()

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self._screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    game_board = self._get_game_board()

            game_board.update()
            game_board.draw(self._screen)
            pygame.display.flip()
            pygame.display.update()
            self._clock.tick(60)

        pygame.quit()

    def _get_game_board(self,):
        game_board = pygame.sprite.Group()
        game_board.add(self._get_bottom_component())
        game_board.add(self._get_top_component())
        return game_board

    def _get_top_component(self):
        top_component_surface = pygame.Surface(
            (
                self._screen.get_width() / TOP_COMPONENT_WIDTH_RATIO,
                self._screen.get_height() / TOP_COMPONENT_HEIGHT_RATIO,
            )
        )
        return TopComponentSprite(
            self._screen,
            top_component_surface,
            (0, 0),
            self._current_player,
            self._opponent_player,
        )

    def _get_bottom_component(self):
        bottom_component_surface = pygame.Surface(
            (
                self._screen.get_width() / BOTTOM_COMPONENT_WIDTH_RATIO,
                self._screen.get_height() / BOTTOM_COMPONENT_HEIGHT_RATIO,
            )
        )
        return BottomComponentSprite(
            self._screen,
            bottom_component_surface,
            (0, self._screen.get_height() / 2),
            self._current_player,
        )
