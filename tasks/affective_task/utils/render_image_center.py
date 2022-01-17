import pygame
from common import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH

COLOR_FOREGROUND = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)


def render_image_center(image_path: str, screen):
    image = pygame.image.load(image_path)

    screen.fill(COLOR_BACKGROUND)
    image_rect = image.get_rect(center=(CLIENT_WINDOW_WIDTH / 2, CLIENT_WINDOW_HEIGHT / 2))
    screen.blit(image, image_rect)

    pygame.display.flip()
