from player.player_data_object import PlayerDataObject
from utils.field import Field


class GameDataObject:

    def __init__(self):
        self.players = {}
        self.grid = []
        self.field_size = 50
        self.make_grid()

    def make_grid(self):
        for i in range(0, 1000, self.field_size):
            self.grid.append([])
            for j in range(0, 700, self.field_size):
                self.grid[i // self.field_size].append(Field(i, j, self.field_size))
        with open("res/board.txt") as file:
            x = file.readlines()
            for i, line in enumerate(x):
                for j, c in enumerate(line):
                    if c == '\n':
                        break
                    if c == '#':
                        self.grid[j][i].color = (100, 40, 40)

    def add_player(self, player_id: int):
        self.players.setdefault(player_id, PlayerDataObject(player_id))
