from common import receive


class ClientFingerTappingTask:
    def __init__(self, from_server, to_server) -> None:
        self._from_server = from_server
        self._to_server = to_server

        self._running = False

    def run(self):
        self._running = True

        print("[STATUS] Running client finger tapping task")

        while self._running:
            data = receive([self._from_server], 0.0)
            if not data:
                continue
            else:
                [data] = data

            print(data)
