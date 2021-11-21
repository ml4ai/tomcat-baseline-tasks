import socket
import threading

import pygame
from common import UPDATE_RATE
from task import ClientTask

from .utils import receive, send


class Client:
    def __init__(self, host: str, port: int, client_name: str, client_task: ClientTask) -> None:
        self._client_name = client_name

        self._from_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._from_server.connect((host, port))
        self._from_server.setblocking(False)

        self._to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._to_server.connect((host, port + 1))
        self._to_server.setblocking(False)

        send([self._to_server], self._client_name)

        print("Connected to server")

        self._state = None

        self._running = False

        self._client_task = client_task

    def run(self):
        self._running = True

        # Create a thread for controlling client from terminal
        client_input_thread = threading.Thread(target=self._client_input_handle, daemon=True)
        client_input_thread.start()

        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        while self._running:
            pygame.event.get()

            data = receive([self._from_server], 0.0)
            if not data:
                continue
            else:
                [data] = data

            screen.fill((0, 0, 0))

            # provide data, modify screen

            pygame.display.flip()

        # Wait for threads to finish
        client_input_thread.join()

        # Close server connection
        self._from_server.close()
        self._to_server.close()

    def _client_input_handle(self):
        """
        Send user's input command to server
        """
        clock = pygame.time.Clock()
        while self._running:
            # Get keys pressed by user
            keys = pygame.key.get_pressed()

            # send key to client task, return data to send
            data = None

            if data is not None:
                send([self._to_server], data, wait_time=0.0)

            clock.tick(UPDATE_RATE)
