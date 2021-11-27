import pygame

from .utils import instruction, wait_for_experimenter


def finger_tapping_task_instruction(to_server, screen, client_name):
    image = pygame.image.load("instructions/images/TomCat_BaslineIntructions01-Introduction.png")
    instruction(image, screen)

    image = pygame.image.load("instructions/images/TomCat_BaselineInstructions02-FingerTapingGame_Explanation.png")
    instruction(image, screen)

    wait_for_experimenter(to_server, screen, client_name)
