import sys
from typing import Tuple
import pygame

from routes.game import Game
from utils.button import Button


class Menu:

    def __init__(self, win_size: Tuple[int, int]):
        self.color = (200, 200, 200)  # TODO change to picture
        self.buttons = [
            Button(
                "PLAY", 40,
                (win_size[0] // 2 - 150, win_size[1] // 2 - 100, 300, 200),
                (200, 0, 100), (150, 0, 50)
            ),
            # Button("", 0, (100, 400, 60, 100), (0, 200, 100), (0, 200, 100))
        ]

    def draw(self, win: pygame.Surface):
        win.fill(self.color)

        for button in self.buttons:
            button.draw(win)

    def update_state(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            for button in self.buttons:  # TODO
                if button.is_mouse(event):
                    return Game()

        return self
