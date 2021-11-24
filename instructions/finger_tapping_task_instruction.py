import pygame

from .utils import instruction, wait_for_experimenter


def finger_tapping_task_instruction(to_server, screen, client_name):
    image = pygame.image.load("instructions/images/more_pinkiepie.png")
    instruction(image, screen)

    image = pygame.image.load("instructions/images/pinkiepie.jpg")
    instruction(image, screen)

    wait_for_experimenter(to_server, screen, client_name)
