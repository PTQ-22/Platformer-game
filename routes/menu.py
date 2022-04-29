import pygame

from utils.button import Button


class Menu:

    def __init__(self):
        # TODO change to picture
        self.color = (200, 200, 200)
        self.buttons = [
            Button("Play", 40, (100, 100, 300, 200), (200, 0, 100), (150, 0, 50)),
        ]

    def draw(self, win: pygame.Surface):
        win.fill(self.color)

        for button in self.buttons:
            button.draw(win)
