import pygame
from common import COLOR_BACKGROUND, COLOR_DIM, COLOR_FOREGROUND
from config import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH


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

    def render(self, text_box_color=COLOR_BACKGROUND):
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

        pygame.draw.rect(self._screen, text_box_color, (x, y, w , h))

        self.object = self._screen.blit(text_render, (x, y))

        pygame.display.flip()

    def select(self):
        self._selected = True
        self.render(COLOR_DIM)

    def unselect(self):
        self._selected = False
        self.render()

    def is_selected(self) -> bool:
        return self._selected
