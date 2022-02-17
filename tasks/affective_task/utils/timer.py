from typing import Callable, List

import pygame

from .render_text_center import render_text_center

from ..config_affective_task import DISCUSSION_TIMER

REFRESH_RATE = 20

TIM = 0

def timer(seconds: int, callbacks: List[Callable], pre_text: str, screen, Rating = False):
    start_ticks = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    while True:
        events = pygame.event.get()

        for callback in callbacks:
            callback(events)

        seconds_has_passed = (pygame.time.get_ticks() - start_ticks) / 1000.0
        seconds_left_to_count = seconds - seconds_has_passed
        if seconds_left_to_count < 0.0:
            break
        else:
            seconds_left_to_count = 0 if seconds_left_to_count < 0.0 else int(seconds_left_to_count)
            TIM = seconds_left_to_count
            render_text_center(pre_text + str(seconds_left_to_count + 1), (300, 50), screen, y_offset=-420)

    clock.tick(REFRESH_RATE)
