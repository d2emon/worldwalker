from ..errors import CrapupError, ServiceError
from ..services.users import UsersService
from .base_player import BasePlayerData


class UserData(BasePlayerData):
    def __init__(self):
        self.__name = ""
        self.__score = 0  # my_sco
        self.__strength = 40  # my_str
        self.__sex = None  # my_sex
        self.__level = None  # my_lev

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, value):
        self.__strength = value
        self.update()

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, value):
        self.__sex = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    # NewUaf
    def __serialize(self):
        return {
            'name': self.name,
            'score': self.score,
            'strength': self.strength,
            'sex': self.sex,
            'level': self.level,
        }

    def __deserialize(self, **kwargs):
        self.score = kwargs.get('score', 0)
        self.strength = kwargs.get('strength', 40)
        self.sex = kwargs.get('sex', None)
        self.level = kwargs.get('level', 1)

    def create(self, **data):
        self.__deserialize(**data)
        self.save()

    def delete(self):
        UsersService.delete(name=self.name)

    def load(self):
        try:
            data = UsersService.get(name=self.name)
        except ServiceError:
            raise CrapupError("Panic: Timeout event on user file\n")

        if data is None:
            return None

        self.__deserialize(**data)
        return self

    def save(self):
        UsersService.post(**self.__serialize())

    def update(self):
        raise NotImplementedError()