import threading

import pygame
from common import UPDATE_RATE, receive, send

from .utils import COLOR_BACKGROUND, COLOR_FOREGROUND, Paddle


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
            elif data["type"] == "request":
                if data["request"] == "end":
                    self._running = False
                    break

            self._screen.fill(COLOR_BACKGROUND)

            # Add sprites to sprite group
            all_sprites_list = pygame.sprite.Group()
            for name, position in state.items():
                paddle = Paddle(position, 
                                paddle_width=self._paddle_width, 
                                paddle_height=self._paddle_height, 
                                color=COLOR_FOREGROUND)
                all_sprites_list.add(paddle)

            # Draw sprite group
            all_sprites_list.draw(self._screen)

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
