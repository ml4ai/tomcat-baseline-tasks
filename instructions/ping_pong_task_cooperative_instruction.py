import pygame

from .utils import instruction


def ping_pong_task_cooperative_instruction(to_server, screen, client_name):
    image = pygame.image.load("instructions/images/pinkiepie.jpg")
    instruction(image, to_server, screen, client_name)
