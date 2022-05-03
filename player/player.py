from typing import Set, List, Tuple

import pygame


class Player:

    def __init__(self, player_id: int, x: int, y: int):
        self.id = player_id

        img_right = pygame.image.load("res/player_1_right.png").convert_alpha()
        img_left = pygame.image.load("res/player_1_left.png").convert_alpha()
        self.image_right = pygame.transform.scale(img_right, (38, 63))
        self.image_left = pygame.transform.scale(img_left, (38, 63))
        # self.image_right = pygame.transform.scale(img_right, (60, 100))
        # self.image_left = pygame.transform.scale(img_left, (60, 100))

        self.rect = self.image_right.get_rect(center=(x, y))
        self.attack_rect = pygame.Rect(
            self.rect.centerx, self.rect.centery, self.rect.width - self.rect.width // 3, self.rect.width // 2
        )
        self.direction = "right"

        self.speed = 1
        self.gravity_speed = 1
        self.jump_val = 0
        self.hit_val = 0
        self.can_jump = True
        self.is_hit = False
        self.hit_direction = None

    def draw(self, win: pygame.Surface):
        if self.direction == "right":
            win.blit(self.image_right, self.rect)
        elif self.direction == "left":
            win.blit(self.image_left, self.rect)

        # TEST TODO remove
        if self.is_hit:
            pygame.draw.circle(win, (255, 0, 0), self.rect.center, 3)
        # pygame.draw.rect(win, (100, 0, 0), self.attack_rect)

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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if 'left' not in blocks_state and self.rect.x > 0:
                self.rect.x -= self.speed
                self.direction = "left"
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and ('on' in blocks_state) and self.can_jump:
            self.jump_val = 150
            self.can_jump = False
        if keys[pygame.K_SPACE]:
            return self.check_for_hit_players(players)
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
        if self.jump_val > 0:
            self.jump_val -= 3
            if 'top' not in blocks_state:
                self.rect.y -= 3
        else:
            self.can_jump = True

        # other player hit
        if self.is_hit:
            self.jump_val = 50
            self.hit_val = 150
            self.is_hit = False
            self.can_jump = False
        if self.hit_val > 0:
            self.hit_val -= 3
            if self.hit_direction == "right" and "right" not in blocks_state and self.rect.right < 1000:
                self.rect.x += 3
            elif self.hit_direction == "left" and "left" not in blocks_state and self.rect.x > 0:
                self.rect.x -= 3

        # change attack rect
        if self.direction == "right":
            self.attack_rect.update(
                self.rect.centerx, self.rect.centery, self.attack_rect.width, self.attack_rect.height
            )
        elif self.direction == "left":
            self.attack_rect.update(
                self.rect.centerx - self.rect.width + self.rect.width // 3,
                self.rect.centery, self.attack_rect.width, self.attack_rect.height
            )

        return hit_players_data

    def is_on_block(self, grid) -> Set[str]:
        states = set()
        for row in grid:
            for field in row:
                collision = self.rect.colliderect(field.rect)
                if (collision and self.rect.bottom < field.rect.y + 5) \
                        and field.color != (255, 255, 255):
                    states.add('on')
                elif collision and field.color != (255, 255, 255):
                    if self.rect.x > field.rect.x:
                        states.add('left')
                    else:
                        states.add('right')
                head_collision = field.rect.collidepoint(self.rect.midtop)
                if head_collision and field.color != (255, 255, 255):
                    states.add('top')
        return states
