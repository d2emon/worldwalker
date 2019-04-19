from worlds.fantasyNames.witch import Witch
from worlds.fantasyNames.witchCoven import WitchCoven
from worlds.fantasyNames.wizard import Wizard
from worlds.fantasyNames.worldDefender import WorldDefender
from worlds.fantasyNames.worldDestroyer import WorldDestroyer
from worlds.fantasyNames.wyvern import Wyvern
from worlds.fantasyNames.yeti import Yeti
from worlds.fantasyNames.zaratan import Zaratan
from worlds.fantasyNames.zombie import Zombie

from worlds.descr.realm import Realm


GENDERS = {
    0: chr(9893),
    1: chr(9794),
    2: chr(9792),
}


def list_names(items):
    for itemId, item in enumerate(items):
        print(itemId + 1, str(item))


def generate_list(title, item_class, *args):
    print("\n{}".format(title))
    list_names([item_class.generate(*args) for _ in range(10)])


def generate_gendered(title, item_class, genders):
    for gender in genders:
        gender_title = "{} ({})".format(
            title,
            GENDERS[gender],
        )
        generate_list(gender_title, item_class, gender)


def main():
    print('World Walker')

    generate_gendered("Witch", Witch, [Witch.MALE, Witch.FEMALE])
    generate_list("Witch Coven", WitchCoven)
    generate_gendered("Wizard", Wizard, [Wizard.MALE, Wizard.FEMALE, Wizard.NEUTRAL])
    generate_list("World Defender", WorldDefender)
    generate_list("World Destroyer", WorldDestroyer)
    generate_gendered("Wyvern", Wyvern, [Wyvern.MALE, Wyvern.FEMALE, Wyvern.NEUTRAL])
    generate_gendered("Yeti", Yeti, [Yeti.MALE, Yeti.FEMALE, Yeti.NEUTRAL])
    generate_list("Zaratan", Zaratan)
    generate_list("Zombie", Zombie)

    print("\nRealm")
    realm = Realm()
    print(realm.show())


if __name__ == "__main__":
    main()
