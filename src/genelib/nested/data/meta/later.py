from genelib.nested.item import NestedItem
from genelib.nested.names import NameGenerator
from .sorry import Sorry


class Later(NestedItem):
    item_type = 'later'

    class ItemGenerator(NestedItem.ItemGenerator):
        description_generator = NameGenerator("will do later")

        @classmethod
        def children(cls):
            yield lambda: cls.child('Sorry')
