from .distances import DISTANCES
from .space_walls import WALLS
from .supervoids import SUPERVOIDS
from .clusters import CLUSTERS
from .galaxies import GALAXIES
from .nebulas import NEBULAS
from .globular_clusters import GLOBULAR_CLUSTERS
from .sun_system import OortsCloud, KuipersBelt, DistanceFromVoyager, DistanceFromNeptune, DistanceFromEarth, DistanceToMoon
from .light_year import LightYear, LightDay
from .measures import MEASURES
from .from_sun import DistanceFromSunToProximaCentauri, DistanceFromAlphaToProximaCentauri, DistanceFromSedna, DistanceFromHaleBopp
from .stars import STARS
from .total_human import TotalHumanHeight
from .planets import PLANETS
from .countries import COUNTRIES
from .structures import STRUCTURES
from .mountains import MOUNTAINS
from .marathon import Marathon
from .comets import COMETS


CLASSES  = [
    *GALAXIES,
    *NEBULAS,
    *GLOBULAR_CLUSTERS,
    OortsCloud, KuipersBelt, DistanceFromVoyager, DistanceFromNeptune, DistanceFromEarth, DistanceToMoon,
    LightYear, LightDay,
    # Parsec,
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
ITEMS = [
    *DISTANCES,
    *WALLS,
    *SUPERVOIDS,
    *MEASURES,
    *CLUSTERS,
    *(
        c(
            name=c.name,
            scale=c.base_scale,
            size=c.base_size,
            color=c.color,
            border=c.border,
        )
        for c in CLASSES
    ),
]
