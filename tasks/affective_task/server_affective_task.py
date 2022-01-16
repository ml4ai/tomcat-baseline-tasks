import csv
import json
import os
from time import time

from common import receive_all, send

from .utils import get_image_paths


class ServerAffectiveTask:
    def __init__(self, 
                 to_client_connections: list, 
                 from_client_connections: dict, 
                 image_timer: float, 
                 rating_timer: float) -> None:
        self._to_client_connections = to_client_connections
        self._from_client_connections = from_client_connections
        self._image_timer = image_timer
        self._rating_timer = rating_timer

        data_path = "./data/affective"

        if not os.path.exists(data_path):
            os.makedirs(data_path)

        csv_file_name = data_path + '/' + str(int(time()))

        self._csv_file = open(csv_file_name + ".csv", 'w', newline='')
        self._csv_writer = csv.writer(self._csv_file, delimiter=';')

    def run(self):
        image_paths = sorted(get_image_paths("./images/task_images"))

        for image_path in image_paths:
            data = {}
            data["type"] = "state"
            data["state"] = {
                "image_path": image_path,
                "image_timer": self._image_timer,
                "rating_timer": self._rating_timer
            }
            send(self._to_client_connections, data)
            data = receive_all(self._from_client_connections)

            current_time = time()
            for client_name, each_data in data.items():
                if each_data["type"] == "response":
                    self._csv_writer.writerow([current_time, image_path, client_name, json.dumps(each_data["response"])])

        data = {}
        data["type"] = "request"
        data["request"] = "end"

        send(self._to_client_connections, data)

        print("[STATUS] Affective task ended")
