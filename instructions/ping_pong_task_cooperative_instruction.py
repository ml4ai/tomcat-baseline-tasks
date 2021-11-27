import pygame

from .utils import instruction


def ping_pong_task_cooperative_instruction(screen):
    image = pygame.image.load("instructions/images/pinkiepie.jpg")
    instruction(image, screen)
