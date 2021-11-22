import socket

from common import send


class Client:
    def __init__(self, host: str, port: int, client_name: str) -> None:
        self.client_name = client_name

        self.from_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.from_server.connect((host, port))
        self.from_server.setblocking(False)

        self.to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.to_server.connect((host, port + 1))
        self.to_server.setblocking(False)

        send([self.to_server], self.client_name)

        print("Connected to server")
