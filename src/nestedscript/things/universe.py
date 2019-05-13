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
            # generate_child(BlackHole, probability=20),
            # generate_child(BlackHole, probability=20),
        ]


class GalaxyCenter(Thing):
    thing_name = 'galaxy arm'
    name_generator = NameGenerator(["galactic center"])

    @classmethod
    def generate_children(cls):
        return [
            # generate_child(BlackHole),
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
        NameGenerator([
            "a bright pink", "a faint", "a fading", "a pale", "a fluo", "a glowing", "a green", "a bright green",
            "a dark brown", "a brooding", "a magenta", "a bright red", "a dark red", "a blueish", "a deep blue",
            "a turquoise", "a teal", "a golden", "a multicolored", "a silver", "a dramatic", "a luminous",
            "a colossal", "a purple", "a gold-trimmed", "an opaline", "a silvery", "a shimmering"
        ]),
        NameGenerator(" "),
        NameGenerator("interstellar cloud"),
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
            # generate_child(VisitorPlanet, probability=5),
            # generate_child(FuturePlanet, probability=10),
            # generate_child(TerraformedPlanet, probability=50),
            # generate_child(TerraformedPlanet, probability=20),
            # generate_child(TerraformedPlanet, probability=10),
            # generate_child(MedievalPlanet, probability=30),
            # generate_child(MedievalPlanet, probability=20),
            # generate_child(AncientPlanet, probability=50),
            # generate_child(AncientPlanet, probability=30),
            # generate_child(AncientPlanet, probability=10),
            # generate_child(BarrenPlanet, probability=60),
            # generate_child(BarrenPlanet, probability=40),
            # generate_child(BarrenPlanet, probability=20),
            # generate_child(GasGiant, probability=60),
            # generate_child(GasGiant, probability=40),
            # generate_child(GasGiant, probability=20),
            # generate_child(GasGiant, probability=10),
            # generate_child(AsteroidBelt, (0, 2)),
        ]


class DysonSphere(Thing):
    thing_name = 'dyson sphere'

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Star),
            generate_child(Star, probability=3),
            # generate_child(DysonSurface),
            # generate_child(FuturePlanet, (1, 8)),
            # generate_child(BarrenPlanet, probability=60),
            # generate_child(BarrenPlanet, probability=40),
            # generate_child(BarrenPlanet, probability=20),
            # generate_child(GasGiant, probability=60),
            # generate_child(GasGiant, probability=40),
            # generate_child(GasGiant, probability=20),
            # generate_child(GasGiant, probability=10),
            # generate_child(AsteroidBelt, (0, 2)),
        ]


class Star(Thing):
    thing_name = 'star'
    name_generator = ComplexNameGenerator([
        NameGenerator([
            "white", "faint", "yellow", "red", "blue", "green", "purple", "bright", "double", "twin", "triple", "old",
            "young", "dying", "small", "giant", "large", "pale", "dark", "hell", "horrific", "twisted", "spectral"
        ]),
        NameGenerator(" star"),
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


"""
new Thing("barren planet",["galactic life,10%","rock","ice,50%",".planet composition"],"telluric planet");
new Thing("visitor planet",["visitor city,1-8","visitor installation,2-6","galactic life","rock","ice,50%",".planet composition"],"telluric planet");
new Thing("future planet",["future continent,2-7","ocean,1-7","future sky",".future moon,30%",".planet composition"],"telluric planet");
new Thing("terraformed planet",["continent,2-7","ocean,1-7","terraformed sky",".terraformed moon,30%",".planet composition"],"telluric planet");
new Thing("medieval planet",["medieval continent,2-4","ancient continent,0-3","ocean,1-7","sky",".planet composition"],"telluric planet");
new Thing("ancient planet",["ancient continent,2-7","ocean,1-7","sky",".planet composition"],"telluric planet");
new Thing("planet composition",["planet core","moon,40%","moon,20%","moon,10%"],"planet");
new Thing("moon",["ghost,0.1%","rock","planet core"],[["young","old","large","small","pale","white","dark","black","old"],[" moon"]]);
new Thing("terraformed moon",[".planet composition","continent,1-4","ocean,1-4","sky"],[["young","old","large","small","pale","white","dark","black","old","green","lush","blue","city","colonized","life"],[" moon"]]);
new Thing("asteroid belt",["galactic life,20%","asteroid,10-30"]);
new Thing("earth",[".asteroid belt"],"Earth");
new Thing("asteroid",["space animal,0.5%","rock","ice,30%"],"asteroid");
new Thing("gas giant",["gas giant atmosphere","planet core,50%","moon,0-3","terraformed moon,20%","terraformed moon,10%"]);
new Thing("gas giant atmosphere",["galactic life,10%","helium","hydrogen","water,50%","ammonia,50%","methane,50%"],"atmosphere");
new Thing("planet core",["space monster,0.5%","iron","rock","diamond,2%","magma"],"core");

new Thing("black hole",["inside the black hole"]);
new Thing("inside the black hole",["end of universe note,0.5%","crustacean,0.2%","white hole"]);
new Thing("white hole",["universe"]);
new Thing("42",["universe"]);
new Thing("everything",["universe"]);
new Thing("end of universe note",["pasta,0.1%"],["Help! I'm trapped in a universe factory!","Okay, you can stop clicking now.","I want to get off Mr Orteil's Wild Ride","my sides"]);
new Thing("orteil",["body","orteil psyche","clothing set","computer"],"Orteil");//I do what I want
new Thing("god",[".orteil"],"Orteil");//I'm a fucking god
new Thing("orteil psyche",["orteil thoughts"],"psyche");
new Thing("orteil thoughts",[],["OH MY GOD WHAT ARE YOU DOING HERE TURN BACK IMMEDIATELY","WHAT IS WRONG WITH YOU","WHAT THE HELL GO AWAY","WHAT ARE YOU DOING OH GOD","WHY THE HELL ARE YOU HERE","I DO WHAT I WANT OKAY","NO I DON'T CARE GO AWAY","WHAT DID I EVEN DO TO YOU","OH NO WHY THIS","OKAY JUST <a href=\"http://orteil.deviantart.com\">GO THERE ALREADY</a>","<a href=\"http://twitter.com/orteil42\">WHATEVER</a>"]);
"""
