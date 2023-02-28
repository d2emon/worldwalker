from .pc_supercluster_complex import PiscesCetusSuperclusterComplex
from .distance_to_shapley import DistanceToShapley
from .fornax import FornaxCluster
from .virgo import VirgoSupercluster, VirgoCluster
from .abell_2029 import Abell2029


CLUSTERS = [
    PiscesCetusSuperclusterComplex,
    DistanceToShapley,
    VirgoSupercluster,
    FornaxCluster,
    VirgoCluster,
    Abell2029,
]
