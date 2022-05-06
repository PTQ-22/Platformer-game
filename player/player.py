from typing import Set, List, Tuple

import pygame

from player.animation_controller import AnimationController
from player.arms_controller import ArmsController
from player.hit_controller import HitController
from player.jump_controller import JumpController


class Player:

    def __init__(self, player_id: int, x: int, y: int):
        self.id = player_id

        img_right = pygame.image.load("res/player/player_1_right.png").convert_alpha()
        img_left = pygame.image.load("res/player/player_1_left.png").convert_alpha()
        self.image_right = pygame.transform.scale(img_right, (38, 63))
        self.image_left = pygame.transform.scale(img_left, (38, 63))
        # self.image_right = pygame.transform.scale(img_right, (60, 100))
        # self.image_left = pygame.transform.scale(img_left, (60, 100))
        self.animation_controller = AnimationController()
        self.is_moving = False

        self.rect = self.image_right.get_rect(center=(x, y))
        self.arms_controller = ArmsController(self.rect)
        self.arm_up = False
        self.r_pressed = False

        self.attack_rect = pygame.Rect(
            self.rect.centerx, self.rect.centery, self.rect.width - self.rect.width // 3, self.rect.width // 2
        )
        self.direction = "right"

        self.speed = 2
        self.gravity_speed = 1

        self.jump_controller = JumpController()
        self.hit_controller = HitController()

        font = pygame.font.Font("freesansbold.ttf", 25)
        self.text_obj = font.render(f'{self.id}', False, (200, 0, 0))

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
        win.blit(self.text_obj, self.text_obj.get_rect(center=(self.rect.centerx, self.rect.centery + 5)))

    def key_handler(self, blocks_state: Set[str], players) -> List[Tuple[int, str]]:
        """
            handle all player's keyboard events
            :return list of hit enemies ids and hit directions
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if 'right' not in blocks_state and self.rect.right < 1000:
                self.rect.x += self.speed
                self.direction = "right"
                self.is_moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if 'left' not in blocks_state and self.rect.x > 0:
                self.rect.x -= self.speed
                self.direction = "left"
                self.is_moving = True
        else:
            self.is_moving = False
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and ('on' in blocks_state) and self.jump_controller.can_jump:
            self.jump_controller.start_jump()
        if keys[pygame.K_SPACE]:
            self.arms_controller.start_animation(self.direction, self.r_pressed)
            self.arm_up = True
            return self.check_for_hit_players(players)
        else:
            self.arm_up = False
        if keys[pygame.K_r]:
            self.r_pressed = True
        else:
            self.r_pressed = False
        return []

    def check_for_hit_players(self, players):
        hit_players_data = []
        for player in players:
            if self.attack_rect.colliderect(player.rect) and player.id != self.id:
                hit_players_data.append((player.id, self.direction))
        return hit_players_data

    def update(self, grid, players) -> List[Tuple[int, str]]:
        """
            update -> method call in game
            updates local player's position, control keyboard and gravity
            :return list of hit enemies ids and hit direction
        """
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

        return hit_players_data

    def update_attack_rect(self):
        if self.direction == "right":
            self.attack_rect.update(
                self.rect.centerx, self.rect.centery, self.attack_rect.width, self.attack_rect.height
            )
        elif self.direction == "left":
            self.attack_rect.update(
                self.rect.centerx - self.rect.width + self.rect.width // 3,
                self.rect.centery, self.attack_rect.width, self.attack_rect.height
            )

    def is_on_block(self, grid) -> Set[str]:
        states = set()
        for row in grid:
            for field in row:
                collision = self.rect.colliderect(field.rect)
                if (collision and self.rect.bottom < field.rect.y + 5) and field.type in ['#']:
                    states.add('on')
                elif collision and field.type in ['#', 'b']:
                    if self.rect.x > field.rect.x:
                        states.add('left')
                    else:
                        states.add('right')
                head_collision = field.rect.collidepoint(self.rect.midtop)
                if (head_collision and field.type in ['#', 'b']) or self.rect.y < grid[0][0].rect.y:
                    states.add('top')
        return states
