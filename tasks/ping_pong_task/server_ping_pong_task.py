import threading

import pygame
from common import UPDATE_RATE, receive, send

from .config_ping_pong_task import SESSION_TIME_SECONDS
from .utils import (BALL_SIZE, CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH,
                    WINDOW_HEIGHT, WINDOW_WIDTH, Ball, Paddle)


class ServerPingPongTask:
    def __init__(self, to_client_connections: list, from_client_connections: dict, cooperative: bool = False) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

        if not cooperative:
            from . import config_ping_pong_competitive as cfg

        self._paddle_height = cfg.PADDLE_HEIGHT
        self._paddle_width = cfg.PADDLE_WIDTH
        self._ball_bounce_on_paddle_scale = cfg.BALL_BOUNCE_ON_PADDLE_SCALE

        self._game_y_lower_bound = int((CLIENT_WINDOW_HEIGHT - WINDOW_HEIGHT) / 2)
        self._game_y_upper_bound = self._game_y_lower_bound + WINDOW_HEIGHT

        self._game_x_lower_bound = int((CLIENT_WINDOW_WIDTH - WINDOW_WIDTH) / 2)
        self._game_x_upper_bound = self._game_x_lower_bound + WINDOW_WIDTH

        center_paddle_y = int((self._game_y_upper_bound + cfg.PADDLE_HEIGHT) / 2)

        self._paddles = {}
        for count, client_name in enumerate(self._from_client_connections.values()):
            if count == 0:
                left_paddle_x = self._game_x_lower_bound
                initial_position = (left_paddle_x, center_paddle_y)
            else:
                right_paddle_x = self._game_x_upper_bound - cfg.PADDLE_WIDTH
                initial_position = (right_paddle_x, center_paddle_y)

            self._paddles[client_name] = Paddle(position=initial_position,
                                                paddle_width=cfg.PADDLE_WIDTH,
                                                paddle_height=cfg.PADDLE_HEIGHT,
                                                upper_bound=self._game_y_upper_bound - cfg.PADDLE_HEIGHT,
                                                lower_bound=self._game_y_lower_bound,
                                                speed_scaling=cfg.SPEED_SCALING,
                                                max_speed=cfg.MAX_SPEED)

        self._ball = Ball(BALL_SIZE, cfg.BALL_X_SPEED)

        self._score_left = 0
        self._score_right = 0

        self._running = False

    def run(self):
        self._running = True

        to_client_update_state_thread = threading.Thread(target=self._to_client_update_state, daemon=True)
        to_client_update_state_thread.start()

        from_client_commands_thread = threading.Thread(target=self._from_client_commands, daemon=True)
        from_client_commands_thread.start()

        print("[STATUS] Running ping pong task")

        # Wait for threads to finish
        to_client_update_state_thread.join()
        from_client_commands_thread.join()

        data = {}
        data["type"] = "request"
        data["request"] = "end"

        send(self._to_client_connections, data)

        print("[STATUS] Ping pong task ended")

    def _to_client_update_state(self):
        counter_target = SESSION_TIME_SECONDS

        start_ticks = pygame.time.get_ticks()

        seconds = 0.0

        clock = pygame.time.Clock()
        while self._running:
            if seconds >= counter_target:
                self._running = False
                break

            # Update state of the ball
            self._ball.update()

            # Check for collision between
            paddle_collide_ball = False
            for paddle in self._paddles.values():
                if pygame.sprite.collide_mask(self._ball, paddle):
                    ball_bound_y_velocity = int(((self._ball.rect.y + BALL_SIZE / 2.0) -
                                                 (paddle.rect.y + self._paddle_height / 2.0))
                                                * self._ball_bounce_on_paddle_scale)
                    self._ball.bounce(ball_bound_y_velocity)

                    if self._ball.rect.x < CLIENT_WINDOW_WIDTH / 2:
                        self._ball.rect.x = self._game_x_lower_bound + self._paddle_width

                    else:
                        self._ball.rect.x = self._game_x_upper_bound - self._paddle_width - BALL_SIZE

                    paddle_collide_ball = True
                    break

            # If ball has not collided with paddle, check if it collides with the wall
            if not paddle_collide_ball:
                # Collides with right wall
                if self._ball.rect.x >= self._game_x_upper_bound - BALL_SIZE:
                    self._score_left += 1
                    self._ball.bounce()
                    # Offset the ball to avoid collision with paddle
                    self._ball.rect.x = self._game_x_upper_bound - BALL_SIZE

                # Collides left wall
                elif self._ball.rect.x <= self._game_x_lower_bound:
                    self._score_right += 1
                    self._ball.bounce()
                    # Offset the ball to avoid collision with paddle
                    self._ball.rect.x = self._game_x_lower_bound

                # Collides with bottom wall
                elif self._ball.rect.y >= self._game_y_upper_bound - BALL_SIZE:
                    self._ball.rect.y = self._game_y_upper_bound - BALL_SIZE - 1
                    self._ball.velocity[1] = -self._ball.velocity[1]

                # Collides with top wall
                elif self._ball.rect.y <= self._game_y_lower_bound:
                    self._ball.rect.y = self._game_y_lower_bound + 1
                    self._ball.velocity[1] = -self._ball.velocity[1]

            data = {}
            data["type"] = "state"
            data["score_left"] = self._score_left
            data["score_right"] = self._score_right
            data["state"] = {}
            data["state"]["ball"] = (self._ball.rect.x, self._ball.rect.y)
            for client_name, paddle in self._paddles.items():
                data["state"][client_name] = (paddle.rect.x, paddle.rect.y)

            seconds_to_send = int(counter_target) - int(seconds)
            data["seconds"] = 1 if seconds_to_send <= 0 else seconds_to_send

            send(self._to_client_connections, data)

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0

            clock.tick(UPDATE_RATE)

    def _from_client_commands(self):
        while self._running:
            all_data = receive(self._from_client_connections.keys(), 0.1)

            for data in all_data:
                if data["type"] == "change":
                    self._paddles[data["sender"]].update_location(data["change"])
