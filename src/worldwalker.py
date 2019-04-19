from worlds.fantasyNames.witchCoven import WitchCoven
from worlds.fantasyNames.wizard import Wizard
from worlds.fantasyNames.worldDefender import WorldDefender
from worlds.fantasyNames.worldDestroyer import WorldDestroyer
from worlds.fantasyNames.wyvern import Wyvern
from worlds.fantasyNames.yeti import Yeti
from worlds.fantasyNames.zaratan import Zaratan
from worlds.fantasyNames.zombie import Zombie

from worlds.descr.realm import Realm


def listNames(items):
    for itemId, item in enumerate(items):
        print(itemId + 1, str(item))


def generateList(title, item_class, *args):
    print("\n{}".format(title))
    listNames([item_class.generate(*args) for _ in range(10)])


def main():
    print('World Walker')

    generateList("Witch Coven", WitchCoven)

    generateList("Wizard (m)", Wizard, Wizard.MALE)
    generateList("Wizard (f)", Wizard, Wizard.FEMALE)
    generateList("Wizard (n)", Wizard, Wizard.NEUTRAL)

    generateList("World Defender", WorldDefender)
    generateList("World Destroyer", WorldDestroyer)

    generateList("Wyvern (m)", Wyvern, Wyvern.MALE)
    generateList("Wyvern (f)", Wyvern, Wyvern.FEMALE)
    generateList("Wyvern (n)", Wyvern, Wyvern.NEUTRAL)

    generateList("Yeti (m)", Yeti, Yeti.MALE)
    generateList("Yeti (f)", Yeti, Yeti.FEMALE)
    generateList("Yeti (n)", Yeti, Yeti.NEUTRAL)

    generateList("Zaratan", Zaratan)
    generateList("Zombie", Zombie)

    print("\nRealm")
    realm = Realm()
    print(realm.show())


if __name__ == "__main__":
    main()
