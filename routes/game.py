import pickle
import socket

import pygame
import sys
from player.player import Player
from server.game_data_object import GameDataObject


class Game:

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client.connect(("127.0.0.1", 6666))
        self.player_id = int(self.client.recv(8*4096).decode("utf-8"))
        self.game_data: GameDataObject = pickle.loads(self.client.recv(8*4096))

        self.players = {}
        for p_id, player_obj in self.game_data.players.items():
            self.players.setdefault(int(p_id), Player(p_id, player_obj.x, player_obj.y))

        self.local_player = self.players[self.player_id]

    def draw(self, win: pygame.Surface):
        for row in self.game_data.grid:
            for field in row:
                field.draw(win)
        for player in self.players.values():
            player.draw(win)

    def update_state(self):
        self.local_player.update(self.game_data.grid)

        self.update_player_in_game_obj()
        self.fetch_data_from_server()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self

    def update_player_in_game_obj(self):
        self.game_data.players[self.player_id].x = self.local_player.rect.x
        self.game_data.players[self.player_id].y = self.local_player.rect.y

    def fetch_data_from_server(self):
        self.client.send(pickle.dumps(self.game_data))
        self.game_data = pickle.loads(self.client.recv(8*4096))
        print(self.game_data.players)
        for p_id, player_obj in self.game_data.players.items():
            if p_id not in self.players:
                self.players.setdefault(int(p_id), Player(p_id, player_obj.x, player_obj.y))
            if p_id != self.player_id:
                self.players[p_id].rect.x = player_obj.x
                self.players[p_id].rect.y = player_obj.y
