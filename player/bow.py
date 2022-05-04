import math
from typing import Tuple

import pygame


class Bow:
    def __init__(self, player_rect: pygame.Rect):
        img_right = pygame.image.load("res/bow/bow_right.png").convert_alpha()
        self.image_right = pygame.transform.scale(img_right, (23, 41))
        self.current_image = self.image_right
        self.rect = self.current_image.get_rect(center=player_rect.center)

    def draw(self, win: pygame.Surface):
        win.blit(self.current_image, self.rect)

    def update(self, player):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= player.rect.centerx:
            player.direction = 'right'
            self.current_image = self.image_right
            self.rotate_img(mouse_pos, player.rect.centerx + player.rect.w // 4, player.rect.centery - 5)
        else:
            player.direction = 'left'
            self.current_image = self.image_right
            self.rotate_img(mouse_pos, player.rect.x + player.rect.w // 4, player.rect.centery - 5)

    def rotate_img(self, mouse_pos: Tuple[int, int], x: int, y: int):
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        degs = math.degrees(math.atan2(dy, dx))
        self.current_image = pygame.transform.rotate(self.current_image, -degs)
        self.rect = self.current_image.get_rect(center=(x, y))
