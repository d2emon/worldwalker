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

from . import main


def world_walker():
    print('World Walker')

    main.generate_gendered("Fairy", Fairy, [Fairy.MALE, Fairy.FEMALE])

    main.generate_gendered("Witch", Witch, [Witch.MALE, Witch.FEMALE])
    main.generate_list("Witch Coven", WitchCoven)
    main.generate_gendered("Wizard", Wizard, [Wizard.MALE, Wizard.FEMALE, Wizard.NEUTRAL])
    main.generate_list("World Defender", WorldDefender)
    main.generate_list("World Destroyer", WorldDestroyer)
    main.generate_gendered("Wyvern", Wyvern, [Wyvern.MALE, Wyvern.FEMALE, Wyvern.NEUTRAL])
    main.generate_gendered("Yeti", Yeti, [Yeti.MALE, Yeti.FEMALE, Yeti.NEUTRAL])
    main.generate_list("Zaratan", Zaratan)
    main.generate_list("Zombie", Zombie)

    main.generate_description("Realm", Realm)
    main.generate_description("Shotgun", Shotgun)
    main.generate_description("Staff", Staff)
