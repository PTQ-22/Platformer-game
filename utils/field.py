import pygame


class Field:

    def __init__(self, x: int, y: int, size: int):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 255, 255)

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 1)
