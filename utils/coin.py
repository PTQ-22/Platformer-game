import pygame


class Coin:
    def __init__(self, x: int, y: int, img: pygame.Surface, radius: int = 15):
        self.radius = radius
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius*2, self.radius*2)
        self.color = (220, 255, 0)
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.img = img

    def draw(self, win: pygame.Surface):
        win.blit(self.img, self.img.get_rect(center=self.rect.center))
