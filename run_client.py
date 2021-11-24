import argparse

import pygame

from common import DEFAULT_SERVER_ADDR
from instructions import (exit_instruction, finger_tapping_task_instruction,
                          ping_pong_task_competitive_instruction,
                          ping_pong_task_cooperative_instruction)
from network import Client
from tasks.finger_tapping_task import ClientFingerTappingTask
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

    finger_tapping_task_instruction(client.to_server, client.screen, client.client_name)

    client_finger_tapping_task = ClientFingerTappingTask(client.from_server, 
                                                         client.to_server, 
                                                         client.screen, 
                                                         client.client_name)
    client_finger_tapping_task.run()

    ping_pong_task_competitive_instruction(client.to_server, client.screen, client.client_name)

    client_finger_tapping_task = ClientPingPongTask(client.from_server, 
                                                    client.to_server, 
                                                    client.screen, 
                                                    client.client_name)
    client_finger_tapping_task.run()

    ping_pong_task_cooperative_instruction(client.to_server, client.screen, client.client_name)

    client_finger_tapping_task = ClientPingPongTask(client.from_server, 
                                                    client.to_server, 
                                                    client.screen, 
                                                    client.client_name)
    client_finger_tapping_task.run()

    exit_instruction(client.to_server, client.screen, client.client_name)

    client.close()
