from genelib.fng.namegen import ComplexFactory, NamedFactory
from .data_provider import DataProvider


class ListNameGenerator(NamedFactory):
    default_provider = DataProvider([])

    template = "{provider}"

    def __init__(self, provider=None):
        provider = provider or self.default_provider
        super().__init__({'provider': provider})


class SyllableGenerator(ListNameGenerator):
    def __init__(self, provider):
        super().__init__(provider)

    def name(self, **kwargs):
        return next(self.data['provider'])


class SyllablicGenerator(NamedFactory):
    syllable_providers = dict()
    GLUE = ""

    def __init__(self, providers=None):
        super().__init__(providers)
        self.syllable_generators = self.prepare_syllable_generators()

    def template(self):
        return ()

    def prepare_syllable_generators(self):
        return {
            syllable_id: SyllableGenerator(syllable_provider)
            for syllable_id, syllable_provider in self.syllable_providers.items()
        }

    def name_rules(self):
        return dict()

    def rules(self, syllables):
        for syllable_id in syllables.keys():
            rule = self.name_rules().get(syllable_id)
            if rule is None:
                continue
            while not rule(syllables[syllable_id], syllables):
                syllables[syllable_id] = next(self.syllable_generators[syllable_id])
        return syllables

    def syllables(self):
        return self.rules({
            syllable_id: next(syllable)
            for syllable_id, syllable in self.syllable_generators.items()
        })

    @classmethod
    def join_syllables(cls, syllables, *args):
        return cls.GLUE.join(syllables)

    @classmethod
    def from_syllables(cls, syllables, order):
        return cls.GLUE.join([
            str(syllables[syllable_id]) for syllable_id in order
        ])

    def name(self, **kwargs):
        return self.from_syllables(self.syllables(), self.template())
