import socket
import sys
import threading
from select import select

from common import get_terminal_command, receive


class Server:
    def __init__(self, host: str, port: int) -> None:
        # Establish connection where clients can get game state update
        self._to_client_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._to_client_request.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse socket
        self._to_client_request.bind((host, port))
        self._to_client_request.setblocking(False)

        # Establish connection where clients send control commands
        self._from_client_request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._from_client_request.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Reuse socket
        self._from_client_request.bind((host, port + 1))
        self._from_client_request.setblocking(False)

        print(f"Address: {host}, {port}")

        self.to_client_connections = []
        self.from_client_connections = {}

        self._establishing_connections = False

    def establish_connections(self) -> None:
        self._establishing_connections = True

        to_client_request_thread = threading.Thread(target=self._dispatch_to_client_request, daemon=True)
        to_client_request_thread.start()

        from_client_request_thread = threading.Thread(target=self._dispatch_from_client_request, daemon=True)
        from_client_request_thread.start()

        terminal_input_thread = threading.Thread(target=self._terminal_input, daemon=True)
        terminal_input_thread.start()

        print("[STATUS] Establishing connections")

        # Wait for threads to finish
        to_client_request_thread.join()
        from_client_request_thread.join()
        terminal_input_thread.join()

        print("[STATUS] Closed connection gate")

    def close_connections(self) -> None:
        self._to_client_request.close()
        self._from_client_request.close()

    def _dispatch_to_client_request(self) -> None:
        """
        Dispatch client's connection for receiving game state updates from server
        """
        # Listen for client connection
        self._to_client_request.listen()

        while self._establishing_connections:
            # Check for connection request
            readable, _, _ = select([self._to_client_request], [], [self._to_client_request], 0.1)

            for connection in readable:
                client_conn, client_addr = connection.accept()
                client_conn.setblocking(False)

                self.to_client_connections.append(client_conn)

                print("Sending replies to [" + client_addr[0] + ", " + str(client_addr[1]) + ']')

    def _dispatch_from_client_request(self) -> None:
        """
        Establish connection to receive clients' command
        """
        # Listen for client connection
        self._from_client_request.listen()

        while self._establishing_connections:
            # Check for connection request
            readable, _, _ = select([self._from_client_request], [], [self._from_client_request], 0.1)

            for connection in readable:
                client_conn, client_addr = connection.accept()
                client_conn.setblocking(False)

                [client_name] = receive([client_conn])

                self.from_client_connections[client_conn] = client_name

                print("Receiving commands from [" + client_name + ", " + client_addr[0] + ", " + str(client_addr[1]) + ']')

    def _terminal_input(self):
        """
        Control the server 
        """
        while self._establishing_connections:
            command = get_terminal_command(wait_time=0.5)

            if command is None:
                continue

            if command == "h" or command == "help":
                print("-----")
                print("close: Stop establishing new connections")
                print("h or help: List available commands")
                print("-----")

            elif command == "close":
                self._establishing_connections = False

            else:
                print("Unknown command")
