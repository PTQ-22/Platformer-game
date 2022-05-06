import os
import sys

import pygame

from level_builder.level_builder import LevelBuilder
from routes.route import Route
from routes.singleplayer import Singleplayer
from utils.button import Button


class LevelBuilderMenu(Route):

    def __init__(self):
        self.color = (200, 200, 200)
        self.menu_button = Button("MENU", 15, (10, 10, 60, 30), (0, 200, 0), (0, 150, 0))
        self.add_button = Button("ADD NEW", 30, (300, 10, 400, 80), (0, 200, 0), (0, 150, 0))
        self.level_buttons = []
        filenames = sorted(os.listdir("boards/builder_boards"))
        for i, name in enumerate(filenames):
            self.level_buttons.append(
                Button(name.upper()[:-4], 30, (300, 130 + i * 100, 400, 80), (0, 0, 200), (0, 0, 150))
            )

    def draw(self, win: pygame.Surface) -> None:
        win.fill(self.color)
        self.menu_button.draw(win)
        self.add_button.draw(win)
        for button in self.level_buttons:
            button.draw(win)

    def update_state(self) -> 'Route':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if self.menu_button.is_mouse(event):
                from routes.menu import Menu
                return Menu((1000, 700))
            if self.add_button.is_mouse(event):
                return LevelBuilder(len(self.level_buttons) + 1)
            for button in self.level_buttons:
                if button.is_mouse(event):
                    return Singleplayer(button.text.lower())
        return self

