from .hubble_deep_field import HubbleDeepField
from .hcb_greate_wall import HerculesCoronaBorealisGreatWall
from .eridanus_supervoid import EridanusSupervoid
from .distance_great_attractor import DistanceToGreatAttractor
from .clusters import CLUSTERS
from .galaxies import GALAXIES
from .nebulas import NEBULAS
from .globular_clusters import GLOBULAR_CLUSTERS
from .sun_system import OortsCloud, KuipersBelt, DistanceFromVoyager, DistanceFromNeptune, DistanceFromEarth, DistanceToMoon
from .light_year import LightYear, LightDay
from .parsec import Parsec, Gigaparsec
from .from_sun import DistanceFromSunToProximaCentauri, DistanceFromAlphaToProximaCentauri, DistanceFromSedna, DistanceFromHaleBopp
from .stars import STARS
from .total_human import TotalHumanHeight
from .planets import PLANETS
from .countries import COUNTRIES
from .structures import STRUCTURES
from .mountains import MOUNTAINS
from .marathon import Marathon
from .comets import COMETS


ITEMS  = [
    HubbleDeepField,
    HerculesCoronaBorealisGreatWall,
    Gigaparsec,
    EridanusSupervoid,
    DistanceToGreatAttractor,
    *CLUSTERS,
    *GALAXIES,
    *NEBULAS,
    *GLOBULAR_CLUSTERS,
    OortsCloud, KuipersBelt, DistanceFromVoyager, DistanceFromNeptune, DistanceFromEarth, DistanceToMoon,
    LightYear, LightDay,
    Parsec,
    DistanceFromSunToProximaCentauri, DistanceFromAlphaToProximaCentauri, DistanceFromSedna, DistanceFromHaleBopp,
    *STARS,
    TotalHumanHeight,
    *PLANETS,
    *COUNTRIES,
    *STRUCTURES,
    *MOUNTAINS,
    Marathon,
    *COMETS,
]