from genelib.fng import genders
from genelib.fng.name import Name


class WitchName(Name):
    @property
    def first_name(self):
        if self.gender == genders.MALE:
            return self.values.get('nm3')
        elif self.gender == genders.FEMALE:
            return self.values.get('nm1')
        else:
            return ''

    @property
    def last_name(self):
        return self.values.get('nm2')

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
