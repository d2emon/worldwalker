# meta
from genelib.nested.names import NameGenerator
from ..thing import Thing, generate_child

from .universe import Universe


class Later(Thing):
    thing_name = 'later'
    name_generator = NameGenerator("will do later")

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Sorry),
        ]


class ErrorThing(Thing):
    thing_name = 'error'
    name_generator = NameGenerator("Uh oh... It looks like you didn't supply a valid element to create.")

    @classmethod
    def generate_children(cls):
        return [
            generate_child(Sorry),
        ]


class Sorry(Thing):
    thing_name = 'sorry'
    name_generator = NameGenerator("(Sorry!)")

    @classmethod
    def generate_children(cls):
        return [
            generate_child(ConsolationUniverse),
        ]


class ConsolationUniverse(Universe):
    thing_name = 'consolation universe'
