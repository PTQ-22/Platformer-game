import pygame


class Coin:
    def __init__(self, x: int, y: int, radius: int = 15):
        self.radius = radius
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.color = (220, 255, 0)
        self.font = pygame.font.Font("freesansbold.ttf", 30)

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.color, self.rect.center, self.radius)
