from typing import List

from player.player_data_object import PlayerDataObject
from utils.field import Field


class GameDataObject:

    def __init__(self):
        self.players = {}
        self.grid: List[List[Field]] = []
        self.field_size = 50
        self.alive = 0
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
                        self.grid[j][i].color = (0, 0, 0)
                        self.grid[j][i].type = '#'

    def add_player(self, player_id: int, x: int):
        self.players.setdefault(player_id, PlayerDataObject(player_id, x, 10))
        self.alive += 1

    def remove_player(self, player_id: int):
        self.players.pop(player_id)
        self.alive -= 1

    def update(self, player: PlayerDataObject):
        if player.y < 750:
            self.players[player.id] = player
        elif player.id in self.players:
            self.remove_player(player.id)