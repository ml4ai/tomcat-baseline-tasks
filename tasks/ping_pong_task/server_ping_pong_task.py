import threading

from common import UPDATE_RATE, receive, send
from pygame import time

from .utils import Paddle


class ServerPingPongTask:
    def __init__(self, to_client_connections: list, from_client_connections: dict) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

        self._state = {}
        for client_name in self._from_client_connections.values():
            self._state[client_name] = Paddle(500, 10, 100, 980, 0, (0, 0, 0))

        self._running = False

    def run(self):
        self._running = True

        to_client_update_state_thread = threading.Thread(target=self._to_client_update_state, daemon=True)
        to_client_update_state_thread.start()

        from_client_commands_thread = threading.Thread(target=self._from_client_commands, daemon=True)
        from_client_commands_thread.start()

        print("[STATUS] Running finger tapping task")

        # Wait for threads to finish
        to_client_update_state_thread.join()
        from_client_commands_thread.join()

        data = {}
        data["type"] = "request"
        data["request"] = "end"

        send(self._to_client_connections, data)

        print("[STATUS] Finger tapping task ended")

    def _to_client_update_state(self):
        clock = time.Clock()
        while self._running:
            data = {}
            data["type"] = "state"

            data["state"] = {}
            for client_name, paddle in self._state.items():
                data["state"][client_name] = (paddle.rect.x, paddle.rect.y)

            send(self._to_client_connections, data)

            clock.tick(UPDATE_RATE)

    def _from_client_commands(self):
        while self._running:
            all_data = receive(self._from_client_connections.keys(), 0.1)

            for data in all_data:
                if data["type"] == "change":
                    self._state[data["sender"]].update_location(data["change"])
