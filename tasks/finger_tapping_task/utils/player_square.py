import pygame
from tasks.finger_tapping_task.config_finger_tapping_task import BOX_WIDTH


class PlayerSquare(pygame.sprite.Sprite):
    """
    Player square sprite
    """
    def __init__(self, position, color):
        # Set up pygame sprite
        super().__init__()
        self.image = pygame.Surface((BOX_WIDTH, BOX_WIDTH))
        self.image.fill((0, 0 ,0))
        self.image.set_colorkey((0, 0 ,0))
        pygame.draw.rect(self.image, color, (0, 0, BOX_WIDTH, BOX_WIDTH))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
