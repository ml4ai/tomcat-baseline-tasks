from common import receive, send

from .utils import render_image_center


class ClientAffectiveTask:
    def __init__(self, from_server, to_server, screen) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen

    def run(self):
        print("[STATUS] Running affective task")

        while True:
            [data] = receive([self._from_server])

            if data["type"] == "request":
                if data["request"] == "end":
                    break

            state = data["state"]
            render_image_center(state["image_path"], self._screen)
            input()

            render_image_center("./tasks/affective_task/images/buttons_images/Valence.jpg", 
                                self._screen, 
                                y_offset=-200, 
                                refresh=True)
            render_image_center("./tasks/affective_task/images/buttons_images/Arousal.jpg", 
                                self._screen, 
                                y_offset=200)
            input()

            # TODO: submit valid responses
            response = {
                "type": "response",
                "response": "test test test"
            }

            send([self._to_server], response)

        print("[STATUS] Affective task ended")
