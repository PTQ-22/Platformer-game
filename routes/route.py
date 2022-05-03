from abc import ABC, abstractmethod

import pygame


class Route(ABC):

    @abstractmethod
    def draw(self, win: pygame.Surface) -> None:
        pass

    @abstractmethod
    def update_state(self) -> 'Route':
        pass
