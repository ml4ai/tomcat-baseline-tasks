import threading

import pygame
from common import UPDATE_RATE, receive, send


class ClientFingerTappingTask:
    def __init__(self, from_server, to_server, screen, client_name) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen
        self._client_name = client_name

        self._state = None

        self._running = False

    def run(self):
        self._running = True

        client_input_thread = threading.Thread(target=self._client_input_handle, daemon=True)
        client_input_thread.start()

        print("[STATUS] Running client finger tapping task")

        while self._running:
            pygame.event.get()

            data = receive([self._from_server], 0.0)
            if not data:
                continue
            else:
                [data] = data

            self._state = data["state"]

            print(self._state)

            self._screen.fill((0, 0, 0))

            # Display timer
            font = pygame.font.Font(None, 74)
            text = font.render(str(self._state[self._client_name]), 1, (255, 255, 255))
            text_rect = text.get_rect(center=(500, 1000))
            self._screen.blit(text, text_rect)

            pygame.display.flip()

        # Wait for threads to finish
        client_input_thread.join()

    def _client_input_handle(self):
        """
        Send user's input command to server
        """
        clock = pygame.time.Clock()
        while self._running:
            # Get keys pressed by user
            keys = pygame.key.get_pressed()

            if self._state is None:
                continue

            data = None

            if keys[pygame.K_SPACE]:
                if self._state[self._client_name] == 0:
                    data = {}
                    data["type"] = "command"
                    data["sender"] = self._client_name
                    data["command"] = "tap"
            elif self._state[self._client_name] == 1:
                data = {}
                data["type"] = "command"
                data["sender"] = self._client_name
                data["command"] = "untap"

            if data is not None:
                send([self._to_server], data, wait_time=0.0)

            clock.tick(UPDATE_RATE)
