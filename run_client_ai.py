import argparse

import pygame

from config import DEFAULT_SERVER_ADDR
from network import Client
from tasks.ping_pong_task import ClientAIPingPongTask

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run client of finger tapping task.')
    parser.add_argument("-a", "--address", metavar='', help="IP address of server")
    parser.add_argument("-p", "--port", type=int, required=True, metavar='', help="Port of server")
    parser.add_argument("-n", "--name", default="ai", metavar='', help="Name of client")
    args = parser.parse_args()

    server_address = DEFAULT_SERVER_ADDR if args.address is None else args.address
    server_port = args.port
    client_name = args.name

    assert "ai" in client_name

    pygame.init()

    client = Client(server_address, server_port, client_name, screen=False)

    client_ai_ping_pong_task = ClientAIPingPongTask(client.from_server, 
                                                    client.to_server,
                                                    client.client_name,
                                                    easy_mode=False)
    client_ai_ping_pong_task.run()

    client.close()
