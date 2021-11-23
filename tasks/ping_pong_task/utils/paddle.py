import pygame


class Paddle(pygame.sprite.Sprite):
    """
    Paddle pygame sprite controlled by the client.
    """
    def __init__(self,
                 position,
                 paddle_width: int,
                 paddle_height: int,
                 color,
                 upper_bound: int = 0,
                 lower_bound: int = 0,
                 speed_scaling: float = 1.0):
        super().__init__()

         # Store game information
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound
        self._speed_scaling = speed_scaling

        # Set up pygame sprite
        self.image = pygame.Surface((paddle_width, paddle_height))
        self.image.fill((0, 0 ,0))
        self.image.set_colorkey((0, 0 ,0))
        pygame.draw.rect(self.image, color, (0, 0, paddle_width, paddle_height))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update_location(self, change: int):
        self.rect.y = max(self._lower_bound, min(self._upper_bound, self.rect.y + int(change * self._speed_scaling)))
