import threading

import pygame
from common import UPDATE_RATE, receive, send

from .utils import Paddle


class ClientPingPongTask:
    def __init__(self, from_server, to_server, screen, client_name) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen
        self._client_name = client_name

        self._running = False

    def run(self):
        self._running = True

        client_input_thread = threading.Thread(target=self._client_input_handle, daemon=True)
        client_input_thread.start()

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

            self._screen.fill((0, 0, 0))

            # Add sprites to sprite group
            all_sprites_list = pygame.sprite.Group()
            for name, position in state.items():
                paddle = Paddle(position, 10, 100, (255, 255, 255))
                all_sprites_list.add(paddle)

            # Draw sprite group
            all_sprites_list.draw(self._screen)

            pygame.display.flip()

        # Wait for threads to finish
        client_input_thread.join()

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

            send([self._to_server], data, wait_time=0.0)

            clock.tick(UPDATE_RATE)
