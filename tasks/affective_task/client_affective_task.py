import pygame
from common import receive, send

from .utils import REFRESH_RATE, Button, render_image_center


class ClientAffectiveTask:
    def __init__(self, from_server, to_server, screen) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen

    def run(self):
        button_arousal_minus_2 = Button((-400, -50), "-2", self._screen)
        button_arousal_minus_1 = Button((-200, -50), "-1", self._screen)
        button_arousal_0 = Button((0, -50), "0", self._screen)
        button_arousal_plus_1 = Button((200, -50), "+1", self._screen)
        button_arousal_plus_2 = Button((400, -50), "+2", self._screen)

        button_valence_plus_2 = Button((-400, 350), "+2", self._screen)
        button_valence_plus_1 = Button((-200, 350), "+1", self._screen)
        button_valence_0 = Button((0, 350), "0", self._screen)
        button_valence_minus_1 = Button((200, 350), "-1", self._screen)
        button_valence_minus_2 = Button((400, 350), "-2", self._screen)

        button_submit = Button((0, 450), "Submit", self._screen)

        clock = pygame.time.Clock()

        print("[STATUS] Running affective task")

        while True:
            [data] = receive([self._from_server])

            if data["type"] == "request":
                if data["request"] == "end":
                    break

            state = data["state"]
            render_image_center(state["image_path"], self._screen, refresh=True)
            input()

            render_image_center("./tasks/affective_task/images/buttons_images/Valence.jpg", 
                                self._screen, 
                                y_offset=-200, 
                                refresh=True)
            render_image_center("./tasks/affective_task/images/buttons_images/Arousal.jpg", 
                                self._screen, 
                                y_offset=200)

            button_arousal_minus_2.render()
            button_arousal_minus_1.render()
            button_arousal_0.render()
            button_arousal_plus_1.render()
            button_arousal_plus_2.render()

            button_valence_plus_2.render()
            button_valence_plus_1.render()
            button_valence_0.render()
            button_valence_minus_1.render()
            button_valence_minus_2.render()

            button_submit.render()

            submitted = False
            while not submitted:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_submit.object.collidepoint(pygame.mouse.get_pos()):
                            print("Submitted")
                            submitted = True

                clock.tick(REFRESH_RATE)

            # TODO: submit valid responses
            response = {
                "type": "response",
                "response": "test test test"
            }

            send([self._to_server], response)

        print("[STATUS] Affective task ended")
