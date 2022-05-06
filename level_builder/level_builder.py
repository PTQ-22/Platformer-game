import os
import sys

import pygame

from routes.route import Route
from utils.button import Button


class LevelBuilder(Route):

    def __init__(self):
        self.color = (200, 200, 200)
        self.menu_button = Button("MENU", 15, (10, 10, 60, 30), (0, 200, 0), (0, 150, 0))

    def draw(self, win: pygame.Surface) -> None:
        win.fill(self.color)
        self.menu_button.draw(win)

    def update_state(self) -> 'Route':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if self.menu_button.is_mouse(event):
                from routes.level_builder_menu import LevelBuilderMenu
                return LevelBuilderMenu()
        return self

