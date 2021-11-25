import pygame

from .constants import LEFT_TEAM


class Paddle(pygame.sprite.Sprite):
    """
    Paddle pygame sprite controlled by the client.
    """
    def __init__(self,
                 position: tuple,
                 paddle_width: int,
                 paddle_height: int,
                 color: tuple = (0, 0, 0),
                 upper_bound: int = 0,
                 lower_bound: int = 0,
                 speed_scaling: float = 1.0,
                 max_speed = None,
                 team: int = LEFT_TEAM):
        super().__init__()

         # Store game information
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound
        self._speed_scaling = speed_scaling
        self._max_speed = max_speed

        self.team = team

        # Set up pygame sprite
        self.image = pygame.Surface((paddle_width, paddle_height))
        self.image.fill((0, 0 ,0))

        self.mask = pygame.mask.from_surface(self.image)

        pygame.draw.rect(self.image, color, (0, 0, paddle_width, paddle_height))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update_location(self, change: int):
        speed = int(change * self._speed_scaling)

        if self._max_speed is not None:
            speed = max(-self._max_speed, min(self._max_speed, speed))

        self.rect.y = max(self._lower_bound, min(self._upper_bound, self.rect.y + speed))
