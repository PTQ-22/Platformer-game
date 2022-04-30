import pygame
import sys
from player.player import Player


class Field:

    def __init__(self, x: int, y: int, size: int):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 255, 255)

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, (0, 0, 0), self.rect, 1)


class Game:

    def __init__(self):
        self.color = (200, 200, 200)  # TODO change to picture
        self.player = Player()

        self.grid = []
        self.field_size = 50
        self.make_grid()

    def make_grid(self):
        for i in range(0, 1000, self.field_size):
            self.grid.append([])
            for j in range(0, 700, self.field_size):
                self.grid[i // self.field_size].append(
                    Field(i, j, self.field_size)
                )
        with open("res/board.txt") as file:
            x = file.readlines()
            for i, line in enumerate(x):
                for j, c in enumerate(line):
                    if c == '\n':
                        break
                    if c == '#':
                        self.grid[j][i].color = (100, 40, 40)

        # for i in range(7, 14):
        #     self.grid[i][7].color = (100, 40, 40)
        # for i in range(3, 9):
        #     self.grid[i][4].color = (100, 40, 40)
        # for i in range(12, 19):
        #     self.grid[i][9].color = (100, 40, 40)

    def draw(self, win: pygame.Surface):
        win.fill(self.color)

        for row in self.grid:
            for field in row:
                field.draw(win)

        self.player.draw(win)

    def update_state(self):
        self.player.update(self.grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self
