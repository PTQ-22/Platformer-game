import sys
from typing import List

import pygame

from player.player import Player
from routes.route import Route
from utils.field import Field


class Singleplayer(Route):

    def __init__(self):
        self.grid: List[List[Field]] = []
        self.field_size = 50
        self.make_grid()

        self.player = Player(1, 10, 10)

    def make_grid(self):
        for i in range(0, 1000, self.field_size):
            self.grid.append([])
            for j in range(0, 700, self.field_size):
                self.grid[i // self.field_size].append(Field(i, j, self.field_size))
        with open("res/singleplayer_board.txt") as file:
            x = file.readlines()
            for i, line in enumerate(x):
                for j, c in enumerate(line):
                    if c == '\n':
                        break
                    if c == '#':
                        self.grid[j][i].color = (0, 0, 0)
                        self.grid[j][i].type = '#'

    def draw(self, win: pygame.Surface) -> None:
        for row in self.grid:
            for field in row:
                field.draw(win)
        self.player.draw(win)

    def update_state(self) -> 'Route':
        self.player.update(self.grid, [])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self
