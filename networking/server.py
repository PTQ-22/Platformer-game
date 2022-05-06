import random
import socket
import time
import json
from _thread import *
import pickle
from networking.game_data_object import GameDataObject

game_data_obj = GameDataObject()
games = {1: game_data_obj}


def threaded_client(conn: socket.socket, player_id: int):
    game_obj = games[1]
    game_obj.add_player(player_id, random.randint(10, 940))
    conn.sendall(f"{player_id}".encode('utf-8'))
    conn.sendall(pickle.dumps(game_obj))
    while True:
        try:
            try:
                player = pickle.loads(conn.recv(8*4096))
            except EOFError:
                break
            game_obj = games[1]
            game_obj.update(player)

            conn.sendall(pickle.dumps(game_obj))
        except socket.error:
            break
    game_obj = games[1]
    game_obj.remove_player(player_id)
    print(f"Close connection with {player_id}")
    conn.close()


def grid_controller():
    game_obj = games[1]
    while len(game_obj.players) < 2:
        time.sleep(1)
    while game_obj.time_to_start > 0:
        time.sleep(1)
        game_obj.time_to_start -= 1

    while len(game_obj.players) > 1:
        # print(game_obj.players)
        for i in range(20):
            for j in range(14):
                if game_obj.grid[i][j].type == '#':
                    if game_obj.grid[i][j].color[0] + game_obj.grid[i][j].multiplier < 255:
                        time.sleep(0.03)
                        game_obj.grid[i][j].color = (
                            game_obj.grid[i][j].color[0] + game_obj.grid[i][j].multiplier,
                            0,
                            0
                        )
                        # print(f"color changed to {game_obj.grid[i][j].color}")
                    else:
                        game_obj.grid[i][j].color = (255, 255, 255)
                        game_obj.grid[i][j].type = '.'
    for p_id in game_obj.players.keys():
        game_obj.winner = game_obj.players[p_id]


def main():

    with open("config.json") as config_file:
        network_data = json.loads(config_file.read())
        ip = network_data['ip']
        port = network_data['port']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, port))
    except socket.error as e:
        print(e)

    s.listen()
    print("Server started")

    start_new_thread(grid_controller, ())

    id_counter = 1
    while True:
        try:
            connection, address = s.accept()
            print(f"{address}, id = {id_counter} connected")
            start_new_thread(threaded_client, (connection, id_counter))
            id_counter += 1
        except KeyboardInterrupt:
            print("Server stopped")
            break
