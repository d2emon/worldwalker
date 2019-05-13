# universe stuff
from ..thing import Thing, generate_child
from ..name_generator import NameGenerator, ComplexNameGenerator

"""
new Thing("multiverse",["universe,10-30"],["multiverse","lasagnaverse","doughnutverse","towelverse","baconverse","sharkverse","nestedverse","tastyverse","upverse","downverse","layerverse","clusterverse","metaverse","quantiverse","paraverse","epiverse","alterverse","hypoverse","dimensioverse","planiverse","pluriverse","polyverse","maniverse","stackoverse","antiverse","superverse","upperverse","maxiverse","megaverse","babyverse","tinyverse","retroverse","ultraverse","topoverse","otherverse","bubbleverse","esreverse","versiverse","'verse","cookieverse","grandmaverse"]);
"""


class Universe(Thing):
    thing_name = 'universe'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Supercluster, (10, 30)),
        ]


class Supercluster(Thing):
    thing_name = 'supercluster'
    name_generator = NameGenerator(["galactic supercluster"])

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Galaxy, (10, 30)),
        ]


class Galaxy(Thing):
    thing_name = 'galaxy'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(GalaxyCenter),
            generate_child(GalaxyArm, (2, 6)),
        ]


class GalaxyArm(Thing):
    thing_name = 'galaxy arm'
    name_generator = NameGenerator(["arm"])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(GalacticLife, probability=5),
            generate_child(DysonSphere, probability=4),
            generate_child(DysonSphere, probability=2),
            generate_child(StarSystem, (20, 50)),
            generate_child(Nebula, (0, 12)),
            generate_child(BlackHole, probability=20),
            generate_child(BlackHole, probability=20),
        ]


class GalaxyCenter(Thing):
    thing_name = 'galaxy arm'
    name_generator = NameGenerator(["galactic center"])

    @classmethod
    def generate_children(cls):
        return [
            generate_child(BlackHole),
            # generate_child(GalacticLife, probability=10),
            generate_child(DysonSphere, probability=4),
            generate_child(DysonSphere, probability=2),
            generate_child(StarSystem, (20, 50)),
            generate_child(Nebula, (0, 12)),
        ]


class Nebula(Thing):
    thing_name = 'nebula'

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(GalacticLife, probability=15),
            generate_child(Star, probability=2),
            generate_child(Star, probability=2),
            generate_child(Star, probability=2),
            generate_child(InterstellarCloud, (1, 6)),
        ]


class InterstellarCloud(Thing):
    thing_name = 'interstellar cloud'
    name_generator = ComplexNameGenerator([
        [
            "a bright pink", "a faint", "a fading", "a pale", "a fluo", "a glowing", "a green", "a bright green",
            "a dark brown", "a brooding", "a magenta", "a bright red", "a dark red", "a blueish", "a deep blue",
            "a turquoise", "a teal", "a golden", "a multicolored", "a silver", "a dramatic", "a luminous",
            "a colossal", "a purple", "a gold-trimmed", "an opaline", "a silvery", "a shimmering"
        ],
        " ",
        "interstellar cloud",
    ])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(Helium),
            # generate_child(Hydrogen),
            # generate_child(Carbon, probability=80),
            # generate_child(Water, probability=5),
            # generate_child(Ammonia, probability=5),
            # generate_child(Nitrogen, probability=5),
            # generate_child(Iron, probability=5),
            # generate_child(Sulfur, probability=5),
            # generate_child(Oxygen, probability=15),
        ]


class StarSystem(Thing):
    thing_name = 'star system'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Star),
            generate_child(Star, probability=3),
            generate_child(VisitorPlanet, probability=5),
            generate_child(FuturePlanet, probability=10),
            generate_child(TerraformedPlanet, probability=50),
            generate_child(TerraformedPlanet, probability=20),
            generate_child(TerraformedPlanet, probability=10),
            generate_child(MedievalPlanet, probability=30),
            generate_child(MedievalPlanet, probability=20),
            generate_child(AncientPlanet, probability=50),
            generate_child(AncientPlanet, probability=30),
            generate_child(AncientPlanet, probability=10),
            generate_child(BarrenPlanet, probability=60),
            generate_child(BarrenPlanet, probability=40),
            generate_child(BarrenPlanet, probability=20),
            generate_child(GasGiant, probability=60),
            generate_child(GasGiant, probability=40),
            generate_child(GasGiant, probability=20),
            generate_child(GasGiant, probability=10),
            generate_child(AsteroidBelt, (0, 2)),
        ]


class DysonSphere(Thing):
    thing_name = 'dyson sphere'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Star),
            generate_child(Star, probability=3),
            # generate_child(DysonSurface),
            generate_child(FuturePlanet, (1, 8)),
            generate_child(BarrenPlanet, probability=60),
            generate_child(BarrenPlanet, probability=40),
            generate_child(BarrenPlanet, probability=20),
            generate_child(GasGiant, probability=60),
            generate_child(GasGiant, probability=40),
            generate_child(GasGiant, probability=20),
            generate_child(GasGiant, probability=10),
            generate_child(AsteroidBelt, (0, 2)),
        ]


class Star(Thing):
    thing_name = 'star'
    name_generator = ComplexNameGenerator([
        [
            "white", "faint", "yellow", "red", "blue", "green", "purple", "bright", "double", "twin", "triple", "old",
            "young", "dying", "small", "giant", "large", "pale", "dark", "hell", "horrific", "twisted", "spectral"
        ],
        " star",
    ])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(Ghost, probability=0.1),
            # generate_child(SpaceMonster, probability=0.2),
            # generate_child(Hydrogen),
            # generate_child(Helium),
        ]

# class Planet(TerraformedPlanet):
#     thing_name = 'planet'
#     name_generator = NameGenerator(["telluric planet"])


class BarrenPlanet(Thing):
    thing_name = 'barren planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(GalacticLife, probability=10),
            # generate_child(Rock),
            # generate_child(Ice, probability=50),
        ] + PlanetComposition.generate_children()


class VisitorPlanet(Thing):
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


class FuturePlanet(Thing):
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


class TerraformedPlanet(Thing):
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


class MedievalPlanet(Thing):
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


class AncientPlanet(Thing):
    thing_name = 'barren planet'
    name_generator = NameGenerator(['telluric planet'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(AncientContinent, (2, 7)),
            # generate_child(Ocean, (1, 7)),
            # generate_child(Sky),
        ] + PlanetComposition.generate_children()


class PlanetComposition(Thing):
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


class Moon(Thing):
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


class AsteroidBelt(Thing):
    thing_name = 'asteroid belt'

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(GalacticLife, probability=20),
            generate_child(Asteroid, (10, 30)),
        ]


"""
new Thing("earth",[".asteroid belt"],"Earth");
"""


class Asteroid(Thing):
    thing_name = 'asteroid'
    name_generator = NameGenerator(['asteroid'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(SpaceAnimal, probability=0.5),
            # generate_child(Rock),
            # generate_child(Ice, probability=30),
        ]


class GasGiant(Thing):
    thing_name = 'gas giant'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(GasGiantAtmosphere),
            generate_child(PlanetCore),
            generate_child(Moon, (0, 3)),
            generate_child(TerraformedMoon, probability=20),
            generate_child(TerraformedMoon, probability=10),
        ]


class GasGiantAtmosphere(Thing):
    thing_name = 'gas giant atmosphere'
    name_generator = NameGenerator(['atmosphere'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(GalacticLife, probability=10),
            # generate_child(Helium),
            # generate_child(Hydrogen),
            # generate_child(Water, probability=50),
            # generate_child(Ammonia, probability=50),
            # generate_child(Methane, probability=50),
        ]


class PlanetCore(Thing):
    thing_name = 'planet core'
    name_generator = NameGenerator(['core'])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(SpaceMonster, probability=0.5),
            # generate_child(Iron),
            # generate_child(Rock),
            # generate_child(Diamond, probability=2),
            # generate_child(Magma),
        ]


class BlackHole(Thing):
    thing_name = 'black hole'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(InsideTheBlackHole),
        ]


class InsideTheBlackHole(Thing):
    thing_name = 'inside the black hole'

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(EndOfUniverseNote, probability=0.5),
            # generate_child(Crustacean, probability=0.2),
            generate_child(WhiteHole),
        ]


class WhiteHole(Thing):
    thing_name = 'white hole'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Universe),
        ]


"""
new Thing("42",["universe"]);
new Thing("everything",["universe"]);
"""


class EndOfUniverseNote(Thing):
    thing_name = 'end of universe note'
    name_generator = NameGenerator([
        "Help! I'm trapped in a universe factory!", "Okay, you can stop clicking now.",
        "I want to get off Mr Orteil's Wild Ride", "my sides"
    ])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(Pasta, probability=0.1),
        ]


"""
new Thing("orteil",["body","orteil psyche","clothing set","computer"],"Orteil");//I do what I want
new Thing("god",[".orteil"],"Orteil");//I'm a fucking god
new Thing("orteil psyche",["orteil thoughts"],"psyche");
new Thing("orteil thoughts",[],["OH MY GOD WHAT ARE YOU DOING HERE TURN BACK IMMEDIATELY","WHAT IS WRONG WITH YOU","WHAT THE HELL GO AWAY","WHAT ARE YOU DOING OH GOD","WHY THE HELL ARE YOU HERE","I DO WHAT I WANT OKAY","NO I DON'T CARE GO AWAY","WHAT DID I EVEN DO TO YOU","OH NO WHY THIS","OKAY JUST <a href=\"http://orteil.deviantart.com\">GO THERE ALREADY</a>","<a href=\"http://twitter.com/orteil42\">WHATEVER</a>"]);
"""
