from worlds.fantasyNames.yeti import Yeti
from worlds.fantasyNames.zaratan import Zaratan
from worlds.fantasyNames.zombie import Zombie

from worlds.descr.realm import Realm


def listNames(items):
    for itemId, item in enumerate(items):
        print(itemId + 1, str(item))

def main():
    print('World Walker')
    print("\nYeti")
    listNames(Yeti.generate())
    print("\nZaratan")
    listNames(Zaratan.generate())
    print("\nZombie")
    listNames(Zombie.generate())

    print("\nRealm")
    realm = Realm()
    print(realm.show())


if __name__ == "__main__":
    main()
