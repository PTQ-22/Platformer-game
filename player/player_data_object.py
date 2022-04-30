import random


class PlayerDataObject:

    def __init__(self, player_id: int):
        self.id = player_id
        self.x = random.randint(10, 950)
        self.y = 10
