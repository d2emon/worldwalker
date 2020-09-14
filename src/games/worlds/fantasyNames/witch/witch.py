from genelib.fng.named import Gendered
from genelib.fng.namegen import GenderedFactory
from .male import MaleNameFactory
from .female import FemaleNameFactory


class Witch(Gendered):
    """
    Witches come in all sorts of different types, and while some names might fit an evil witch better than a good witch,
    I've decided to keep them all together in one generator rather than splitting them up with separate buttons. There's
    only so much in a name after all.

    Depending on which type of witchcraft you're dealing with, it's also possible to have male witches. In some cases
    they're called warlocks, sorcerers or wizards, but in others they're simply called wizards. No matter the term the
    names in this generator focus on the more regular sounding names, rather than the more fantasy-themed names you'll
    find in some of the other related name generators.
    """
    class NameFactory(Gendered.NameFactory):
        factory = GenderedFactory(
            male=MaleNameFactory,
            female=FemaleNameFactory,
        )
