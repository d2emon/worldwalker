class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def name(self):
        raise NotImplementedError()

    @name.setter
    def name(self, value):
        raise NotImplementedError()

    @property
    def position(self):
        raise NotImplementedError()

    @position.setter
    def position(self, value):
        raise NotImplementedError()

    @property
    def location(self):
        raise NotImplementedError()

    @location.setter
    def location(self, value):
        raise NotImplementedError()

    @property
    def strength(self):
        raise NotImplementedError()

    @strength.setter
    def strength(self, value):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()

    @level.setter
    def level(self, value):
        raise NotImplementedError()

    @property
    def visible(self):
        raise NotImplementedError()

    @visible.setter
    def visible(self, value):
        raise NotImplementedError()

    @property
    def weapon(self):
        raise NotImplementedError()

    @weapon.setter
    def weapon(self, value):
        raise NotImplementedError()

    @property
    def sex(self):
        raise NotImplementedError()

    @sex.setter
    def sex(self, value):
        raise NotImplementedError()

    @property
    def sex_all(self):
        raise NotImplementedError()

    @sex_all.setter
    def sex_all(self, value):
        raise NotImplementedError()

    @property
    def helping(self):
        raise NotImplementedError()

    @helping.setter
    def helping(self, value):
        raise NotImplementedError()

    @property
    def is_alive(self):
        return bool(self.name)

    @property
    def is_mobile(self):
        return self.player_id >= 16

    @classmethod
    def fpbn(cls, player_name, not_found_error=None):
        raise NotImplementedError()

    def put_on(self, name, location, position):
        self.name = name
        self.location = location
        self.position = position
        self.level = 1
        self.visible = 0
        self.strength = -1
        self.weapon = None
        self.sex = 0

    def start(self, strength, level, visible, sex):
        self.strength = strength
        self.level = level
        self.visible = visible
        self.weapon = None
        self.sex_all = sex
        self.helping = None

    def remove(self):
        self.name = ""