import pygame
from common import COLOR_BACKGROUND, COLOR_FOREGROUND
from config import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH


def render_text_center(text: str, text_box_shape, screen, font_size = 50, x_offset = 0, y_offset: int = 0):
    font = pygame.font.SysFont("Arial", font_size)
    text_render = font.render(text, True, COLOR_FOREGROUND)

    text_box = pygame.Surface(text_box_shape)
    text_box.fill(COLOR_BACKGROUND)

    text_box_shape_x, text_box_shape_y = text_box_shape
    _, _, text_width, _ = text_render.get_rect()
    text_box.blit(text_render, ((text_box_shape_x - text_width) / 2, 0))

    center = ((CLIENT_WINDOW_WIDTH - text_box_shape_x) / 2 + x_offset, (CLIENT_WINDOW_HEIGHT - text_box_shape_y) / 2 + y_offset)
    screen.blit(text_box, center)

    pygame.display.flip()
