from genelib.nested.item import NestedItem
from genelib.nested.names import NameGenerator
from .consolation_universe import ConsolationUniverse


class Sorry(NestedItem):
    class ItemGenerator(NestedItem.ItemGenerator):
        default_name = 'sorry'
        name_generator = NameGenerator("(Sorry!)")

        @classmethod
        def children(cls):
            return [
                cls.child(ConsolationUniverse),
            ]
