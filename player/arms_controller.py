import pygame


class Arm:
    COLOR = (90, 90, 90)

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.surf = pygame.Surface((width, height))
        self.surf.fill(self.COLOR)

        self.up = False
        self.animation_phase = 'up'
        self.count_target = 0
        self.counter = 0

    def draw(self, win: pygame.Surface):
        win.blit(self.surf, (self.x, self.y))

    def start_animation(self):
        self.up = True
        self.animation_phase = 'up'
        self.count_target = self.surf.get_height()
        self.counter = 0

    def animate(self, rect: pygame.Rect):
        if self.counter >= self.count_target:
            self.animation_phase = 'down'
        if self.animation_phase == 'up':
            self.y -= 7
            self.counter += 0.3
        elif self.animation_phase == 'down':
            self.y += 0.3
            self.counter -= 0.3
            if self.counter <= 0:
                self.up = False
                self.y = rect.centery - rect.width // 5


class ArmsController:
    COLOR = (90, 90, 90)

    def __init__(self, rect: pygame.Rect):
        self.left_arm = Arm(rect.x, rect.centery - rect.width // 5, rect.width // 6, rect.height // 3)
        self.right_arm = Arm(
            rect.x + rect.width - rect.width // 6, rect.centery - rect.width // 5, rect.width // 6, rect.height // 3)

    def start_animation(self, direction: str, r_pressed: bool):
        if (direction == "right" and not r_pressed) or (direction == 'left' and r_pressed):
            self.right_arm.start_animation()
        elif (direction == "left" and not r_pressed) or (direction == 'right' and r_pressed):
            self.left_arm.start_animation()

    def animate(self, rect: pygame.Rect):
        if self.right_arm.up:
            self.right_arm.animate(rect)
        elif self.left_arm.up:
            self.left_arm.animate(rect)

    def draw_arms(self, win: pygame.Surface):
        self.left_arm.draw(win)
        self.right_arm.draw(win)

    def update_rect_pos(self, rect: pygame.Rect):
        self.left_arm.x = rect.x
        self.left_arm.y = rect.centery - rect.width // 5
        self.right_arm.x = rect.x + rect.width - rect.width // 6
        self.right_arm.y = rect.centery - rect.width // 5
        self.animate(rect)
