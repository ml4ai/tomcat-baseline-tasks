import argparse

import pygame

from common import render_blank_screen
from config import BLANK_SCREEN_COUNT_DOWN_MILLISECONDS, DEFAULT_SERVER_ADDR
from instructions import (exit_instruction, finger_tapping_task_instruction,
                          introduction_instruction,
                          ping_pong_task_competitive_instruction,
                          ping_pong_task_cooperative_instruction,
                          MultiSubjectAffectiveTask_Instruction,
                          wait_for_experimenter)
from network import Client
from tasks.affective_task import ClientAffectiveTask
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

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Introduction slides

    introduction_instruction(screen)
    
    # Finger tapping task

    finger_tapping_task_instruction(screen)

    wait_for_experimenter(client.to_server, client.from_server, screen)

    client_finger_tapping_task = ClientFingerTappingTask(client.from_server, 
                                                         client.to_server, 
                                                         screen, 
                                                         client.client_name)
    client_finger_tapping_task.run()

    render_blank_screen(screen, BLANK_SCREEN_COUNT_DOWN_MILLISECONDS)

    # Affective task

    # Individual
    # TODO: write instruction for affective task
    MultiSubjectAffectiveTask_Instruction(client.screen)

    wait_for_experimenter(client.to_server, client.from_server, screen)

    client_affective_task = ClientAffectiveTask(client.from_server, 
                                                client.to_server, 
                                                screen)

    client_affective_task.run()

    render_blank_screen(screen, BLANK_SCREEN_COUNT_DOWN_MILLISECONDS)

    # Team
    # TODO: write instruction for affective task
    finger_tapping_task_instruction(screen)

    wait_for_experimenter(client.to_server, client.from_server, screen)

    client_affective_task = ClientAffectiveTask(client.from_server, 
                                                client.to_server, 
                                                screen)

    client_affective_task.run()

    render_blank_screen(screen, BLANK_SCREEN_COUNT_DOWN_MILLISECONDS)

    # Ping pong competitive task

    ping_pong_task_competitive_instruction(screen)

    wait_for_experimenter(client.to_server, client.from_server, screen)

    client_ping_pong_task = ClientPingPongTask(client.from_server, 
                                               client.to_server, 
                                               screen, 
                                               client.client_name)
    client_ping_pong_task.run()

    render_blank_screen(screen, BLANK_SCREEN_COUNT_DOWN_MILLISECONDS)

    # Ping pong cooperative task

    ping_pong_task_cooperative_instruction(screen)

    wait_for_experimenter(client.to_server, client.from_server, screen)

    client_ping_pong_task = ClientPingPongTask(client.from_server, 
                                               client.to_server, 
                                               screen, 
                                               client.client_name,
                                               easy_mode=False)
    client_ping_pong_task.run()

    render_blank_screen(screen, BLANK_SCREEN_COUNT_DOWN_MILLISECONDS)

    exit_instruction(client.to_server, screen)

    client.close()
