from .fantasyNames.fairy import Fairy
from .fantasyNames.witch import Witch
from .fantasyNames.witchCoven import WitchCoven
from .fantasyNames.wizard import Wizard
from .fantasyNames.worldDefender import WorldDefender
from .fantasyNames.worldDestroyer import WorldDestroyer
from .fantasyNames.wyvern import Wyvern
from .fantasyNames.yeti import Yeti
from .fantasyNames.zaratan import Zaratan
from .fantasyNames.zombie import Zombie

from .descr.realm import Realm
from .descr.weapons import Shotgun
from .descr.weapons import Staff

from genelib.fng import genders
from .fillers import fill, describe


def world_walker():
    print('World Walker')

    [fill(Fairy, gender=gender) for gender in genders.MF]

    [fill(Witch, gender=gender) for gender in genders.MF]
    fill(WitchCoven)
    [fill(Wizard, gender=gender) for gender in genders.MFN]
    fill(WorldDefender)
    fill(WorldDestroyer)
    [fill(Wyvern, gender=gender) for gender in genders.MF]
    [fill(Yeti, gender=gender) for gender in genders.MF]
    fill(Zaratan)
    fill(Zombie)

    describe(Realm)
    describe(Shotgun)
    describe(Staff)
