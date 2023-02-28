"""Grid maker.

Typical usage example:

  grid = Grid(10, (0, 0), (100, 100))
  grid.draw(image)
"""
import pygame


class Grid:
    """Grid maker."""

    def __init__(self, step=10, start=(0, 0), size=(100, 100)):
        """Initialize grid.

        Args:
            step (int): Grid step.
            start (tuple): Grid starting position.
            size (tuple): Grid size.
        """
        self.__step = step
        self.__start = start
        self.__size = size

    def draw(self, image):
        """Draw grid.

        Args:
            image (pygame.Surface): Image to draw grid on it.
        """
        min_x, min_y = self.__start
        max_x, max_y = self.__size

        # Fill horyzontal lines
        for x in range(min_x, max_x, self.__step):
            pygame.draw.line(image, (0, 0, 0), (x, min_y), (x, max_y))

        # Fill vertical lines
        for y in range(min_y, max_y, self.__step):
            pygame.draw.line(image, (0, 0, 0), (min_x, y), (max_x, y))
