from games.worlds.database import genders
from .base import BaseFairyNameGenerator


class FemaleFairyNameGenerator(BaseFairyNameGenerator):
    gender = genders.FEMALE
    template = "{namesFemale} {namesFamily}{namesFamily2}"
