"""Items for map."""

from ..items.hubble_deep_field import HubbleDeepField
from ..items.hcb_greate_wall import HerculesCoronaBorealisGreatWall
from ..items.gigaparsec import Gigaparsec
from ..items.pc_supercluster_complex import PiscesCetusSuperclusterComplex
from ..items.eridanus_supervoid import EridanusSupervoid
from ..items.distance_great_attractor import DistanceToGreatAttractor


def load_items():
    """Items loader.

    Yields:
        pygame.Sprite: Map item
    """
    yield HubbleDeepField((150, 150))
    yield HerculesCoronaBorealisGreatWall((350, 150))
    yield Gigaparsec((450, 150))
    yield PiscesCetusSuperclusterComplex((550, 150))
    yield EridanusSupervoid((550, 150))
    yield DistanceToGreatAttractor((650, 150))
