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
        self.is_add_active = True
        self.level_buttons = []
        self.del_buttons = []
        filenames = sorted(os.listdir("boards/builder_boards"))
        for i, name in enumerate(filenames):
            self.level_buttons.append(
                Button(name.upper()[:-4], 30, (300, 130 + i * 100, 400, 80), (0, 0, 200), (0, 0, 150))
            )
            self.del_buttons.append(
                Button("X", 30, (750, 150 + i * 100, 50, 40), (200, 0, 0), (150, 0, 0))
            )

    def draw(self, win: pygame.Surface) -> None:
        win.fill(self.color)
        self.menu_button.draw(win)
        self.add_button.draw(win)
        for button in self.level_buttons:
            button.draw(win)
        for del_button in self.del_buttons:
            del_button.draw(win)

    def update_state(self) -> 'Route':
        if len(self.level_buttons) >= 5:
            self.is_add_active = False
            self.add_button.color = (100, 100, 100)
            self.add_button.hover_color = (70, 70, 70)
        else:
            self.is_add_active = True
            self.add_button.color = (0, 200, 0)
            self.add_button.hover_color = (0, 150, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if self.menu_button.is_mouse(event):
                from routes.menu import Menu
                return Menu((1000, 700))
            if self.add_button.is_mouse(event) and self.is_add_active:
                maxi = 0
                for button in self.level_buttons:
                    s = button.text.split()
                    maxi = max(int(s[1]), maxi)
                return LevelBuilder(maxi + 1)
            for button in self.level_buttons:
                if button.is_mouse(event):
                    return Singleplayer(button.text.lower())
            for i, del_button in enumerate(self.del_buttons):
                if del_button.is_mouse(event):
                    self.del_level(i, del_button)
        return self

    def del_level(self, i: int, del_butt: Button):
        self.del_level_file(self.level_buttons[i].text.lower())
        self.del_buttons.remove(del_butt)
        del self.level_buttons[i]
        for i, button in enumerate(self.level_buttons):
            if button.rect.y > del_butt.rect.y:
                button.move_y(-100)
                self.del_buttons[i].move_y(-100)

    @staticmethod
    def del_level_file(text: str):
        os.remove(f"boards/builder_boards/{text}.txt")
