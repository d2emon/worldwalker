# From 10^24 to 10^27
# Point: Supercluster
from genelib.nested import Universe, CosmicWall, GalaxyFilament, Supervoid, Supercluster


def sphere(diameter):
    return [diameter] * 3


SIZE = 1.6 * 1000

ObservableUniverse = Universe(sphere(9.3 * 1000))
DistanceToHubbleDeepField = 1.27 * 100

Gigaparsec = 3.3 * 10
SloanGreatWall = CosmicWall(sphere(1.3 * 10))
PerseusCetusSuperclusterComplex = GalaxyFilament(sphere(1 * 10))

DistanceToShapleySupercluster = 6.5
EridanusSupervoid = Supervoid(sphere(5))
DistanceToGreatAttractor = 2.5
VirgoSupercluster = Supercluster(sphere(1.1))
