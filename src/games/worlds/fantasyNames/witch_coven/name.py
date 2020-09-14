from genelib.fng import genders
from genelib.fng.name import Name


class WitchCovenName(Name):
    def __init__(self, name='', gender=genders.NEUTRAL, name_type=None, **kwargs):
        super().__init__(name=name, gender=gender, **kwargs)
        self.name_type = name_type

    @property
    def name(self):
        if self.name_type == 1:
            return f"The {self.values('nm1')} {self.values('nm3')}"
        elif self.name_type == 2:
            return f"{self.values('nm3')} of {self.values('nm2')}"
        else:
            return ''
