import socket
from _thread import *
import pickle
from server.game_data_object import GameDataObject


def threaded_client(conn: socket.socket, player_id: int, game_obj: GameDataObject):
    game_obj.add_player(player_id)
    conn.send(f"{player_id}".encode('utf-8'))
    conn.send(pickle.dumps(game_obj))
    while True:
        try:
            game_obj = pickle.loads(conn.recv(8*4096))
            conn.send(pickle.dumps(game_obj))
        except socket.error:
            break
    game_obj.players.pop(player_id)
    print(f"Close connection with {player_id}")
    conn.close()


def main():
    ip = "127.0.0.1"
    port = 6666
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, port))
    except socket.error as e:
        print(e)

    s.listen()
    print("Server started")

    game_data_object = GameDataObject()

    id_counter = 0
    while True:
        connection, address = s.accept()
        print(f"{address}, id = {id_counter} connected")
        start_new_thread(threaded_client, (connection, id_counter, game_data_object))
        id_counter += 1
