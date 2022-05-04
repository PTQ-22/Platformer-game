import pygame
import sys

from networking.client import Client
from player.player import Player
from player.player_data_object import PlayerDataObject
from routes.route import Route


class MultiplayerGame(Route):

    def __init__(self):
        self.client = None
        self.player_id = None
        self.game_data = None
        self.players = {}
        self.local_player = None
        self.is_player_alive = True
        self.updated_hit = False
        try:
            self.try_to_connect_and_init()
        except ConnectionRefusedError:
            self.phase = 'waiting'

        self.font = pygame.font.Font("freesansbold.ttf", 50)

    def try_to_connect_and_init(self):
        self.client = Client()
        self.phase = 'game'
        self.player_id, self.game_data = self.client.first_communication()
        for p_id, player_obj in self.game_data.players.items():
            self.players.setdefault(int(p_id), Player(p_id, player_obj.x, player_obj.y))
        self.local_player: Player = self.players[self.player_id]

    def draw(self, win: pygame.Surface) -> None:
        if self.phase == 'game':
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
        elif self.phase == 'waiting':
            win.fill((200, 200, 200))
            text_obj = self.font.render("Waiting for connection...", False, (0, 0, 0))
            win.blit(text_obj, (200, 250))

    def update_state(self) -> 'Route':
        if self.phase == 'game':
            hit_players_data = self.local_player.update(self.game_data.grid, self.players.values())

            self.fetch_data_from_server(hit_players_data)

            self.update_players_with_server_data()
        else:
            try:
                self.try_to_connect_and_init()
            except ConnectionRefusedError:
                self.phase = 'waiting'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        return self

    def fetch_data_from_server(self, hit_players_data):
        if self.is_player_alive:
            self.client.send_player_data_obj(
                PlayerDataObject(self.player_id, self.local_player.rect.x, self.local_player.rect.y,
                                 hit_players_data, self.updated_hit,
                                 self.local_player.is_moving, self.local_player.direction, self.local_player.arm_up)
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
                self.players[p_id].is_moving = player_obj.is_moving
                self.players[p_id].direction = player_obj.direction
                if player_obj.arm_up:
                    self.players[p_id].arms_controller.start_animation(player_obj.direction)

        if self.local_player.id in self.game_data.players:
            if self.game_data.players[self.local_player.id].is_hit:
                self.local_player.hit_controller.start_hit(self.game_data.players[self.local_player.id].hit_direction)
                self.updated_hit = True
            else:
                self.updated_hit = False

        for p_id in self.players.keys():
            if p_id not in ids:
                self.players.pop(p_id)
                break
