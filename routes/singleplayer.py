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
        self.level_camera_speed = 0

        self.player = Player(1, 360, 10)

    def make_grid(self):
        with open('res/singleplayer_board.txt') as file:
            x = file.readlines()
            for i, line in enumerate(x):
                self.grid.append([])
                for j, c, in enumerate(line):
                    if c == '\n':
                        break
                    self.grid[i].append(Field(j * self.field_size, i * self.field_size, self.field_size))
                    if c == '#':
                        self.grid[i][j].color = (0, 0, 0)
                        self.grid[i][j].type = '#'

    def draw(self, win: pygame.Surface) -> None:
        for row in self.grid:
            for field in row:
                field.draw(win)
        self.player.draw(win)

    def update_state(self) -> 'Route':
        self.camera()
        self.update_fields()
        self.player.update(self.grid, [])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self

    def camera(self):
        if self.player.direction == "right" and self.player.is_moving:
            if self.player.rect.centerx >= 800:
                self.player.speed = 0
                self.level_camera_speed = -2
        elif self.player.direction == "left" and self.player.is_moving:
            if self.player.rect.centerx <= 200:
                self.player.speed = 0
                self.level_camera_speed = 2
        else:
            self.player.speed = 2
            self.level_camera_speed = 0

    def update_fields(self):
        for field_list in self.grid:
            for field in field_list:
                field.rect.x += self.level_camera_speed
