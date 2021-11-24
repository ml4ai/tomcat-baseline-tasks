import pygame

from .utils import instruction


def finger_tapping_task_instruction(to_server, screen, client_name):
    image = pygame.image.load("instructions/images/pinkiepie.jpg")
    instruction(image, to_server, screen, client_name)
