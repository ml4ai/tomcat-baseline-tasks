import socket

import pygame
from common import receive, send


class Client:
    def __init__(self, host: str, port: int, client_name: str, screen: bool = True) -> None:
        self.client_name = client_name

        self.from_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.from_server.connect((host, port))
        self.from_server.setblocking(False)

        send([self.from_server], self.client_name)
        [data] = receive([self.from_server])
        if data["type"] != "status" or data["status"] == "failed":
            raise RuntimeError("[ERROR] Connection to from_server failed")

        self.to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.to_server.connect((host, port + 1))
        self.to_server.setblocking(False)

        send([self.to_server], self.client_name)
        [data] = receive([self.to_server])
        if data["type"] != "status" or data["status"] == "failed":
            raise RuntimeError("[ERROR] Connection to to_server failed")

        print("[INFO] Connected to server")

        if screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def close(self):
        data = {}
        data["type"] = "request"
        data["request"] = "close"
        data["sender"] = self.client_name

        send([self.to_server], data)

        self.from_server.close()
        self.to_server.close()

        print("[INFO] Closed connection to server")
