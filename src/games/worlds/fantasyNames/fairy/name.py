from genelib.fng import genders
from genelib.fng.name import Name


class FairyName(Name):
    @property
    def first_name(self):
        if self.gender == genders.MALE:
            return self.values.get('names_male')
        elif self.gender == genders.FEMALE:
            return self.values.get('names_female')
        else:
            return ''

    @property
    def last_name(self):
        return f"{self.values.get('names_family')}{self.values.get('names_family_2')}"

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'
