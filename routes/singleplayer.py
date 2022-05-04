import sys
from typing import List

import pygame

from player.player import Player
from routes.route import Route
from utils.coin import Coin
from utils.field import Field
from utils.level_bar import LevelBar


class Singleplayer(Route):

    def __init__(self):
        self.grid: List[List[Field]] = []
        self.field_size = 50
        self.coins: List[Coin] = []
        self.make_grid()
        self.level_camera_speed = 0
        self.player = Player(1, 360, 70)
        self.level_bar = LevelBar(self.field_size)

    def make_grid(self):
        with open('res/singleplayer_board.txt') as file:
            x = file.readlines()
            for i, line in enumerate(x):
                # add barrier field
                self.grid.append([Field(-self.field_size, (i+1) * self.field_size, self.field_size, 'b')])
                for j, c, in enumerate(line):
                    if c == '\n':
                        break
                    self.grid[i].append(Field(j * self.field_size, (i+1) * self.field_size, self.field_size))
                    if c == '#':
                        self.grid[i][j+1].color = (0, 0, 0)
                        self.grid[i][j+1].type = '#'
                    if c == 'c':
                        self.coins.append(Coin(self.grid[i][j+1].rect.centerx, self.grid[i][j+1].rect.centery))
                # add barrier field
                self.grid[i].append(Field(j * self.field_size, (i+1) * self.field_size, self.field_size, 'b'))

    def draw(self, win: pygame.Surface) -> None:
        for row in self.grid:
            for field in row:
                field.draw(win)
        self.player.draw(win)
        for coin in self.coins:
            coin.draw(win)
        self.level_bar.draw(win)

    def update_state(self) -> 'Route':
        self.camera()
        self.update_tiles()
        self.player.update(self.grid, [])

        for coin in self.coins:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.level_bar.increse_coin_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if self.level_bar.menu_button.is_mouse(event):
                from routes.menu import Menu
                return Menu((1000, 700))
        return self

    def camera(self):
        move = False
        if self.player.direction == "right" and self.player.is_moving:
            if self.player.rect.centerx >= 800:
                self.player.speed = 0
                self.level_camera_speed = -2
                move = True
        if self.player.direction == "left" and self.player.is_moving:
            if self.player.rect.centerx <= 200:
                self.player.speed = 0
                self.level_camera_speed = 2
                move = True
        if not move:
            self.player.speed = 2
            self.level_camera_speed = 0

    def update_tiles(self):
        if self.level_camera_speed != 0:
            player_blocks_state = self.player.is_on_block(self.grid)
            for field_list in self.grid:
                for field in field_list:
                    if "left" not in player_blocks_state and "right" not in player_blocks_state:
                        field.rect.x += self.level_camera_speed
            for coin in self.coins:
                if "left" not in player_blocks_state and "right" not in player_blocks_state:
                    coin.rect.x += self.level_camera_speed
