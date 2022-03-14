import csv
import json
import os
from time import sleep, time

from common import record_metadata, request_clients_end
from network import receive, receive_all, send

from .config_rest_state import (BLANK_SCREEN_MILLISECONDS,
                                    CROSS_SCREEN_MILLISECONDS,
                                    REST_TIMER)

class ServerRestState:
    def __init__(self, to_client_connections: list, from_client_connections: dict) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

        # metadata = {}
        # metadata["blank_screen_milliseconds"] = BLANK_SCREEN_MILLISECONDS
        # metadata["cross_screen_milliseconds"] = CROSS_SCREEN_MILLISECONDS
        # metadata["rest_timer"] = REST_TIMER

    def run(self):

            data = {}
            data["type"] = "state"
            data["state"] = {}
            data["state"]["rest_timer"] = REST_TIMER

            print("[STATUS] Running rest state")
            send(self._to_client_connections, data)
            
            sleep(0.1)

            while(True):
                responses = receive(self._from_client_connections)
                response = list(responses.values())[0]
                if response["type"] == "STOP":
                    #break
                    request_clients_end(self._to_client_connections)
                    print("[STATUS] Rest state has ended")

