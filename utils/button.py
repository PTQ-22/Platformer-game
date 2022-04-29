from typing import Tuple
import pygame


class Button:

    def __init__(self, text: str, font_size: int, rect: Tuple[int, int, int, int],
                 color: Tuple[int, int, int], hover_color: Tuple[int, int, int]):
        font = pygame.font.Font("freesansbold.ttf", font_size)
        self.text_obj = font.render(text, False, (0, 0, 0))
        self.text_rect = self.text_obj.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hover_color = hover_color
        self.current_color = color

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.current_color, self.rect)
        win.blit(self.text_obj, self.text_rect)
        self.is_mouse()

    def is_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False
