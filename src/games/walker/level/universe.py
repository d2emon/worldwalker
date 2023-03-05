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
    __cell = hubble_deep_field
    default_size = [__cell * 10] * 2

    @property
    def grid_step(self):
        return self.__cell

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # Factories
        wall_factory = Wall('Space Wall')
        # void_factory = Supervoid('Supervoid')
        # supercluster_complex_factory = SuperclusterComplex('Supercluster Complex', size=1.0)

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
            )

        # voids = [
        #     void_factory(
        #         self.random_point(),
        #         self.scale,
        #     )
        #     for _ in range(10)
        # ]

        # space_web = SpaceWeb(self.size, voids)

        # yield space_web

        # for filament in space_web.filaments:
        #     yield wall_factory(
        #         [filament[0][id] + (filament[1][id] - filament[0][id]) / 2 for id in range(2)],
        #         self.scale,
        #     )

        # yield from voids

        # for vertex in space_web.vertices:
        #     yield supercluster_complex_factory(
        #         vertex,
        #         self.scale,
        #     )


class SpaceWall(Level):
    gigaparsec = 3.3
    __cell = int(gigaparsec * 100)
    default_size = [__cell * 3] * 2
    voids_count = 20

    @property
    def grid_step(self):
        return self.__cell

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # Factories
        void_factory = Supervoid('Supervoid')
        supercluster_complex_factory = SuperclusterComplex('Supercluster Complex', size=1.0)
        cluster_factory = Cluster('Cluster', size=2.0)

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
            )
            for _ in range(self.voids_count)
        ]

        space_web = SpaceWeb(self.size, voids)

        yield space_web

        yield from voids

        for vertex_id, vertex in enumerate(space_web.vertices):
            if vertex_id == 0:
                yield supercluster_complex_factory(
                    vertex,
                    self.scale,
                )
            else:
                size = random.randrange(15, 30) / 10
                yield cluster_factory(
                    vertex,
                    self.scale,
                    size=(size, size)
                )


class SuperclusterComplexLevel(Level):
    distance_to_shapley_supercluster = 6.4
    __cell = int(distance_to_shapley_supercluster * 10)
    default_size = [__cell * 15] * 2
    clusters_count = 100

    @property
    def grid_step(self):
        return self.__cell

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
