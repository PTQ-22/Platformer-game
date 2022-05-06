from typing import Dict

import pygame


class TileImages:

    def __init__(self, size: int):
        self.images = {
            "blank": self.load_tile_img(size, "blank.png"),
            "brick": self.load_tile_img(size, "brick.png"),
            "dirt": self.load_tile_img(size, "dirt.png"),
            "grass": self.load_tile_img(size, "grass.png"),
            "thorns": self.load_tile_img(size, "thorns.png"),
            "coin": self.load_tile_img(size, "coin.png"),
            "door_up": self.load_tile_img(size, "door_up.png"),
            "door_down": self.load_tile_img(size, "door_down.png"),
            "player_pos": self.load_tile_img(size, "player_pos.png")
        }

    @staticmethod
    def load_tile_img(size: int, filename: str):
        img = pygame.image.load(f"res/tiles/{filename}").convert_alpha()
        return pygame.transform.scale(img, (size, size))


class Tile:

    def __init__(self, x: int, y: int, size: int, tile_images: Dict[str, pygame.Surface],
                 field_type: str = '.', type_name: str = 'blank'):
        self.rect = pygame.Rect(x, y, size, size)
        self.type = field_type
        self.img = tile_images[type_name]

    def draw(self, win: pygame.Surface):
        win.blit(self.img, self.rect)

    @staticmethod
    def find_type(name: str) -> str:
        if name == 'blank':
            return '.'
        elif name == 'dirt' or name == 'grass':
            return '#'
        elif name == 'thorns':
            return 'A'
        elif name == 'coin':
            return 'c'
        elif name == 'brick':
            return 'b'
