import pygame


class ArmsController:
    COLOR = (90, 90, 90)

    def __init__(self, rect: pygame.Rect):
        self.left_arm_x = rect.x
        self.left_arm_y = rect.centery - rect.width // 5
        self.left_arm_surf = pygame.Surface((rect.width // 6, rect.height // 3))
        self.left_arm_surf.fill(self.COLOR)

        self.right_arm_x = rect.x + rect.width - rect.width // 6
        self.right_arm_y = rect.centery - rect.width // 5
        self.right_arm_surf = pygame.Surface((rect.width // 6, rect.height // 3), pygame.SRCALPHA)
        self.right_arm_surf.fill(self.COLOR)

        self.right_arm_up = False
        self.right_animation_phase = 'up'
        self.right_count_target = 0
        self.right_counter = 0

        self.left_arm_up = False
        self.left_animation_phase = 'up'
        self.left_count_target = 0
        self.left_counter = 0

    def start_animation(self, direction: str):
        if direction == "right":
            self.right_arm_up = True
            self.right_animation_phase = 'up'
            self.right_count_target = self.right_arm_surf.get_height()
            self.right_counter = 0
        elif direction == "left":
            self.left_arm_up = True
            self.left_animation_phase = 'up'
            self.left_count_target = self.left_arm_surf.get_height()
            self.left_counter = 0

    def animate(self, rect: pygame.Rect):
        if self.right_arm_up:
            if self.right_counter >= self.right_count_target:
                self.right_animation_phase = 'down'
            if self.right_animation_phase == 'up':
                self.right_arm_y -= 7
                self.right_counter += 0.3
            elif self.right_animation_phase == 'down':
                self.right_arm_y += 0.3
                self.right_counter -= 0.3
                if self.right_counter <= 0:
                    self.right_arm_up = False
                    self.right_arm_y = rect.centery - rect.width // 5
        elif self.left_arm_up:
            if self.left_counter >= self.left_count_target:
                self.left_animation_phase = 'down'
            if self.left_animation_phase == 'up':
                self.left_arm_y -= 7
                self.left_counter += 0.3
            elif self.left_animation_phase == 'down':
                self.left_arm_y += 0.3
                self.left_counter -= 0.3
                if self.left_counter <= 0:
                    self.left_arm_up = False
                    self.left_arm_y = rect.centery - rect.width // 5

    def draw_arms(self, win: pygame.Surface):
        win.blit(self.left_arm_surf, (self.left_arm_x, self.left_arm_y))
        win.blit(self.right_arm_surf, (self.right_arm_x, self.right_arm_y))

    def update_rect_pos(self, rect: pygame.Rect):
        self.left_arm_x = rect.x
        self.left_arm_y = rect.centery - rect.width // 5
        self.right_arm_x = rect.x + rect.width - rect.width // 6
        self.right_arm_y = rect.centery - rect.width // 5
        self.animate(rect)
