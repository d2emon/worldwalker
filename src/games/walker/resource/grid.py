"""Grid maker.

Typical usage example:

  grid = Grid(10, (0, 0), (100, 100))
  grid.draw(image)
"""
import pygame


class Grid(pygame.Surface):
    """Grid maker."""

    def __init__(self, size=(100, 100), step=10):
        """Initialize grid.

        Args:
            step (int): Grid step.
            start (tuple): Grid starting position.
            size (tuple): Grid size.
        """
        super().__init__(size, flags=pygame.SRCALPHA)

        self.color = (128, 128, 128)
        self.step = step

        self.draw()

    def draw(self):
        """Draw grid."""
        max_x, max_y = self.get_size()

        # Fill horyzontal lines
        for x in range(0, max_x, self.step):
            pygame.draw.line(self, self.color, (x, 0), (x, max_y))

        # Fill vertical lines
        for y in range(0, max_y, self.step):
            pygame.draw.line(self, self.color, (0, y), (max_x, y))
