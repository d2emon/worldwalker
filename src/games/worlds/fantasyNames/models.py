from genelib.fng.named import Gendered, Named
from .fairy.model import Fairy
from .witch.model import Witch
from .witch_coven.model import WitchCoven
from .wizard import NameFactory as WizardNameFactory
from .worldDefender import NameFactory as WorldDefenderNameFactory
from .worldDestroyer import NameFactory as WorldDestroyerNameFactory
from .wyvern import NameFactory as WyvernNameFactory
from .yeti import NameFactory as YetiNameFactory
from .zaratan import NameFactory as ZaratanNameFactory
from .zombie import NameFactory as ZombieNameFactory


class Elf(Gendered):
    pass


class Gnome(Gendered):
    pass


class Troll(Gendered):
    pass


class Wizard(Gendered):
    """
    Wizard names vary greatly from one work of fiction to another. Some choose to stick more to real names, like many
    names in Harry Potter, while others stick to fantasy-style names, like in Lord of the Rings.

    This generator generally sticks to the fantasy-style names, as there are plenty of name generators for real names.
    However, there are plenty of names which could also be used as a fairly unique real name.

    I've also tried to make sure many different types of fantasy styles are part of this generator, from the more
    easily pronounceable friendly names, to the less pronounceable, demonic or evil sounding names.
    """
    name_factory = WizardNameFactory


class WorldDefender(Named):
    """
    There are all sorts of world defenders of course. Godly beings with vast powers, fighters who've sworn to protect
    all life, or even just a humble activist trying to make the world a better place. While this generator generally
    focuses more on the fantasy themed world defenders, the names in this generator could fit every kind of world
    defender.

    The names in this generator, which could arguably simply be called titles, come in the forms of names like 'The
    World Warden', 'Keeper of Life', and 'The Ancient Shepherd'. Some names will fit certain types of defenders better
    than others, but there's plenty to pick from, so you're bound to find a name that suits your needs.
    """
    name_factory = WorldDefenderNameFactory


class WorldDestroyer(Named):
    """
    World destroyers come in many different shapes and sizes, from a relatively small creature with (un)godly powers to
    massive, planet-sized beings who consume entire galaxies. This name generator is aimed at all of those and anything
    in between, though, to some extent, you could see the names in this generator as titles, rather than as names.
    You'll find results like 'Ruiner of Realms', 'The Grand Consumer' and 'Undoer of Life'.

    If you combine them you could end up with a long sequence of titles, similar to how royalty sometimes has multiple
    titles, but in a more gruesome way when it comes to world destroyers.
    """
    name_factory = WorldDestroyerNameFactory


class Wyvern(Gendered):
    """
    Wyverns are creatures similar to dragons, except they only have 2 legs and usually a barbed tail. Wyverns usually
    also don't breathe fire either, but their bite is venemous. However, all these details vary from work of fiction to
    work of fiction.

    As far as names go, wyvern names tend to be far more vicious sounding than their dragon counterparts, perhaps
    because wyverns are often depicted as less intelligent and more animalistic and aggressive or perhaps for a
    different reason entirely. Either way I focused on these kinds of names in this generator. If you are looking for
    more melodic names the dragon name generator is a great place to start.
    """
    name_factory = WyvernNameFactory


class Yeti(Gendered):
    """
    Yetis are ape-like humanoids who supposedly inhabit the Himalayan regions and are part of popular folklore,
    religion and mythologies. There are many variants in other regions too, like Bigfoot, the Yeren, the Yowie and so
    on.

    Yetis and similar creatures aren't often given personal names, in many cases because they're the only specimen
    believed to exist. This made creating a name generator a little tricky, but since these creatures do inhabit
    specific regions of the world I decided to take inspiration from those regions to create naming conventions. I
    focused primarily on the Himalayan regions, but also took some inspiration for some of the lesser known variants of
    'yeti' out there, like the before mentioned Yeren and Yowie.
    """
    name_factory = YetiNameFactory


class Zaratan(Named):
    """
    Zaratan are giant sea turtles, big enough to support a small island ecosystem on their shells. As a result they're
    often mistaken for islands, especially when they're in the middle of the ocean, and their movement is difficult to
    detect.

    Zaratan are common in many works of fiction, but vary a lot in terms of personality, purpose, and any meaning they
    may have. In some cases they're wise, in some they're aggressive, and in others they might simply be docile beings
    swimming across the oceans. Unfortunately there wasn't much to work with in terms of names, but the term zaratan
    does seem to come from Spanish.

    For this generator I mostly focused on bigger sounding names, often with more melodic and gentle tones. But I also
    included Spanish influences, as well as some other influences for a wider variety of possible names. The names will
    generally still have the same large and docile feel to them, but there's plenty to pick from on both ends of the
    spectrum.
    """
    name_factory = ZaratanNameFactory


class Zombie(Named):
    """
    Zombies come in many shapes and sizes, many of which have their own nickname or type name. From bloaters and
    belchers to crawlers and runners, there's hundreds of different types of zombies both in fiction and in this
    generator, so there's plenty to pick from and plenty to fill your zombie world with.
    """
    name_factory = ZombieNameFactory
