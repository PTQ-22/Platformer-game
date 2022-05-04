from typing import Set


class JumpController:
    JUMP_SPEED = 3

    def __init__(self):
        self.jump_val = 0
        self.can_jump = True

    def start_jump(self):
        self.jump_val = 150
        self.can_jump = False

    def work(self, player, blocks_state: Set[str]):
        if self.jump_val > 0:
            self.jump_val -= self.JUMP_SPEED
            if 'top' not in blocks_state and player.rect.y > -20:
                player.rect.y -= self.JUMP_SPEED
        else:
            self.can_jump = True
