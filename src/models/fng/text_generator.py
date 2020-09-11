from models.model import Model


class TextGenerator(Model):
    fields = [
        Model.IndexField('slug', ''),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def title(self):
        return self.slug.title()

    def __repr__(self):
        return f'<{self.title} Generator>'
