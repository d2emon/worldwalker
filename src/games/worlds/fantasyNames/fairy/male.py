from games.worlds.database import genders
from .base import BaseFairyNameGenerator


class MaleFairyNameGenerator(BaseFairyNameGenerator):
    gender = genders.MALE
    template = "{namesMale} {namesFamily}{namesFamily2}"
