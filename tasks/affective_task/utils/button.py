from typing import Tuple

import pygame
from common import COLOR_DIM, COLOR_FOREGROUND
from config import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH


class Button:
    def __init__(self, offset: Tuple[int, int], screen):
        x_offset, y_offset = offset
        x = CLIENT_WINDOW_WIDTH / 2 + x_offset
        y = CLIENT_WINDOW_HEIGHT / 2 + y_offset

        self._position = (x, y)
        self._screen = screen

        self.object = None
        self._selected = False

    def render(self):
        x, y = self._position

        if self._selected:
            color = COLOR_FOREGROUND
        else:
            color = COLOR_DIM

        self.object = pygame.draw.rect(self._screen, color, (x, y, 100, 200))

        pygame.display.flip()

    def select(self):
        self._selected = True
        self.render()

    def unselect(self):
        self._selected = False
        self.render()

    def is_selected(self) -> bool:
        return self._selected
