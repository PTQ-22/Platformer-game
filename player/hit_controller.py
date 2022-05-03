from typing import Set


class HitController:
    PUNCH_SPEED = 3

    def __init__(self):
        self.hit_val_x = 0
        self.hit_val_y = 0
        self.is_hit = False
        self.hit_direction = None

    def start_hit(self, direction: str):
        self.is_hit = True
        self.hit_direction = direction

    def work(self, player, blocks_state: Set[str]):
        if self.is_hit:
            self.hit_val_y = 50
            self.hit_val_x = 150
            self.is_hit = False
        if self.hit_val_x > 0:
            self.hit_val_x -= self.PUNCH_SPEED
            if self.hit_direction == "right" and "right" not in blocks_state and player.rect.right < 1000:
                player.rect.x += self.PUNCH_SPEED
            elif self.hit_direction == "left" and "left" not in blocks_state and player.rect.x > 0:
                player.rect.x -= self.PUNCH_SPEED
        if self.hit_val_y > 0:
            self.hit_val_y -= self.PUNCH_SPEED
            if "top" not in blocks_state:
                player.rect.y -= self.PUNCH_SPEED
