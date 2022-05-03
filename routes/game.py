import pygame
import sys

from networking.client import Client
from player.player import Player
from player.player_data_object import PlayerDataObject


class Game:

    def __init__(self):

        self.client = Client()
        self.player_id, self.game_data = self.client.first_communication()

        self.players = {}
        for p_id, player_obj in self.game_data.players.items():
            self.players.setdefault(int(p_id), Player(p_id, player_obj.x, player_obj.y))

        self.local_player: Player = self.players[self.player_id]
        self.is_player_alive = True
        self.updated_hit = False
        self.font = pygame.font.Font("freesansbold.ttf", 50)

    def draw(self, win: pygame.Surface):
        for row in self.game_data.grid:
            for field in row:
                field.draw(win)

        text_obj = self.font.render(str(self.game_data.alive), False, (0, 0, 0))
        win.blit(text_obj, (20, 20))

        if self.game_data.time_to_start > 0:
            time_test_obj = self.font.render(str(self.game_data.time_to_start), False, (0, 0, 0))
            win.blit(time_test_obj, (400, 20))

        if self.game_data.winner is not None:
            winner_text_obj = self.font.render(f"Winner: {self.game_data.winner.id}", False, (0, 0, 0))
            win.blit(winner_text_obj, (600, 20))

        for player in self.players.values():
            player.draw(win)

    def update_state(self):
        hit_players_data = self.local_player.update(self.game_data.grid, self.players.values())
        if len(hit_players_data) > 0:
            print(hit_players_data)
        self.fetch_data_from_server(hit_players_data)

        self.update_players_with_server_data()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self

    def fetch_data_from_server(self, hit_players_data):
        if self.is_player_alive:
            self.client.send_player_data_obj(
                PlayerDataObject(self.player_id, self.local_player.rect.x, self.local_player.rect.y,
                                 hit_players_data, self.updated_hit)
            )
        self.game_data = self.client.recv_data()

    def update_players_with_server_data(self):
        ids = []
        for p_id, player_obj in self.game_data.players.items():
            ids.append(p_id)
            if p_id not in self.players:
                self.players.setdefault(int(p_id), Player(p_id, player_obj.x, player_obj.y))
            if p_id != self.player_id:
                self.players[p_id].rect.x = player_obj.x
                self.players[p_id].rect.y = player_obj.y

        for p_id in self.players.keys():
            if p_id not in ids:
                self.players.pop(p_id)
                break

        if self.game_data.players[self.local_player.id].is_hit:
            self.local_player.is_hit = True
            self.local_player.hit_direction = self.game_data.players[self.local_player.id].hit_direction
            self.updated_hit = True
        else:
            self.updated_hit = False

