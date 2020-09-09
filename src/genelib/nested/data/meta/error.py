from genelib.nested.item import NestedItem
from genelib.nested.names import NameGenerator
from .sorry import Sorry


class ErrorItem(NestedItem):
    item_type = 'error'

    class ItemGenerator(NestedItem.ItemGenerator):
        description_generator = NameGenerator("Uh oh... It looks like you didn't supply a valid element to create.")

        @classmethod
        def children(cls):
            yield lambda: cls.child('Sorry')
