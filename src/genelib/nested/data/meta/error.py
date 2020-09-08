from genelib.nested.item import NestedItem
from genelib.nested.names import NameGenerator
from .sorry import Sorry


class ErrorItem(NestedItem):
    class ItemGenerator(NestedItem.ItemGenerator):
        default_name = 'error'
        name_generator = NameGenerator("Uh oh... It looks like you didn't supply a valid element to create.")

        @classmethod
        def children(cls):
            return [
                cls.child(Sorry),
            ]
