import pygame

from .utils import instruction


def finger_tapping_task_instruction(screen):
    image = pygame.image.load("instructions/images/TomCat_BaselineInstructions02-FingerTapGame_Pt1.png")
    instruction(image, screen)

    image = pygame.image.load("instructions/images/TomCat_BaselineInstructions03_FingerTapGame_Pt2.png")
    instruction(image, screen)
