import threading

import pygame
from common import UPDATE_RATE, receive, send
from tasks.ping_pong_task.utils.constants import WINDOW_HEIGHT

from .utils import (BALL_SIZE, CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH,
                    COLOR_BACKGROUND, COLOR_FOREGROUND, WINDOW_HEIGHT,
                    WINDOW_WIDTH, Ball, Paddle)


class ClientPingPongTask:
    def __init__(self, from_server, to_server, screen, client_name, cooperative: bool = False) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen
        self._client_name = client_name

        if not cooperative:
            from . import config_ping_pong_competitive as cfg

        self._paddle_height = cfg.PADDLE_HEIGHT
        self._paddle_width = cfg.PADDLE_WIDTH

        self._game_y_lower_bound = int((CLIENT_WINDOW_HEIGHT - WINDOW_HEIGHT) / 2)
        self._game_y_upper_bound = self._game_y_lower_bound + WINDOW_HEIGHT

        self._game_x_lower_bound = int((CLIENT_WINDOW_WIDTH - WINDOW_WIDTH) / 2)
        self._game_x_upper_bound = self._game_x_lower_bound + WINDOW_WIDTH

        self._running = False

    def run(self):
        self._running = True

        client_input_thread = threading.Thread(target=self._client_input_handle, daemon=True)
        client_input_thread.start()

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        print("[STATUS] Running ping pong task")

        while self._running:
            pygame.event.get()

            data = receive([self._from_server], 0.0)
            if not data:
                continue
            else:
                [data] = data

            if data["type"] == "state":
                state = data["state"]
                score_left = data["score_left"]
                score_right = data["score_right"]
            elif data["type"] == "request":
                if data["request"] == "end":
                    self._running = False
                    break

            self._screen.fill(COLOR_BACKGROUND)

            # Add sprites to sprite group
            all_sprites_list = pygame.sprite.Group()
            for name, position in state.items():
                if name == "ball":
                    ball = Ball(BALL_SIZE)
                    ball.rect.x, ball.rect.y = position
                    all_sprites_list.add(ball)
                else:
                    paddle = Paddle(position, 
                                    paddle_width=self._paddle_width, 
                                    paddle_height=self._paddle_height, 
                                    color=COLOR_FOREGROUND)
                    all_sprites_list.add(paddle)

            # Draw sprite group
            all_sprites_list.draw(self._screen)

            # Draw game border
            pygame.draw.line(self._screen,
                             COLOR_FOREGROUND,
                             (self._game_x_lower_bound, self._game_y_lower_bound),
                             (self._game_x_upper_bound, self._game_y_lower_bound))
            pygame.draw.line(self._screen,
                             COLOR_FOREGROUND,
                             (self._game_x_lower_bound, self._game_y_upper_bound),
                             (self._game_x_upper_bound, self._game_y_upper_bound))
            pygame.draw.line(self._screen,
                             COLOR_FOREGROUND,
                             (self._game_x_lower_bound, self._game_y_lower_bound),
                             (self._game_x_lower_bound, self._game_y_upper_bound))
            pygame.draw.line(self._screen,
                             COLOR_FOREGROUND,
                             (self._game_x_upper_bound, self._game_y_lower_bound),
                             (self._game_x_upper_bound, self._game_y_upper_bound))

            # Display scores:
            font = pygame.font.Font(None, 74)
            text_score_left = font.render(str(score_left), 1, (255, 255, 255))
            text_score_left_rect = text_score_left.get_rect(center=(25, 25))
            self._screen.blit(text_score_left, text_score_left_rect)

            text_score_right = font.render(str(score_right), 1, (255, 255, 255))
            text_score_right_rect = text_score_right.get_rect(center=(WINDOW_WIDTH - 25, 25))
            self._screen.blit(text_score_right, text_score_right_rect)

            pygame.display.flip()

        # Wait for threads to finish
        client_input_thread.join()

        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)

        print("[STATUS] Ping pong task ended")

    def _client_input_handle(self):
        """
        Send user's input command to server
        """
        clock = pygame.time.Clock()
        while self._running:
            _, mouse_y_change = pygame.mouse.get_rel()

            data = {}
            data["type"] = "change"
            data["sender"] = self._client_name
            data["change"] = mouse_y_change

            send([self._to_server], data)

            clock.tick(UPDATE_RATE)
