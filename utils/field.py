import random
from typing import Tuple

import pygame


class Field:

    def __init__(self, x: int, y: int, size: int):
        self.rect = pygame.Rect(x, y, size, size)
        self.color: Tuple[int, int, int] = (255, 255, 255)
        self.type = '.'
        self.multiplier = int(random.randint(1, 100) / (y // size + 2))

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, self.rect)
        # pygame.draw.rect(win, (0, 0, 0), self.rect, 1)
