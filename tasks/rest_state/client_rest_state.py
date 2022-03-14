from common import (cursor_visibility, render_blank_screen,
                    set_cursor_position, wait)
from config import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH
from network import receive, send

from .config_rest_state import (BLANK_SCREEN_MILLISECONDS,
                                    CROSS_SCREEN_MILLISECONDS)
from .utils import (render_text_center, timer)

class ClientRestState:
    def __init__(self, from_server, to_server, screen):
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen

    def run(self):
        print("[STATUS] Running Rest state")

        while True:

            [data] = receive([self._from_server])
            print(data)
            if data["type"] == "request":
                if data["request"] == "end":
                    print('im in break')
                    break
            elif data["type"] == "state":
                print('Im in state')
                state = data["state"]
                print(state)
            else:
                # Read the next message
                continue      

            # show a blank screen and a cross before showing an image
            render_blank_screen(self._screen, BLANK_SCREEN_MILLISECONDS)

            wait(CROSS_SCREEN_MILLISECONDS)

            timer(state["rest_timer"], [], "Please sit back, relax and try not to move for: ", self._screen)
            response = {"type": "STOP"}
            send([self._to_server], response)
        print("[STATUS] Affective task ended")