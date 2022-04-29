import sys
import pygame

from routes.menu import Menu


def main():
    pygame.init()
    win_size = (1000, 750)
    win = pygame.display.set_mode(win_size)

    route = Menu()

    while True:
        win.fill((255, 255, 255))

        route.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        pygame.display.update()
