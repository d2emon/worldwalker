import random
from .base_name_generator import BaseNameGenerator


class NameGenerator(BaseNameGenerator):
    def __init__(self, names):
        self.names = names

    def get_name(self):
        return random.choice(self.names)
