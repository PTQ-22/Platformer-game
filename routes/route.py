import pygame
import sys
from player.player import Player


class Route:

    def __init__(self):
        self.color = (200, 200, 200)  # TODO change to picture
        self.player = Player()
        self.player_grup = pygame.sprite.GroupSingle(self.player)

    def draw(self, win: pygame.Surface):
        win.fill(self.color)
        for i in range(0, 1000, 50):
            for j in range(0, 700, 50):
                field = pygame.Rect(i, j, 50, 50)
                if self.player.rect.colliderect(field):
                    pygame.draw.rect(win, (150, 0, 0), field)
                pygame.draw.rect(win, (0, 0, 0), field, 2)
        self.player_grup.draw(win)

        self.player_grup.update()

    def update_state(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self
