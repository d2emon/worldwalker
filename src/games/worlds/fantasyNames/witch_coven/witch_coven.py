from genelib.fng.named import Named
from genelib.fng.namegen import ComplexFactory
from .name import NameFactory1, NameFactory2


class WitchCoven(Named):
    """
    A coven is a group of witches, which can come in different forms depending on the type of witchcraft the witches
    belong to. The coven might be a community of many, a mere handful or anything in between. It could be a permanent
    group or merely a temporary gathering and so on.

    Coven names can also vary greatly, although I did notice several themes in existing coven names and I used these
    themes for the names in this generator. A coven's name is usually a very personal choice however, but hopefully
    this name generator will be helpful nonetheless.
    """

    class NameFactory(Named.NameFactory):
        factory = ComplexFactory(
            *(NameFactory1 for _ in range(0, 5)),
            *(NameFactory2 for _ in range(5, 10)),
        )
