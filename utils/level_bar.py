from typing import Dict
import pygame

from utils.button import Button
from utils.coin import Coin


class LevelBar:
    def __init__(self, field_size: int, tile_images: Dict[str, pygame.Surface]):
        self.field_size = field_size
        self.coin_counter = 0
        self.menu_button = Button("MENU", 15, (10, 10, 60, 30), (0, 200, 0), (0, 150, 0))
        self.coin = Coin(900, 25, tile_images['coin'], 20)
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.time_counter = 0

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, (200, 200, 200), (0, 0, win.get_width(), self.field_size))
        self.menu_button.draw(win)
        # draw time counter
        text_obj = self.font.render(f'TIME: ', False, (0, 0, 0))
        win.blit(text_obj, text_obj.get_rect(center=(490, 25)))
        text_obj = self.font.render(f'{self.time_counter}', False, (200, 0, 0))
        win.blit(text_obj, text_obj.get_rect(center=(550, 25)))
        # draw coin counter
        self.coin.draw(win)
        text_obj = self.font.render(f'{self.coin_counter}x', False, (0, 0, 0))
        win.blit(text_obj, text_obj.get_rect(center=(950, 25)))

    def increase_coin_counter(self):
        self.coin_counter += 1

    def increase_time_counter(self):
        self.time_counter += 1
