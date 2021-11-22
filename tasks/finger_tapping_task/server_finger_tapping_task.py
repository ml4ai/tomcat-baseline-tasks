import threading

from common import UPDATE_RATE, send
from pygame import time


class ServerFingerTappingTask:
    def __init__(self, to_client_connections: list, from_client_connections: dict) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

        self._running = False

    def run(self):
        self._running = True

        to_client_update_state_thread = threading.Thread(target=self._to_client_update_state, daemon=True)
        to_client_update_state_thread.start()

        print("[STATUS] Running server finger tapping task")

        # Wait for threads to finish
        to_client_update_state_thread.join()

    def _to_client_update_state(self):
        data = {}
        data["type"] = "state"
        data["state"] = "Hello World!"

        clock = time.Clock()
        while self._running:
            send(self._to_client_connections, data)

            clock.tick(UPDATE_RATE)
