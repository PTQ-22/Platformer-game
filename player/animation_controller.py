import pygame


class AnimationController:
    NUM_OF_IMAGES = 4
    IMAGE_WIDTH = 38
    IMAGE_HEIGHT = 63

    ANIMATION_COUNTER_MAX = 20

    def __init__(self):
        self.right_images = []
        self.left_images = []
        for i in range(self.NUM_OF_IMAGES):
            img_right = pygame.image.load(f"res/player/player_{i + 1}_right.png").convert_alpha()
            img_left = pygame.image.load(f"res/player/player_{i + 1}_left.png").convert_alpha()
            self.right_images.append(pygame.transform.scale(img_right, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT)))
            self.left_images.append(pygame.transform.scale(img_left, (self.IMAGE_WIDTH, self.IMAGE_HEIGHT)))
        self.animation_counter = 0

    def animate(self, win: pygame.Surface, rect: pygame.Rect, direction: str):
        self.animation_counter += 1
        if self.animation_counter > self.ANIMATION_COUNTER_MAX:
            self.animation_counter = 0
        if direction == "right":
            win.blit(self.right_images[self.animation_counter % self.NUM_OF_IMAGES], rect)
        elif direction == "left":
            win.blit(self.left_images[self.animation_counter % self.NUM_OF_IMAGES], rect)
