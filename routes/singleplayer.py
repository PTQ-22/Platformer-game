import sys
from typing import List

import pygame

from player.local_player import LocalPlayer
from routes.route import Route
from utils.coin import Coin
from utils.field import Field
from utils.level_bar import LevelBar


class Singleplayer(Route):

    def __init__(self):
        self.grid: List[List[Field]] = []
        self.danger_fields: List[Field] = []
        self.field_size = 50
        self.coins: List[Coin] = []
        self.make_grid()
        self.level_camera_speed = 0
        # self.player = Player(1, 360, 70)
        self.player = LocalPlayer(1, 500, 400)
        self.level_bar = LevelBar(self.field_size)
        self.phase = 'game'
        self.font = pygame.font.Font("freesansbold.ttf", 100)

    def make_grid(self):
        with open('res/singleplayer_board.txt') as file:
            x = file.readlines()
            for i, line in enumerate(x):
                # add barrier field
                self.grid.append([Field(-self.field_size, (i + 1) * self.field_size, self.field_size, 'b')])
                for j, c, in enumerate(line):
                    if c == '\n':
                        break
                    self.grid[i].append(Field(j * self.field_size, (i + 1) * self.field_size, self.field_size))
                    if c == '#':
                        self.grid[i][j + 1].color = (0, 0, 0)
                        self.grid[i][j + 1].type = '#'
                    if c == 'A':
                        self.grid[i][j + 1].type = 'A'
                        self.danger_fields.append(self.grid[i][j + 1])
                    if c == 'c':
                        self.coins.append(Coin(self.grid[i][j + 1].rect.centerx, self.grid[i][j + 1].rect.centery))
                # add barrier field
                self.grid[i].append(Field(j * self.field_size, (i + 1) * self.field_size, self.field_size, 'b'))

    def draw(self, win: pygame.Surface) -> None:
        for row in self.grid:
            for field in row:
                if field.rect.colliderect(win.get_rect()):
                    field.draw(win)
        for coin in self.coins:
            if coin.rect.colliderect(win.get_rect()):
                coin.draw(win)
        self.player.draw(win)
        self.level_bar.draw(win)

        if self.phase == 'lose':
            text_obj = self.font.render("YOU LOST", False, (200, 0, 0))
            win.blit(text_obj, text_obj.get_rect(midbottom=win.get_rect().center))

    def update_state(self) -> 'Route':
        if self.phase == 'game':
            self.camera()
            self.update_tiles()
            self.player.update(self.grid, [])
            self.check_danger_fields()

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

    def check_danger_fields(self):
        for field in self.danger_fields:
            if self.player.rect.collidepoint(field.rect.center):
                self.phase = 'lose'
