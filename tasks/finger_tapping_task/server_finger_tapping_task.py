import csv
import json
import os
import threading
from time import time

import pygame
from common import UPDATE_RATE, receive, send

from .config_finger_tapping_task import (SECONDS_COUNT_DOWN,
                                         SECONDS_PER_SESSION, SESSION)
from .utils import TAPPED, UNTAPPED


class ServerFingerTappingTask:
    def __init__(self, to_client_connections: list, from_client_connections: dict) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

        self._state = {}
        for client_name in from_client_connections.values():
            self._state[client_name] = UNTAPPED

        csv_data_path = "./data/finger_tapping"

        if not os.path.exists(csv_data_path):
            os.makedirs(csv_data_path)

        self._csv_file = open(csv_data_path + '/' + str(int(time())) + ".csv", 'w', newline='')
        self._csv_writer = csv.writer(self._csv_file, delimiter=';')

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

        self._csv_file.close()

        data = {}
        data["type"] = "request"
        data["request"] = "end"

        send(self._to_client_connections, data)

        print("[STATUS] Finger tapping task ended")

    def _to_client_update_state(self):
        session_index = -1
        counter_target = SECONDS_COUNT_DOWN

        start_ticks = pygame.time.get_ticks()

        seconds = 0.0

        clock = pygame.time.Clock()
        while self._running:
            if seconds >= counter_target:
                session_index += 1

                if session_index >= len(SESSION):
                    self._running = False
                    break

                counter_target = SECONDS_PER_SESSION[session_index]
                start_ticks = pygame.time.get_ticks()

            data = {}
            data["type"] = "state"
            data["state"] = self._state
            data["reveal"] = 1 if session_index < 0 else SESSION[session_index]
            data["session_index"] = session_index

            seconds_to_send = int(counter_target) - int(seconds)
            data["seconds"] = 1 if seconds_to_send <= 0 else seconds_to_send

            # Record state of the game
            if session_index >= 0:
                self._csv_writer.writerow([time(), json.dumps(data)])

            send(self._to_client_connections, data)

            seconds = (pygame.time.get_ticks() - start_ticks) / 1000.0

            clock.tick(UPDATE_RATE)

    def _from_client_commands(self):
        while self._running:
            all_data = receive(self._from_client_connections.keys(), 0.1)

            for data in all_data:
                if data["type"] == "command":
                    if data["command"] == "tap":
                        self._state[data["sender"]] = TAPPED
                    else:
                        self._state[data["sender"]] = UNTAPPED
