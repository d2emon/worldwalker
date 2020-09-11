from genelib.fng.named import Gendered
from genelib.fng.namegen import GenderedFactory
from .male import MaleNameFactory
from .female import FemaleNameFactory


class Fairy(Gendered):
    """
    Fairies are usually named after natural elements, like plant names or geographical areas, and the names tend to
    sound cute. Which is also the case in this generator.

    The last names consist of a combination of two words, most of them are also related to nature.

    Having said that, some names will sound darker and more mysterious, as not all fairies are cute and innocent, some
    are vicious, vile and evil. I've had quite a few name submissions with 'evil fairy' names, so you'll find those in
    here as well.
    """
    class NameFactory(Gendered.NameFactory):
        factory = GenderedFactory(
            male=MaleNameFactory,
            female=FemaleNameFactory,
        )
