import pygame

from .utils import instruction


def introduction_instruction(screen):
    image = pygame.image.load("instructions/images/TomCat_BaselineInstructions01-Introduction.png")
    instruction(image, screen)
