import argparse

from common import DEFAULT_SERVER_ADDR
from network import Server
from tasks.finger_tapping_task import ServerFingerTappingTask

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run server of finger tapping task.')
    parser.add_argument("-a", "--address", metavar='', help="IP address of server")
    parser.add_argument("-p", "--port", type=int, required=True, metavar='', help="Port of server")
    args = parser.parse_args()

    server_address = DEFAULT_SERVER_ADDR if args.address is None else args.address
    server_port = args.port

    server = Server(server_address, server_port)

    server.establish_connections()

    server_finger_tapping_task = ServerFingerTappingTask()
