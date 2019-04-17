from ..database import db_data_provider
from genelib import SyllablicGenerator, Named


class BaseZaratanNameGenerator(SyllablicGenerator):
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
    default_providers = {
        'nm1': db_data_provider('zaratan', 'nm1'),
        'nm2': db_data_provider('zaratan', 'nm2'),
        'nm3': db_data_provider('zaratan', 'nm3'),
        'nm4': db_data_provider('zaratan', 'nm4'),
        'nm5': db_data_provider('zaratan', 'nm5'),
        'nm6': db_data_provider('zaratan', 'nm6'),
    }
    syllable_providers = {
        1: db_data_provider('zaratan', 'nm1'),
        2: db_data_provider('zaratan', 'nm2'),
        3: db_data_provider('zaratan', 'nm3'),
        4: db_data_provider('zaratan', 'nm4'),
        5: db_data_provider('zaratan', 'nm6'),

        6: db_data_provider('zaratan', 'nm5'),
        7: db_data_provider('zaratan', 'nm2'),
    }

    def rules(self, syllables):
        while str(syllables[3]) in (str(syllables[1]), str(syllables[5])):
            syllables[3] = next(self.syllable_generators[3])
        return syllables

    @classmethod
    def join_syllables(cls, syllables, inner=(), *args):
        return cls.GLUE.join([
            str(syllables[1]),
            str(syllables[2]),
            str(syllables[3]),
            str(syllables[4]),
            cls.GLUE.join([str(s) for s in inner]),
            str(syllables[5]),
        ])


class ZaratanNameGenerator1(BaseZaratanNameGenerator):
    pass


class ZaratanNameGenerator2(BaseZaratanNameGenerator):
    def rules(self, syllables):
        syllables = super().rules(syllables)
        while str(syllables[5]) in (str(syllables[2]), str(syllables[4])):
            syllables[5] = next(self.syllable_generators[5])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables(syllables, [
            syllables[6],
            syllables[7],
        ])


class Zaratan(Named):
    name_generators = [
        ZaratanNameGenerator1(),
        ZaratanNameGenerator2(),
    ]
