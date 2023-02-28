from .hubble_deep_field import HubbleDeepField
from .hcb_greate_wall import HerculesCoronaBorealisGreatWall
from .gigaparsec import Gigaparsec
from .eridanus_supervoid import EridanusSupervoid
from .distance_great_attractor import DistanceToGreatAttractor
from .clusters import CLUSTERS
from .galaxies import GALAXIES


ITEMS  = [
    HubbleDeepField,
    HerculesCoronaBorealisGreatWall,
    Gigaparsec,
    EridanusSupervoid,
    DistanceToGreatAttractor,
    *CLUSTERS,
    *GALAXIES,
]