from typing import List, Tuple


class PlayerDataObject:

    def __init__(self, player_id: int, x: int, y: int,
                 hit_players_ids: List[Tuple[int, str]] = None, updated_hit=False):
        self.id = player_id
        self.x = x
        self.y = y
        self.hit_players_ids = hit_players_ids
        self.is_hit = False
        self.hit_direction = None
        self.updated_hit = updated_hit
