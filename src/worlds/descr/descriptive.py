from genelib.descriptionGenerator import DescriptionGenerator


class Descriptive:
    description_generator = DescriptionGenerator(dict())

    def __init__(self, **data):
        self.data = data

    @property
    def description(self):
        return self.description_generator.generate(**self.data)
