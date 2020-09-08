from .model import Model
from ..exceptions import WorldFullException


class Person(Model):
    items_count = 16
    items = None

    offset = 350
    length = items_count * 48

    @classmethod
    def model(cls):
        return {
            0: None,
            # 0: "None",
            4: None,
            5: None,
            7: None,
            8: None,
            9: [None] * 8,
            10: None,
            11: None,
            13: None,
        }

    @classmethod
    def find_empty_person(cls):
        for person_id in range(cls.items_count):
            if cls(person_id).is_empty:
                return person_id
        raise WorldFullException()

    @classmethod
    def fpbn(cls, username):
        return None

    def __init__(self, person_id):
        self.person_id = person_id

    def add_user(self, user):
        self.name = user.name
        self.loc = user.location_id
        self.pos = None
        self.level = 1
        self.vis = 0
        self.strength = None
        self.weapon = None
        self.sex = 0

    @property
    def data(self):
        return self.items[self.person_id]

    @property
    def name(self):
        return self.data[0]

    @property
    def is_empty(self):
        return not self.name

    @name.setter
    def name(self, value):
        self.data[0] = value

    @property
    def loc(self):
        return self.data[4]

    @loc.setter
    def loc(self, value):
        self.data[4] = value

    @property
    def chan(self):
        return self.loc

    @property
    def pos(self):
        return self.data[5]

    @pos.setter
    def pos(self, value):
        self.data[5] = value

    @property
    def strength(self):
        return self.data[7]

    @strength.setter
    def strength(self, value):
        self.data[7] = value

    @property
    def vis(self):
        return self.data[8]

    @vis.setter
    def vis(self, value):
        self.data[8] = value

    @property
    def sexall(self):
        return self.data[9]

    @sexall.setter
    def sexall(self, value):
        self.data[9] = value

    @property
    def sex(self):
        return self.data[9][0]

    @sex.setter
    def sex(self, value):
        self.data[9][0] = value

    @property
    def level(self):
        return self.data[10]

    @level.setter
    def level(self, value):
        self.data[10] = value

    @property
    def weapon(self):
        return self.data[11]

    @weapon.setter
    def weapon(self, value):
        self.data[11] = value

    @property
    def helping(self):
        return self.data[13]

    @helping.setter
    def helping(self, value):
        self.data[13] = value
