import sys
from typing import Tuple
import pygame

from routes.level_builder_menu import LevelBuilderMenu
from routes.multiplayer import MultiplayerGame
from routes.route import Route
from routes.singleplayer import Singleplayer
from utils.button import Button


class Menu(Route):

    def __init__(self, win_size: Tuple[int, int]):
        self.color = (200, 200, 200)  # TODO change to picture
        self.buttons = [
            Button("SINGLEPLAYER", 40,
                   (win_size[0] // 2 - 200, win_size[1] // 2 - 300, 400, 100),
                   (0, 200, 100), (0, 150, 100)),
            Button(
                "MULTIPLAYER", 40,
                (win_size[0] // 2 - 200, win_size[1] // 2 - 100, 400, 100),
                (200, 100, 100), (150, 100, 100)
            ),
            Button(
                "LEVEL BUILDER", 40, (win_size[0] // 2 - 200, win_size[1] // 2 + 100, 400, 100),
                (200, 100, 200),
                (150, 100, 200)),
        ]

    def draw(self, win: pygame.Surface) -> None:
        win.fill(self.color)

        for button in self.buttons:
            button.draw(win)

    def update_state(self) -> 'Route':

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if self.buttons[0].is_mouse(event):
                return Singleplayer()
            if self.buttons[1].is_mouse(event):
                return MultiplayerGame()
            if self.buttons[2].is_mouse(event):
                return LevelBuilderMenu()

        return self
