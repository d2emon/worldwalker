from .data_provider import DataProvider
from .name_generator import ListNameGenerator, SyllablicGenerator, build_name_generator


def unique_with(*syllable_ids):
    def f(syllable, syllables):
        return str(syllable) not in [str(syllables[syllable_id]) for syllable_id in syllable_ids]
    return f
