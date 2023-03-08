from .galaxies import GALAXIES as NORMAL_GALAXIES
from .small_galaxies import GALAXIES as SMALL_GALAXIES
from .dwarf_galaxies import GALAXIES as DWARF_GALAXIES


GALAXIES = [
    *NORMAL_GALAXIES,
    *SMALL_GALAXIES,
    *DWARF_GALAXIES,
]
