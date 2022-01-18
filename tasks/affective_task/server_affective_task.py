import csv
import json
import os
from time import time

from network import receive_all, send

from .config_affective_task import (INDIVIDUAL_IMAGE_TIMER,
                                    INDIVIDUAL_RATING_TIMER, TEAM_IMAGE_TIMER,
                                    TEAM_RATING_TIMER)
from .utils import get_image_paths


class ServerAffectiveTask:
    def __init__(self, to_client_connections: list, from_client_connections: dict) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections

        data_path = "./data/affective"

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        csv_file_name = data_path + '/' + str(int(time()))

        self._csv_file = open(csv_file_name + ".csv", 'w', newline='')
        self._csv_writer = csv.writer(self._csv_file, delimiter=';')

    def run(self, images_dir: str, collaboration: bool = False):
        # Extract images
        image_paths = sorted(get_image_paths(images_dir))
        if collaboration:
            image_paths = [path for path in image_paths if "Team" in path]
        else:
            image_paths = [path for path in image_paths if "Indivijual" in path]

        data = {}
        data["type"] = "state"
        data["state"] = {"collaboration": collaboration}

        if collaboration:
            data["state"]["image_timer"] = TEAM_IMAGE_TIMER
            data["state"]["rating_timer"] = TEAM_RATING_TIMER
        else:
            data["state"]["image_timer"] = INDIVIDUAL_IMAGE_TIMER
            data["state"]["rating_timer"] = INDIVIDUAL_RATING_TIMER

        print("[STATUS] Running affective task")

        for image_path in image_paths:
            data["state"]["image_path"] = image_path
            send(self._to_client_connections, data)
            responses = receive_all(self._from_client_connections)

            current_time = time()
            for client_name, response in responses.items():
                if response["type"] == "rating":
                    self._csv_writer.writerow([current_time, image_path, client_name, json.dumps(response["rating"])])

        data = {}
        data["type"] = "request"
        data["request"] = "end"

        send(self._to_client_connections, data)

        print("[STATUS] Affective task ended")
