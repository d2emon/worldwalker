from .base_name_generator import BaseNameGenerator
from .name_generator import NameGenerator


class ComplexNameGenerator(BaseNameGenerator):
    def __init__(self, parts):
        self.generators = [NameGenerator(part) for part in parts]

    def get_name(self):
        return "".join([part.generate() for part in self.generators])
