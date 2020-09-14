from genelib.fng.named import Named
from genelib.fng.namegen import ComplexFactory
from ..database.provider import group_providers_from_list, group_providers_from_dict
from games.worlds.genelib import SyllablicGenerator, unique_with


class BaseZaratanNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1
    default_providers = group_providers_from_list('zaratan', [
        'nm1',
        'nm2',
        'nm3',
        'nm4',
        'nm5',
        'nm6',
    ])
    syllable_providers = group_providers_from_dict('zaratan', {
        1: 'nm1',
        2: 'nm2',
        3: 'nm3',
        4: 'nm4',
        5: 'nm6',

        6: 'nm5',
        7: 'nm2',
    })
    templates = {
        NAME_V1: (1, 2, 3, 4, 5),
        NAME_V2: (1, 2, 3, 4, 6, 7, 5),
    }

    @classmethod
    def template(cls):
        return cls.templates[cls.name_type]

    def name_rules(self):
        return {
            3: unique_with(1, 5),
        }


class ZaratanNameGenerator1(BaseZaratanNameGenerator):
    pass


class ZaratanNameGenerator2(BaseZaratanNameGenerator):
    def name_rules(self):
        rules = super().name_rules()
        rules[5] = unique_with(2, 4)
        return rules


class Zaratan(Named):
    """
    Zaratan are giant sea turtles, big enough to support a small island ecosystem on their shells. As a result they're
    often mistaken for islands, especially when they're in the middle of the ocean, and their movement is difficult to
    detect.

    Zaratan are common in many works of fiction, but vary a lot in terms of personality, purpose, and any meaning they
    may have. In some cases they're wise, in some they're aggressive, and in others they might simply be docile beings
    swimming across the oceans. Unfortunately there wasn't much to work with in terms of names, but the term zaratan
    does seem to come from Spanish.

    For this generator I mostly focused on bigger sounding names, often with more melodic and gentle tones. But I also
    included Spanish influences, as well as some other influences for a wider variety of possible names. The names will
    generally still have the same large and docile feel to them, but there's plenty to pick from on both ends of the
    spectrum.
    """

    class NameFactory(Named.NameFactory):
        factory = ComplexFactory(
            *(ZaratanNameGenerator1 for _ in range(0, 5)),
            *(ZaratanNameGenerator2 for _ in range(5, 10)),
        )
