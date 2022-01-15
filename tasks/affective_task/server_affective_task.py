from time import time

from common import receive_all, send

from .utils import get_image_paths


class ServerAffectiveTask:
    def __init__(self, to_client_connections: list, from_client_connections: dict) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

    def run(self):
        image_paths = get_image_paths("./images/task_images")
        

        data = {}
        data["type"] = "request"
        data["request"] = "end"

        send(self._to_client_connections, data)

        print("[STATUS] Affective task ended")
