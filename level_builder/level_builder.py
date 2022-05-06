import sys

import pygame

from level_builder.tiles_bar import TilesBar
from routes.route import Route
from utils.button import Button
from utils.coin import Coin
from utils.tile import Tile, TileImages


class LevelBuilder(Route):

    def __init__(self, new_level_number: int):
        self.new_level_number = new_level_number
        self.color = (200, 200, 200)
        self.menu_button = Button("MENU", 20, (10, 10, 80, 40), (0, 200, 0), (0, 150, 0))
        self.save_button = Button("SAVE", 20, (900, 10, 80, 40), (0, 200, 0), (0, 150, 0))
        self.grid = []
        self.field_size = 35
        self.grid_start_x = 190
        self.grid_start_y = -22
        self.tiles_bar = TilesBar(TileImages(50).images)
        self.immutable_tiles_types = ['s', 'd', 'b']
        self.coins = []
        self.tile_images = TileImages(self.field_size).images
        self.load_example()
        self.find_s(self.tile_images)

        self.current_clicked_tile = None

    def load_example(self):
        with open('boards/example.txt') as example_file:
            x = example_file.readlines()
            for i, line in enumerate(x):
                self.grid.append([
                    Tile(-self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                         self.field_size, self.tile_images, 'b', 'brick')])
                for j, c in enumerate(line):
                    if c == '\n':
                        break
                    if c == 'c':
                        self.grid[i].append(
                            Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                                 self.field_size, self.tile_images))
                        self.coins.append(Coin(self.grid[i][j + 1].rect.centerx, self.grid[i][j + 1].rect.centery,
                                               self.tile_images['coin']))
                    elif c == '#':
                        filename = 'dirt'
                        if i != 0 and self.grid[i - 1][j + 1].type != '#':
                            filename = 'grass'
                        self.grid[i].append(
                            Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                                 self.field_size, self.tile_images, '#', filename))
                    elif c == 'A':
                        self.grid[i].append(
                            Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                                 self.field_size, self.tile_images, 'A', 'thorns'))
                    elif c == 'e':
                        self.grid[i - 1][j + 1] = Tile(j * self.field_size + self.grid_start_x,
                                                       i * self.field_size + self.grid_start_y, self.field_size,
                                                       self.tile_images, 'd', 'door_up')
                        self.grid[i].append(
                            Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                                 self.field_size, self.tile_images, 'd', 'door_down'))
                    elif c == 's':
                        self.grid[i].append(
                            Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                                 self.field_size, self.tile_images, 's', 'player_pos'))
                    else:
                        self.grid[i].append(
                            Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                                 self.field_size, self.tile_images))
                self.grid[i].append(
                    Tile(j * self.field_size + self.grid_start_x, (i + 1) * self.field_size + self.grid_start_y,
                         self.field_size, self.tile_images, 'b', 'brick'))

    def find_s(self, tile_images):
        for i, line in enumerate(self.grid):
            for j, tile in enumerate(line):
                if i != 0 and self.grid[i-1][j].type == 's':
                    self.grid[i][j] = Tile((j-1) * self.field_size + self.grid_start_x,
                                           (i+1) * self.field_size + self.grid_start_y, self.field_size, tile_images,
                                           's', 'player_pos')
                    return

    def draw(self, win: pygame.Surface) -> None:
        win.fill(self.color)
        self.menu_button.draw(win)
        self.save_button.draw(win)
        for row in self.grid:
            for tile in row:
                tile.draw(win)
                pygame.draw.rect(win, (0, 0, 0), tile.rect, 1)
                mouse_pos = pygame.mouse.get_pos()
                if tile.rect.collidepoint(mouse_pos):
                    self.draw_transparent_mouse_pos(win, tile.rect)
        for coin in self.coins:
            coin.draw(win)

        self.tiles_bar.draw(win, self.current_clicked_tile)

    def update_state(self) -> 'Route':
        self.check_for_click_on_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            tile_button_click_name = self.tiles_bar.get_clicked_tile_name(event)
            if tile_button_click_name is not None:
                self.current_clicked_tile = tile_button_click_name
            if self.menu_button.is_mouse(event):
                from routes.level_builder_menu import LevelBuilderMenu
                return LevelBuilderMenu()
            if event.type == pygame.MOUSEBUTTONDOWN and self.save_button.is_mouse(event):
                self.save_grid()
                from routes.level_builder_menu import LevelBuilderMenu
                return LevelBuilderMenu()
        return self

    def check_for_click_on_grid(self):
        for row in self.grid:
            for tile in row:
                if tile.type in self.immutable_tiles_types:
                    continue
                mouse_pos = pygame.mouse.get_pos()
                if tile.rect.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed(3)[0]:
                        if self.current_clicked_tile is not None:
                            tile.img = self.tile_images[self.current_clicked_tile]
                            tile.type = Tile.find_type(self.current_clicked_tile)

    def save_grid(self):
        for i, line in enumerate(self.grid):
            for j, c in enumerate(line):
                if i != 0 and self.grid[i-1][j].type == 's':
                    self.grid[i][j].type = '.'
                if i != 0 and self.grid[i-1][j].type == 'd':
                    self.grid[i-1][j].type = '.'
                    self.grid[i][j].type = 'e'
        grid_str = ""
        for i, line in enumerate(self.grid):
            for j, c in enumerate(line):
                if c.type != 'b':
                    grid_str += c.type
            grid_str += '\n'
        with open(f'boards/builder_boards/level {self.new_level_number}.txt', 'w') as new_file:
            new_file.write(grid_str)

    @staticmethod
    def draw_transparent_mouse_pos(win: pygame.Surface, rect: pygame.Rect):
        surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(surf, (0, 0, 200, 100), surf.get_rect())
        win.blit(surf, rect)
