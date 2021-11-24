import pygame

from .utils import instruction, wait_for_experimenter


def ping_pong_task_cooperative_instruction(to_server, screen, client_name):
    image = pygame.image.load("instructions/images/pinkiepie.jpg")
    instruction(image, screen)

    wait_for_experimenter(to_server, screen, client_name)
