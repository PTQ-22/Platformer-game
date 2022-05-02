import socket
import pickle

from networking.game_data_object import GameDataObject
from player.player_data_object import PlayerDataObject


class Client:

    BUF_SIZE = 8*4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 6666))

    def first_communication(self) -> (int, GameDataObject):
        player_id = int(self.socket.recv(self.BUF_SIZE).decode('utf-8'))
        game_data = pickle.loads(self.socket.recv(self.BUF_SIZE))
        return player_id, game_data

    def send_player_data_obj(self, player_data: PlayerDataObject):
        self.socket.send(pickle.dumps(player_data))

    def recv_data(self):
        return pickle.loads(self.socket.recv(self.BUF_SIZE))
