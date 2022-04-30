
import pygame


class Player:

    def __init__(self):
        img = pygame.image.load("res/player_1.png").convert_alpha()
        self.image = pygame.transform.scale(img, (30, 50))
        self.rect = self.image.get_rect(center=(200, 10))
        self.speed = 1
        self.gravity_speed = 1
        self.jump_val = 0
        self.can_jump = True

    def draw(self, win: pygame.Surface):
        win.blit(self.image, self.rect)

    def key_handler(self, on_block: bool):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < 1000:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and on_block and self.can_jump:
            self.jump_val = 100
            self.can_jump = False

    def update(self, grid):
        on_block = self.is_on_block(grid)
        self.key_handler(on_block)
        if not on_block:
            self.rect.y += self.gravity_speed

        if self.jump_val > 0:
            self.rect.y -= 2
            self.jump_val -= 2
        else:
            self.can_jump = True

    def is_on_block(self, grid) -> bool:
        for row in grid:
            for field in row:
                if self.rect.colliderect(field.rect) and field.color != (255, 255, 255):
                    return True
        return False
