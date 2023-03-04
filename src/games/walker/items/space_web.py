import pygame
import random
from scipy.spatial import Voronoi
from .clusters import SuperclusterComplex


class SpaceWeb(pygame.sprite.Sprite):
    def __init__(self, size, voids, *groups):
        super().__init__(*groups)
        self.name = 'Space Web'
        self.scale = 24
        self.visible = True
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        supercluster_complex_factory = SuperclusterComplex('Supercluster Complex', size=1.0)

        # points = [item.rect.center for item in voids]

        # Calculate Voronoi Polygons
        vor = Voronoi([item.rect.center for item in voids])

        self.clusters = [
            supercluster_complex_factory(
                vertex,
                self.scale,
            )
            for vertex in vor.vertices
        ]

        self.vertices = vor.vertices
        self.filaments = [
            [vor.vertices[id] for id in vertices]
            for vertices in vor.ridge_vertices
            if -1 not in vertices
        ]

        for filament in self.filaments:
            filament_alpha = random.randrange(256)
            filament_color = pygame.Color(255, 255, 255, filament_alpha)
            filament_width = random.randrange(1, 10)
            pygame.draw.line(
                self.image,
                filament_color,
                filament[0],
                filament[1],
                filament_width,
            )
