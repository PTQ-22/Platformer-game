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
