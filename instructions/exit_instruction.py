import pygame
from common import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH, send

from .utils import COLOR_BACKGROUND, COLOR_FOREGROUND, FONT_SIZE, READY_MSG


def exit_instruction(to_server, screen, client_name):
    screen.fill(COLOR_BACKGROUND)

    font = pygame.font.Font(None, FONT_SIZE)

    text = font.render("Thank you for participating in the baseline tasks", 1, COLOR_FOREGROUND)
    text_rect = text.get_rect(center=(CLIENT_WINDOW_WIDTH / 2, CLIENT_WINDOW_HEIGHT / 2))
    screen.blit(text, text_rect)

    text = font.render(READY_MSG, 1, COLOR_FOREGROUND)
    text_rect = text.get_rect(center=(CLIENT_WINDOW_WIDTH / 2, CLIENT_WINDOW_HEIGHT - 60))
    screen.blit(text, text_rect)

    pygame.display.flip()

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            break

    data = {}
    data["type"] = "ready"
    data["sender"] = client_name

    send([to_server], data)
