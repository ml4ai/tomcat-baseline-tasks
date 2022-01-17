from common import receive, send


class ClientAffectiveTask:
    def __init__(self, from_server, to_server, screen) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen

    def run(self):
        print("[STATUS] Running affective task")

        while True:
            data = receive([self._from_server])

            if data["type"] == "request":
                if data["request"] == "end":
                    break

            # TODO: Display data

            # TODO: submit valid responses
            response = {
                "type": "response",
                "response": "test test test"
            }

            send([self._to_server], response)

        print("[STATUS] Affective task ended")
