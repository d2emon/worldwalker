from models.model import Model
from .data_group import DataGroup


class DataItem(Model):
    fields = [
        Model.IndexField('item_id'),
        Model.Field('text', ''),
        Model.LookupField('group', DataGroup),
    ]

    @property
    def text_generator(self):
        return self.group.text_generator

    def __repr__(self):
        return f'<{self.text_generator.title}[{self.group.title}]: "{self.text}">'
