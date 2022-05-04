from typing import List, Tuple

import pygame

from player.bow import Bow
from player.player import Player


class LocalPlayer(Player):
    
    def __init__(self, player_id: int, x: int, y: int):
        super().__init__(player_id, x, y)
        self.bow = Bow(self.rect)

    def draw(self, win: pygame.Surface):
        if self.is_moving:
            self.animation_controller.animate_walk(win, self.rect, self.direction)
        else:
            if self.direction == "right":
                win.blit(self.image_right, self.rect)
            elif self.direction == "left":
                win.blit(self.image_left, self.rect)

        self.arms_controller.update_rect_pos(self.rect)
        self.arms_controller.draw_arms(win)
        if self.r_pressed:
            self.bow.draw(win)

    def update(self, grid, players) -> List[Tuple[int, str]]:
        blocks_state = self.is_on_block(grid)
        hit_players_data = self.key_handler(blocks_state, players)

        # gravity
        if 'on' not in blocks_state and self.rect.y - 10 < 750:
            self.rect.y += self.gravity_speed
        # jump
        self.jump_controller.work(self, blocks_state)
        # other player hit
        self.hit_controller.work(self, blocks_state)
        # change attack rect
        self.update_attack_rect()
        if self.r_pressed:
            self.bow.update(self)

        return hit_players_data

        