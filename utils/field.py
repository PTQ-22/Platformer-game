import random
from typing import Tuple

import pygame


class Field:

    def __init__(self, x: int, y: int, size: int, field_type: str = '.'):
        self.rect = pygame.Rect(x, y, size, size)
        self.color: Tuple[int, int, int] = (255, 255, 255)
        self.type = field_type
        self.multiplier = max(int(random.randint(1, 100) / (y // size + 2)), 1)

    def draw(self, win: pygame.Surface):
        if self.type == 'b':
            pygame.draw.rect(win, (150, 0, 0), self.rect)
        elif self.type == 'A':
            pygame.draw.rect(win, self.color, self.rect)
            pygame.draw.polygon(win, (50, 50, 50), [self.rect.bottomleft, self.rect.midtop, self.rect.bottomright])
        else:
            pygame.draw.rect(win, self.color, self.rect)
        # pygame.draw.rect(win, (0, 0, 0), self.rect, 1)

    @staticmethod
    def load_tile_img(size: int, filename: str):
        img = pygame.image.load(f"res/tiles/{filename}").convert_alpha()
        return pygame.transform.scale(img, (size, size))
