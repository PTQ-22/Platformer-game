from typing import Set

import pygame


class Player:

    def __init__(self, player_id: int, x: int, y: int):
        self.id = player_id
        img = pygame.image.load("res/player_1.png").convert_alpha()
        self.image = pygame.transform.scale(img, (38, 63))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 1
        self.gravity_speed = 1
        self.jump_val = 0
        self.can_jump = True

    def draw(self, win: pygame.Surface):
        win.blit(self.image, self.rect)
        pygame.draw.circle(win, (255, 0, 0), self.rect.center, 3)

    def key_handler(self, blocks_state: Set[str]):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if 'right' not in blocks_state and self.rect.right < 1000:
                self.rect.x += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if 'left' not in blocks_state and self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and ('on' in blocks_state) and self.can_jump:
            self.jump_val = 150
            self.can_jump = False

    def update(self, grid):
        blocks_state = self.is_on_block(grid)
        self.key_handler(blocks_state)
        if 'on' not in blocks_state:
            self.rect.y += self.gravity_speed

        if self.jump_val > 0:
            self.jump_val -= 3
            if 'top' not in blocks_state:
                self.rect.y -= 3
        else:
            self.can_jump = True

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
