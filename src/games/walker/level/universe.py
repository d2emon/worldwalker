import random
from .items import load_items
from .level import Level
from ..items.clusters import SuperclusterComplex, Cluster
from ..items.distance import Distance
from ..items.map_label import MapLabel
from ..items.space_walls import Wall
from ..items.space_web import SpaceWeb
from ..items.supervoids import Supervoid


class Universe(Level):
    hubble_deep_field = 127
    cell = hubble_deep_field
    default_size = [cell * 10] * 2
    zoom_size = 99, 99


    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # Factories
        wall_factory = Wall('Space Wall')

        # From items database
        yield MapLabel(
            'Universe',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        yield MapLabel(
            'Hubble Deep Field',
            rect=(0, 50, 200, 100),
            font_size=16,
        )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        for _ in range(10):
           yield wall_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(80, 100) / 10] * 2,
            )


class SpaceWall(Level):
    gigaparsec = 3.3
    cell = int(gigaparsec * 100)
    default_size = [cell * 3] * 2
    voids_count = 20
    zoom_size = 96, 96

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # Factories
        void_factory = Supervoid('Supervoid')
        supercluster_complex_factory = SuperclusterComplex('Supercluster Complex')
        cluster_factory = Cluster('Cluster')

        # From items database
        yield MapLabel(
            'Space Wall',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        yield MapLabel(
            'Gigaparsec',
            rect=(0, 50, 200, 100),
            font_size=16,
        )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        voids = [
            void_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(60, 80) / 10] * 2
            )
            for _ in range(self.voids_count)
        ]

        space_web = SpaceWeb(self.size, voids)

        yield space_web

        yield from voids

        for vertex in space_web.vertices:
            if random.randrange(100) < 10:
                yield supercluster_complex_factory(
                    vertex,
                    self.scale,
                    size=[random.randrange(5, 15) / 10] * 2
                )
            else:
                yield cluster_factory(
                    vertex,
                    self.scale,
                    size=[random.randrange(15, 30) / 10] * 2
                )


class SuperclusterComplexLevel(Level):
    distance_to_shapley_supercluster = 6.4
    cell = int(distance_to_shapley_supercluster * 10)
    default_size = [cell * 15] * 2
    clusters_count = 100
    zoom_size = 160, 160

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # Factories
        cluster_factory = Cluster('Cluster', size=2.0)
        distance_factory = Distance('Distance to Great Attractor', scale=24, size=1.9, color=(0, 255, 0))

        # From items database
        yield MapLabel(
            'Supercluster Complex',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        yield MapLabel(
            'Distance to the Shapley Superclaster',
            rect=(0, 50, 200, 100),
            font_size=16,
        )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        for _ in range(self.clusters_count):
            size = random.randrange(15, 30) / 10
            yield cluster_factory(
                self.random_point(),
                self.scale,
                size=(size, size)
            )

        # Distance
        distance = distance_factory(
            self.starting_pos,
            self.scale,
        )
        yield distance


class SupervoidLevel(Level):
    distance_to_shapley_supercluster = 6.4
    cell = int(distance_to_shapley_supercluster * 10)
    default_size = [cell * 15] * 2
    clusters_count = 10
    zoom_size = 165, 165

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # Factories
        void_factory = Supervoid('Supervoid')
        cluster_factory = Cluster('Cluster', size=2.0)
        distance_factory = Distance('Distance to Great Attractor', scale=24, size=1.9, color=(0, 255, 0))

        # From items database
        yield MapLabel(
            'Supervoid',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        yield MapLabel(
            'Distance to the Shapley Superclaster',
            rect=(0, 50, 200, 100),
            font_size=16,
        )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        yield void_factory(
            self.starting_pos,
            self.scale,
            size=[random.randrange(60, 80) / 10] * 2
        )

        for _ in range(self.clusters_count):
            size = random.randrange(15, 30) / 10
            yield cluster_factory(
                self.random_point(),
                self.scale,
                size=(size, size)
            )

        # Distance
        distance = distance_factory(
            self.starting_pos,
            self.scale,
        )
        yield distance
