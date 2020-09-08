from .name_generator import NameGenerator
from .complex_name_generator import ComplexNameGenerator


def name_generator(data):
    if isinstance(data, str):
        return NameGenerator([data])
    elif isinstance(data[0], str):
        return NameGenerator(data)
    return ComplexNameGenerator(data)
