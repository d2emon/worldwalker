from models.model import Model
from .text_generator import TextGenerator


class DataGroup(Model):
    fields = [
        Model.IndexField('slug'),
        Model.LookupField('text_generator', TextGenerator),
    ]

    @property
    def title(self):
        return self.slug.title() if self.slug else ''

    def __repr__(self):
        return f'<{self.text_generator.title}: {self.title} Data>'
