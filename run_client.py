import argparse

import pygame

from client import Client
from finger_tapping_task import ClientFingerTappingTask
from network import DEFAULT_SERVER_ADDR

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

    client_finger_tapping_task = ClientFingerTappingTask()

    client = Client(server_address, server_port, client_name, client_finger_tapping_task)
    client.run()
