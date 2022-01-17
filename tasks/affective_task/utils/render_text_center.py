import pygame
from common import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH

from .config import COLOR_BACKGROUND, COLOR_FOREGROUND


def render_text_center(text: str, text_box_shape, screen, y_offset: int = 0):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, True, COLOR_FOREGROUND)

    text_box = pygame.Surface(text_box_shape)
    text_box.fill(COLOR_BACKGROUND)

    text_box_shape_x, text_box_shape_y = text_box_shape
    _, _, text_width, _ = text_render.get_rect()
    text_box.blit(text_render, ((text_box_shape_x - text_width) / 2, 0))

    center = ((CLIENT_WINDOW_WIDTH - text_box_shape_x) / 2, (CLIENT_WINDOW_HEIGHT - text_box_shape_y) / 2 + y_offset)
    screen.blit(text_box, center)

    pygame.display.flip()
