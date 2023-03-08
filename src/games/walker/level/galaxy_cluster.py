import random
from .items import load_items
from .level import Level
from ..items.clusters import Cluster, GalaxyGroup
from ..items.galaxies.galaxies import Galaxy
from ..items.galaxies.small_galaxies import SmallGalaxy
from ..items.galaxies.dwarf_galaxies import DwarfGalaxy
from ..items.distance import Distance
from ..items.map_label import MapLabel


class GalaxyClusterLevel(Level):
    megaparsec = 3.3
    cell = int(megaparsec * 10)
    default_size = [cell * 50] * 2
    clusters_count = 5
    groups_count = 5
    galaxies_count = 10
    zoom_size = 132, 132

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # From items database
        yield MapLabel(
            'Galaxy Clusters',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        yield MapLabel(
            'Megaparsec',
            rect=(0, 50, 200, 100),
            font_size=16,
        )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        cluster_factory = Cluster('Cluster')
        for _ in range(self.clusters_count):
            yield cluster_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 30) / 10] * 2
            )

        group_factory = GalaxyGroup('Galaxy Group')
        for _ in range(self.groups_count):
            yield group_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(50, 100) / 10] * 2
            )

        galaxy_factory = Galaxy('Galaxy')
        for _ in range(self.galaxies_count):
            yield galaxy_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 50) / 10] * 2
            )

        # Distance
        distance_factory = Distance('Distance to the Shapley Superclaster', scale=21 + 2, size=3.20, color=(0, 255, 0))
        distance = distance_factory(
            self.starting_pos,
            self.scale,
        )
        yield distance


class GalaxyGroupComplexLevel(Level):
    megaparsec = 3.3
    cell = int(megaparsec * 100)
    default_size = [cell * 4] * 2
    galaxies_count = 20
    zoom_size = 300, 300

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # From items database
        yield MapLabel(
            'Galaxy Groups',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        yield MapLabel(
            'Megaparsec',
            rect=(0, 50, 200, 100),
            font_size=16,
        )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        group_factory = GalaxyGroup('Galaxy Group')
        yield group_factory(
            self.starting_pos,
            self.scale,
            size=[random.randrange(10, 30) / 10] * 2
        )

        galaxy_factory = Galaxy('Galaxy')
        for _ in range(self.galaxies_count):
            yield galaxy_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 50) / 10] * 2
            )

        small_galaxy_factory = SmallGalaxy('Galaxy')
        for _ in range(self.galaxies_count):
            yield small_galaxy_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 100) / 10] * 2
            )

        # Distance
        distance_factory = Distance('Distance to Andromeda Galaxy', scale=21 + 1, size=2.3, color=(0, 255, 0))
        # distance_factory = Distance('Distance Earth has Travelled (Relative to Sun)', scale=21, size=4.5, color=(0, 255, 0))
        distance = distance_factory(
            self.starting_pos,
            self.scale,
        )
        yield distance


class GalaxyGroupLevel(Level):
    distance = 10.0
    cell = int(distance * 10)
    default_size = [cell * 30] * 2
    clusters_count = 100
    galaxies_count = 20
    zoom_size = 500, 500

    @property
    def items_data(self):
        print('scale', self.scale, self.step)

        # From items database
        yield MapLabel(
            'Galaxy Group',
            rect=(0, 0, 200, 100),
            font_size=32,
        )
        # yield MapLabel(
        #     'Distance to the Shapley Superclaster',
        #     rect=(0, 50, 200, 100),
        #     font_size=16,
        # )
        yield from load_items(
            self.scale,
            self.size,
            step=self.step,
        )

        # Other
        galaxy_factory = Galaxy('Galaxy')
        for _ in range(self.galaxies_count):
            yield galaxy_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 50) / 10] * 2
            )

        small_galaxy_factory = SmallGalaxy('Galaxy')
        for _ in range(self.galaxies_count):
            yield small_galaxy_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 100) / 10] * 2
            )

        dwarf_galaxy_factory = DwarfGalaxy('Galaxy')
        for _ in range(self.galaxies_count):
            yield dwarf_galaxy_factory(
                self.random_point(),
                self.scale,
                size=[random.randrange(10, 100) / 10] * 2
            )

        # Distance
        # distance_factory = Distance('Distance to Great Attractor', scale=24, size=1.9, color=(0, 255, 0))
        # distance = distance_factory(
        #     self.starting_pos,
        #     self.scale,
        # )
        # yield distance
