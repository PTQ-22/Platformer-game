import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        img = pygame.image.load("res/player_1.png").convert_alpha()
        self.image = pygame.transform.scale(img, (30, 50))
        self.rect = self.image.get_rect(center=(450, 300))
        self.speed = 1

    def keyboard_handler(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 700:
            self.rect.y += self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 1000:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

    def update(self, *args, **kwargs) -> None:
        self.keyboard_handler()
