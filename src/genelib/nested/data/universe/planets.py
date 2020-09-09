from genelib.nested.names import NameGenerator, ComplexNameGenerator
from genelib.nested.item import NestedItem, generate_child


# class Planet(TerraformedPlanet):
#     thing_name = 'planet'
#     name_generator = NameGenerator(["telluric planet"])


class BarrenPlanet(NestedItem):
    thing_name = 'barren planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(GalacticLife, probability=10),
            # generate_child(Rock),
            # generate_child(Ice, probability=50),
        ] + PlanetComposition.generate_children()


class VisitorPlanet(NestedItem):
    thing_name = 'visitor planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(VisitorCity, (1, 8)),
            # generate_child(VisitorInstallation, (2, 6)),
            # generate_child(GalacticLife, probability=10),
            # generate_child(Rock),
            # generate_child(Ice, probability=50),
        ] + PlanetComposition.generate_children()


class FuturePlanet(NestedItem):
    thing_name = 'future planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(FutureContinent, (2, 7)),
            # generate_child(Ocean, (1, 7)),
            # generate_child(FutureSky),
            # generate_child(FutureMoon, probability=30),
        ] + PlanetComposition.generate_children()


class TerraformedPlanet(NestedItem):
    thing_name = 'barren planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(Continent, (2, 7)),
            # generate_child(Ocean, (1, 7)),
            # generate_child(TerraformedSky),
            generate_child(TerraformedMoon, probability=30),
        ] + PlanetComposition.generate_children()


class MedievalPlanet(NestedItem):
    thing_name = 'barren planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(MedievalContinent, (2, 4)),
            # generate_child(AncientContinent, (0, 3)),
            # generate_child(Ocean, (1, 7)),
            # generate_child(Sky),
        ] + PlanetComposition.generate_children()


class AncientPlanet(NestedItem):
    thing_name = 'barren planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(AncientContinent, (2, 7)),
            # generate_child(Ocean, (1, 7)),
            # generate_child(Sky),
        ] + PlanetComposition.generate_children()


class PlanetComposition(NestedItem):
    thing_name = 'planet composition'
    name_generator = NameGenerator(['planet'])

    @classmethod
    def generate_children(cls):
        return [
            generate_child(PlanetCore),
            generate_child(Moon, probability=40),
            generate_child(Moon, probability=20),
            generate_child(Moon, probability=10),
        ]


class Moon(NestedItem):
    thing_name = 'moon'
    name_generator = ComplexNameGenerator([
        ["young", "old", "large", "small", "pale", "white", "dark", "black", "old"],
        [" moon"],
    ])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(Ghost, probability=0.1),
            # generate_child(Rock),
            generate_child(PlanetCore),
        ]


class TerraformedMoon(Moon):
    thing_name = 'moon'
    name_generator = ComplexNameGenerator([
        [
            "young", "old", "large", "small", "pale", "white", "dark", "black", "old", "green", "lush", "blue", "city",
            "colonized", "life"
        ],
        [" moon"],
    ])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(Continent, (1, 4)),
            # generate_child(Ocean, (1, 4)),
            # generate_child(Sky),
        ] + PlanetComposition.generate_children()