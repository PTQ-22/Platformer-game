import pygame

from routes.menu import Menu


def main():
    pygame.init()
    win_size = (1000, 700)
    win = pygame.display.set_mode(win_size)

    route = Menu(win_size)

    while True:
        win.fill((255, 255, 255))  # TODO change background

        route.draw(win)

        route = route.update_state()

        pygame.display.update()
