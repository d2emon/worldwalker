from genelib.nested.item import NestedItem
from genelib.nested.names import NameGenerator
from .sorry import Sorry


class Later(NestedItem):
    class ItemGenerator(NestedItem.ItemGenerator):
        default_name = 'later'
        name_generator = NameGenerator("will do later")

        @classmethod
        def children(cls):
            return [
                cls.child(Sorry),
            ]
