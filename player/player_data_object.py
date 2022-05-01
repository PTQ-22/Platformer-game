import random


class PlayerDataObject:

    def __init__(self, player_id: int, x: int = random.randint(10, 950), y: int = 10):
        self.id = player_id
        self.x = x
        self.y = y
