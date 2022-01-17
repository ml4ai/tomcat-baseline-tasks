import pygame
from common import receive, send

from .utils import Button, render_image_center, timer


class ClientAffectiveTask:
    def __init__(self, from_server, to_server, screen) -> None:
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen

    def run(self):
        arousal_buttons = []
        arousal_buttons.append(Button((-400, -50), "-2", self._screen))
        arousal_buttons.append(Button((-200, -50), "-1", self._screen))
        arousal_buttons.append(Button((0, -50), "0", self._screen))
        arousal_buttons.append(Button((200, -50), "+1", self._screen))
        arousal_buttons.append(Button((400, -50), "+2", self._screen))

        valence_buttons = []
        valence_buttons.append(Button((-400, 350), "+2", self._screen))
        valence_buttons.append(Button((-200, 350), "+1", self._screen))
        valence_buttons.append(Button((0, 350), "0", self._screen))
        valence_buttons.append(Button((200, 350), "-1", self._screen))
        valence_buttons.append(Button((400, 350), "-2", self._screen))

        print("[STATUS] Running affective task")

        while True:
            [data] = receive([self._from_server])

            if data["type"] == "request":
                if data["request"] == "end":
                    break

            state = data["state"]
            render_image_center(state["image_path"], self._screen, refresh=True)
            
            timer(state["image_timer"], [], "Team: " if state["collaboration"] else "Individual: ", self._screen)

            render_image_center("./tasks/affective_task/images/buttons_images/Valence.jpg", 
                                self._screen, 
                                y_offset=-200, 
                                refresh=True)
            render_image_center("./tasks/affective_task/images/buttons_images/Arousal.jpg", 
                                self._screen, 
                                y_offset=200)

            for button in arousal_buttons:
                button.render()

            for button in valence_buttons:
                button.render()

            def button_response():
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check arousal buttons
                        for i, button in enumerate(arousal_buttons):
                            if button.object.collidepoint(pygame.mouse.get_pos()):
                                button.select()
                                for j, each_button in enumerate(arousal_buttons):
                                    if j != i:
                                        each_button.unselect()
                                break

                        # Check valence buttons
                        else:
                            for i, button in enumerate(valence_buttons):
                                if button.object.collidepoint(pygame.mouse.get_pos()):
                                    button.select()
                                    for j, each_button in enumerate(valence_buttons):
                                        if j != i:
                                            each_button.unselect()
                                    break

            timer(state["rating_timer"], [button_response], "Team: " if state["collaboration"] else "Individual: ", self._screen)

            arousal = 0
            for i, button in enumerate(arousal_buttons):
                if button.is_selected():
                    arousal = i - 2
                    break

            valence = 0
            for i, button in enumerate(valence_buttons):
                if button.is_selected():
                    valence = 2 - i
                    break

            response = {
                "type": "rating",
                "rating": {
                    "arousal": arousal,
                    "valence": valence
                }
            }

            send([self._to_server], response)

        print("[STATUS] Affective task ended")
