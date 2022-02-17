import pygame
from common import (cursor_visibility, render_blank_screen,
                    set_cursor_position, wait)
from config import CLIENT_WINDOW_HEIGHT, CLIENT_WINDOW_WIDTH
from network import receive, send

from .config_affective_task import (BLANK_SCREEN_MILLISECONDS,
                                    CROSS_SCREEN_MILLISECONDS)
from .utils import Button, render_image_center, render_text_center, timer

class ClientAffectiveTask:
    def __init__(self, from_server, to_server, screen):
        self._from_server = from_server
        self._to_server = to_server
        self._screen = screen

    def run(self, collaboration: bool = False):
        valence_buttons = []
        valence_buttons.append(Button((-345, 220), self._screen))
        valence_buttons.append(Button((-175, 220), self._screen))
        valence_buttons.append(Button((-2, 220), self._screen))
        valence_buttons.append(Button((173, 220), self._screen))
        valence_buttons.append(Button((343, 220), self._screen))

        arousal_buttons = []
        arousal_buttons.append(Button((-345, -130), self._screen))
        arousal_buttons.append(Button((-175, -130), self._screen))
        arousal_buttons.append(Button((-2, -130), self._screen))
        arousal_buttons.append(Button((173, -130), self._screen))
        arousal_buttons.append(Button((343, -130), self._screen))

        print("[STATUS] Running affective task")

        while True:
            discuss = True

            [data] = receive([self._from_server])

            if data["type"] == "request":
                if data["request"] == "end":
                    break
            elif data["type"] == "state":
                state = data["state"]
            else:
                # Read the next message
                continue

            # show a blank screen and a cross before showing an image
            render_blank_screen(self._screen, BLANK_SCREEN_MILLISECONDS)

            render_image_center("./tasks/affective_task/images/plus.png", self._screen, refresh=True)
            wait(CROSS_SCREEN_MILLISECONDS)

            # show an image
            render_image_center(state["image_path"], self._screen, refresh=True)

            # show timer above image until timer runs out
            timer(state["image_timer"], [], "Team: " if collaboration else "Individual: ", self._screen)

            if collaboration:
                if discuss == True:
                    # show the same image again
                    render_image_center(state["image_path"], self._screen, refresh=True)
                    stmnt = "Discuss"
                    render_text_center(stmnt, (950, 50), self._screen, font_size = 45 , x_offset = 0, y_offset=450)
                    timer(state["discussion_timer"], [], "Team: ", self._screen)
                    discuss = False
                else:
                    discuss = True
            
            # show valence and arousal scoring
            render_image_center("./tasks/affective_task/images/buttons_images/Valence.jpg", 
                                self._screen, 
                                y_offset=-150, 
                                refresh=True)
            render_image_center("./tasks/affective_task/images/buttons_images/Arousal.jpg", 
                                self._screen, 
                                y_offset=200)
                                       
            render_text_center("Valence score", (400, 50), self._screen, y_offset=-270)
            render_text_center("Frowning", (300, 50), self._screen, font_size=30, x_offset=-530, y_offset=-120)
            render_text_center("Happy", (300, 50), self._screen, font_size = 30, x_offset=530, y_offset=-120)
            
            render_text_center("-2", (300, 50), self._screen, font_size=25, x_offset=-340, y_offset=-55)
            render_text_center("-1", (300, 50), self._screen, font_size=25, x_offset=-165, y_offset=-55)
            render_text_center("0", (300, 50), self._screen, font_size=25, x_offset = 0, y_offset=-55)
            render_text_center("+1", (300, 50), self._screen, font_size=25, x_offset=165, y_offset=-55)
            render_text_center("+2", (300, 50), self._screen, font_size=25, x_offset=335, y_offset=-55)

            render_text_center("Arousal score", (400, 50), self._screen, y_offset=80)
            render_text_center("Calm", (300, 50), self._screen, font_size=30, x_offset=-540, y_offset=220)
            render_text_center("Excited", (300, 50), self._screen, font_size=30, x_offset=530,y_offset=220)
            
            render_text_center("-2", (300, 50), self._screen, font_size=25, x_offset=-340, y_offset=290)
            render_text_center("-1", (300, 50), self._screen, font_size=25, x_offset=-165, y_offset=290)
            render_text_center("0", (300, 50), self._screen, font_size=25, x_offset=0, y_offset=290)
            render_text_center("+1", (300, 50), self._screen, font_size=25, x_offset=165, y_offset=290)
            render_text_center("-2", (300, 50), self._screen, font_size=25, x_offset=335, y_offset=290)

            remove_button_frame = collaboration and not state["selected"]

            for button in arousal_buttons:
                button.unselect(remove_button_frame)

            for button in valence_buttons:
                button.unselect(remove_button_frame)

            set_cursor_position(CLIENT_WINDOW_WIDTH / 2, CLIENT_WINDOW_HEIGHT / 2)
            
            if not collaboration or state["selected"]:
                cursor_visibility(True)

            # render button response while timer is running
            def button_response(events):
                if not collaboration or state["selected"]:
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # Check arousal buttons
                            for i, button in enumerate(arousal_buttons):
                                if button.object.collidepoint(pygame.mouse.get_pos()):
                                    button.select()
                                    for j, each_button in enumerate(arousal_buttons):
                                        if j != i:
                                            each_button.unselect()

                                    if collaboration:
                                        update = {
                                            "type": "update",
                                            "update": {
                                                "rating_type": "arousal",
                                                "rating_index": i
                                            }
                                        }
                                        send([self._to_server], update)

                                    break

                            # Check valence buttons
                            else:
                                for i, button in enumerate(valence_buttons):
                                    if button.object.collidepoint(pygame.mouse.get_pos()):
                                        button.select()
                                        for j, each_button in enumerate(valence_buttons):
                                            if j != i:
                                                each_button.unselect()

                                        if collaboration and state["selected"]:
                                            update = {
                                                "type": "update",
                                                "update": {
                                                    "rating_type": "valence",
                                                    "rating_index": i
                                                }
                                            }
                                            send([self._to_server], update)

                                        break
                else:
                    data = receive([self._from_server], 0.0)
                    if data:
                        data = data[0]
                        if data["type"] == "update":
                            update = data["update"]
                            if update["rating_type"] == "arousal":
                                arousal_buttons[update["rating_index"]].select()
                                for j, button in enumerate(arousal_buttons):
                                    if j != update["rating_index"]:
                                        button.unselect(no_frame=True)
                            else:
                                valence_buttons[update["rating_index"]].select()
                                for j, button in enumerate(valence_buttons):
                                    if j != update["rating_index"]:
                                        button.unselect(no_frame=True)


            timer(state["rating_timer"], [button_response], "Team: " if collaboration else "Individual: ", self._screen)

            if not collaboration or state["selected"]:
                cursor_visibility(False)

                # send valence and arousal data to server
                arousal = None
                for i, button in enumerate(arousal_buttons):
                    if button.is_selected():
                        arousal = i - 2
                        break

                valence = None
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
