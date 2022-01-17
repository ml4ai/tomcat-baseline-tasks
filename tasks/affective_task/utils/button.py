import pygame
from common import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH

from .config import COLOR_BACKGROUND, COLOR_FOREGROUND


class Button:
    def __init__(self, offset, text, screen):
        x_offset, y_offset = offset
        x = CLIENT_WINDOW_WIDTH / 2 + x_offset
        y = CLIENT_WINDOW_HEIGHT / 2 + y_offset

        self._position = (x, y)
        self._text = text
        self._screen = screen

        self.object = None
        self._selected = False

    def render(self):
        font = pygame.font.SysFont("Arial", 50)
        text_render = font.render(self._text, 1, COLOR_FOREGROUND)

        _, _, w, h = text_render.get_rect()
        x, y = self._position
        x -= int(w / 2)
        y -= int(h / 2)

        pygame.draw.line(self._screen, COLOR_FOREGROUND, (x, y), (x + w , y), 3)
        pygame.draw.line(self._screen, COLOR_FOREGROUND, (x, y - 2), (x, y + h), 3)
        pygame.draw.line(self._screen, COLOR_FOREGROUND, (x, y + h), (x + w , y + h), 3)
        pygame.draw.line(self._screen, COLOR_FOREGROUND, (x + w , y+h), [x + w , y], 3)
        pygame.draw.rect(self._screen, COLOR_BACKGROUND, (x, y, w , h))

        self.object = self._screen.blit(text_render, (x, y))

        pygame.display.flip()
