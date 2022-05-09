from abc import ABC, abstractmethod

import pygame


class Route(ABC):

    @abstractmethod
    def draw(self, win: pygame.Surface) -> None:
        """
        function to draw everything on the display
        """
        pass

    @abstractmethod
    def update_state(self) -> 'Route':
        """
        function to update everything,
        handle events
        and returns different route
        if some button is clicked
        example: menu
        """
        pass
