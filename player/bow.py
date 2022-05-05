import math
from typing import Tuple, List

import pygame


def rotate_img(img: pygame.Surface, mouse_pos: Tuple[int, int], x: int, y: int) -> Tuple[pygame.Surface, pygame.Rect]:
    """
    Rotates image in order to follow mouse
    :return: rotated image, and it's pygame rect
    """
    dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
    degs = math.degrees(math.atan2(dy, dx))
    img = pygame.transform.rotate(img, -degs)
    rect = img.get_rect(center=(x, y))
    return img, rect


class BowArrow:
    def __init__(self, bow_rect: pygame.Rect):
        arrow_img = pygame.image.load("res/bow/arrow.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(arrow_img, (30, 9))
        self.current_image = self.arrow_image
        self.rect = self.arrow_image.get_rect(center=bow_rect.center)

    def draw(self, win: pygame.Surface):
        win.blit(self.current_image, self.rect)

    def update(self, mouse_pos: Tuple[int, int], bow_rect: pygame.Rect):
        self.current_image, self.rect = rotate_img(self.arrow_image, mouse_pos, bow_rect.centerx, bow_rect.centery)

    def get_img_and_rect(self):
        return self.current_image, self.rect


class FlyArrow:

    def __init__(self, img: pygame.Surface, rect: pygame.Rect, mouse_pos: Tuple[int, int]):
        self.image = img
        self.rect = rect
        self.angle = self.set_angle(mouse_pos)
        print(f"deg {math.degrees(self.angle)}")
        self.speed = 10

    def draw(self, win: pygame.Surface):
        win.blit(self.image, self.rect)

    def move(self):
        self.rect.centerx += (self.speed * math.cos(self.angle))
        self.rect.centery += (self.speed * math.sin(self.angle))
    # def move(self):
    #     vect = pygame.math.Vector2()
    #     vect.from_polar((self.speed, math.degrees(self.angle)))
    #     self.rect.center += vect

    def set_angle(self, mouse_pos: Tuple[int, int]):
        x = self.rect.centerx
        y = self.rect.centery
        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        return math.atan2(dy, dx)


class Bow:
    def __init__(self, player_rect: pygame.Rect):
        img_right = pygame.image.load("res/bow/bow_right.png").convert_alpha()
        self.image_right = pygame.transform.scale(img_right, (23, 41))
        self.current_image = self.image_right
        self.rect = self.current_image.get_rect(center=player_rect.center)
        self.bow_arrow = BowArrow(self.rect)
        self.fly_arrows: List[FlyArrow] = []
        self.counter = 0
        self.shot = False

    def draw(self, win: pygame.Surface):
        win.blit(self.current_image, self.rect)
        self.bow_arrow.draw(win)

    def draw_fly_arrows(self, win: pygame.Surface):
        for arrow in self.fly_arrows:
            arrow.move()
            arrow.draw(win)

    def update(self, player):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] >= player.rect.centerx:
            player.direction = 'right'
            self.current_image, self.rect = rotate_img(
                self.image_right, mouse_pos, player.rect.centerx + player.rect.w // 4, player.rect.centery - 5
            )
        else:
            player.direction = 'left'
            self.current_image, self.rect = rotate_img(
                self.image_right, mouse_pos, player.rect.x + player.rect.w // 4, player.rect.centery - 5
            )
        if player.arm_up:
            self.shot = True
            if self.counter == 0:
                img, rect = self.bow_arrow.get_img_and_rect()
                self.fly_arrows.append(FlyArrow(img, rect, mouse_pos))
        if self.shot:
            self.counter += 1
            if self.counter >= 40:
                self.counter = 0
                self.shot = False

        self.bow_arrow.update(mouse_pos, self.rect)
