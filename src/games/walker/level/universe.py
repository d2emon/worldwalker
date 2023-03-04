import random
from .items import load_items
from .level import Level
from ..items.clusters import SuperclusterComplex, Cluster
from ..items.space_walls import Wall
from ..items.space_web import SpaceWeb
from ..items.supervoids import Supervoid


class Universe(Level):
    default_size = 2000, 2000

    hubble_deep_field = 127

    @property
    def grid_step(self):
        return self.hubble_deep_field

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        wall_factory = Wall('Space Wall')
        void_factory = Supervoid('Supervoid')
        supercluster_complex_factory = SuperclusterComplex('Supercluster Complex', size=1.0)

        voids = [
            void_factory(
                [
                    random.randrange(0, self.max_pos[i]) * self.step + self.offset
                    for i in range(2)
                ],
                self.scale,
            )
            for _ in range(10)
        ]

        space_web = SpaceWeb(self.size, voids)

        yield space_web

        for filament in space_web.filaments:
            yield wall_factory(
                [filament[0][id] + (filament[1][id] - filament[0][id]) / 2 for id in range(2)],
                self.scale,
            )

        yield from voids

        for vertex in space_web.vertices:
            yield supercluster_complex_factory(
                vertex,
                self.scale,
            )


class SpaceWall(Level):
    default_size = 1000, 1000
    gigaparsec = 3.3

    @property
    def grid_step(self):
        return int(self.gigaparsec * 100)

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        void_factory = Supervoid('Supervoid')
        supercluster_complex_factory = SuperclusterComplex('Supercluster Complex', size=1.0)
        cluster_factory = Cluster('Cluster', size=2.0)

        voids = [
            void_factory(
                [
                    random.randrange(0, self.max_pos[i]) * self.step + self.offset
                    for i in range(2)
                ],
                self.scale,
            )
            for _ in range(10)
        ]

        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

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
    default_size = 1000, 1000

    @property
    def grid_step(self):
        return 64

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        cluster_factory = Cluster('Cluster', size=2.0)

        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        for _ in range(50):
            size = random.randrange(15, 30) / 10
            yield cluster_factory(
                [
                    random.randrange(0, self.max_pos[i]) * self.step + self.offset
                    for i in range(2)
                ],
                self.scale,
                size=(size, size)
            )
