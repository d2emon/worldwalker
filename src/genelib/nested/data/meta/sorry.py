from genelib.nested.item import NestedItem
from genelib.nested.names import NameGenerator
from .consolation_universe import ConsolationUniverse


class Sorry(NestedItem):
    item_type = 'sorry'

    class ItemGenerator(NestedItem.ItemGenerator):
        description_generator = NameGenerator("(Sorry!)")

        @classmethod
        def children(cls):
            yield lambda: cls.child('ConsolationUniverse')
