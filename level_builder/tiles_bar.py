import pygame

from utils.button import Button


class TileBox:
    Y = 500
    WIDTH = 150
    HEIGHT = 100

    def __init__(self, img: pygame.Surface, x: int, name: str, blank=False):
        self.img = img
        self.rect = pygame.Rect(x, self.Y, self.WIDTH, self.HEIGHT)
        self.blank = blank
        self.name = name
        self.add_button = Button("ADD", 15, (self.rect.centerx - 30, self.Y + self.rect.height + 15, 60, 30),
                                 (0, 200, 0), (0, 150, 0))

    def draw(self, win: pygame.Surface, active=False):
        pygame.draw.rect(win, (170, 170, 170), self.rect)
        if self.blank:
            pygame.draw.rect(win, (255, 255, 255), self.img.get_rect(center=self.rect.center))
        else:
            win.blit(self.img, self.img.get_rect(center=self.rect.center))
        self.add_button.draw(win)
        if active:
            pygame.draw.circle(win, (255, 0, 0), (self.rect.centerx, self.Y + self.rect.height + 60), 10)


class TilesBar:

    def __init__(self, tiles_images):
        self.tile_boxes = [
            TileBox(tiles_images['dirt'], 125, 'dirt'),
            TileBox(tiles_images['blank'], 325, 'blank', True),
            TileBox(tiles_images['thorns'], 525, 'thorns'),
            TileBox(tiles_images['coin'], 725, 'coin')
        ]

    def draw(self, win: pygame.Surface, current_clicked_tile: str):
        pygame.draw.rect(win, (150, 150, 150), (75, 480, 850, 200))
        for tile_box in self.tile_boxes:
            if tile_box.name == current_clicked_tile:
                tile_box.draw(win, True)
            else:
                tile_box.draw(win)

    def get_clicked_tile_name(self, event: pygame.event) -> str:
        for tile_box in self.tile_boxes:
            if tile_box.add_button.is_mouse(event):
                return tile_box.name
