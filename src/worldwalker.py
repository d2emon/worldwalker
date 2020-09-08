from worlds.fantasyNames.fairy import Fairy
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
from worlds.descr.weapons.shotgun import Shotgun
from worlds.descr.weapons.staff import Staff

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


def generate_description(title, item_class):
    item = item_class()
    print("\n{}".format(title))
    print(item.description)


def main():
    print('World Walker')

    generate_gendered("Fairy", Fairy, [Fairy.MALE, Fairy.FEMALE])

    generate_gendered("Witch", Witch, [Witch.MALE, Witch.FEMALE])
    generate_list("Witch Coven", WitchCoven)
    generate_gendered("Wizard", Wizard, [Wizard.MALE, Wizard.FEMALE, Wizard.NEUTRAL])
    generate_list("World Defender", WorldDefender)
    generate_list("World Destroyer", WorldDestroyer)
    generate_gendered("Wyvern", Wyvern, [Wyvern.MALE, Wyvern.FEMALE, Wyvern.NEUTRAL])
    generate_gendered("Yeti", Yeti, [Yeti.MALE, Yeti.FEMALE, Yeti.NEUTRAL])
    generate_list("Zaratan", Zaratan)
    generate_list("Zombie", Zombie)

    generate_description("Realm", Realm)
    generate_description("Shotgun", Shotgun)
    generate_description("Staff", Staff)


if __name__ == "__main__":
    main()