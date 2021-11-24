import pygame
from common import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH, send

from .config_instructions import (COLOR_BACKGROUND, COLOR_FOREGROUND,
                                  FONT_SIZE, WAIT_FOR_EXPERIMENTER_MSG)


def wait_for_experimenter(to_server, screen, client_name):
    screen.fill(COLOR_BACKGROUND)
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(WAIT_FOR_EXPERIMENTER_MSG, 1, COLOR_FOREGROUND)
    text_rect = text.get_rect(center=(CLIENT_WINDOW_WIDTH / 2, CLIENT_WINDOW_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    data = {}
    data["type"] = "ready"
    data["sender"] = client_name

    send([to_server], data)
