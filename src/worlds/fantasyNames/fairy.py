from ..database import get_data_providers
from genelib import NameGenerator, GenderedNameGenerator, Gendered
from genelib.genders import GENDER_MALE, GENDER_FEMALE


DATABASE = 'fairy'
PARTS = [
    'namesMale',
    'namesFemale',
    'namesFamily',
    'namesFamily2',
]


class BaseFairyNameGenerator(NameGenerator):
    default_providers = get_data_providers(DATABASE, PARTS)
    used_parts = PARTS


class MaleFairyNameGenerator(BaseFairyNameGenerator):
    gender = GENDER_MALE
    template = "{namesMale} {namesFamily}{namesFamily2}"


class FemaleFairyNameGenerator(BaseFairyNameGenerator):
    gender = GENDER_FEMALE
    template = "{namesFemale} {namesFamily}{namesFamily2}"


class Fairy(Gendered):
    """
    Fairies are usually named after natural elements, like plant names or geographical areas, and the names tend to
    sound cute. Which is also the case in this generator.

    The last names consist of a combination of two words, most of them are also related to nature.

    Having said that, some names will sound darker and more mysterious, as not all fairies are cute and innocent, some
    are vicious, vile and evil. I've had quite a few name submissions with 'evil fairy' names, so you'll find those in
    here as well.
    """
    MALE = GENDER_MALE
    FEMALE = GENDER_FEMALE

    name_generator = GenderedNameGenerator({
        MALE: MaleFairyNameGenerator,
        FEMALE: FemaleFairyNameGenerator,
    })
