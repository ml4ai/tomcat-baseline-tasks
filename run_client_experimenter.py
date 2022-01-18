import argparse

import pygame

from config import DEFAULT_SERVER_ADDR
from instructions import (ping_pong_task_competitive_instruction,
                          wait_for_experimenter)
from network import Client
from tasks.ping_pong_task import ClientPingPongTask

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run client of finger tapping task.')
    parser.add_argument("-a", "--address", metavar='', help="IP address of server")
    parser.add_argument("-p", "--port", type=int, required=True, metavar='', help="Port of server")
    parser.add_argument("-n", "--name", required=True, metavar='', help="Name of client")
    args = parser.parse_args()

    server_address = DEFAULT_SERVER_ADDR if args.address is None else args.address
    server_port = args.port
    client_name = args.name

    pygame.init()
    pygame.mouse.set_visible(False)

    client = Client(server_address, server_port, client_name)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    ping_pong_task_competitive_instruction(screen)

    wait_for_experimenter(client.to_server, screen, client.client_name)

    client_ping_pong_task = ClientPingPongTask(client.from_server, 
                                               client.to_server, 
                                               screen, 
                                               client.client_name)
    client_ping_pong_task.run()

    client.close()
