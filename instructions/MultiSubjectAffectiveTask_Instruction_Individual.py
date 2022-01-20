import pygame

from .utils import instruction


def finger_tapping_task_instruction(screen):
    image = pygame.image.load("instructions/images/TomCat_BaselineInstructions_AffectiveTask_Individual_Pt1.png")
    instruction(image, screen)

    image = pygame.image.load("instructions/images/TomCat_BaselineInstructions_AffectiveTask_Individual_Pt2.png")
    instruction(image, screen)
   