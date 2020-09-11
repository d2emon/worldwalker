from games.worlds.database import genders
from games.worlds.genelib import GenderedNameGenerator, Gendered
from .male import MaleFairyNameGenerator
from .female import FemaleFairyNameGenerator


class Fairy(Gendered):
    """
    Fairies are usually named after natural elements, like plant names or geographical areas, and the names tend to
    sound cute. Which is also the case in this generator.

    The last names consist of a combination of two words, most of them are also related to nature.

    Having said that, some names will sound darker and more mysterious, as not all fairies are cute and innocent, some
    are vicious, vile and evil. I've had quite a few name submissions with 'evil fairy' names, so you'll find those in
    here as well.
    """
    MALE = genders.MALE
    FEMALE = genders.FEMALE

    name_generator = GenderedNameGenerator({
        MALE: MaleFairyNameGenerator,
        FEMALE: FemaleFairyNameGenerator,
    })
