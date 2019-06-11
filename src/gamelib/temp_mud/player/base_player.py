class BasePlayer:
    SEX_MALE = 0
    SEX_FEMALE = 1

    def __str__(self):
        return self.name

    @property
    def name(self):
        raise NotImplementedError()

    @name.setter
    def name(self, value):
        raise NotImplementedError()

    @property
    def location_id(self):
        raise NotImplementedError()

    @property
    def position(self):
        raise NotImplementedError()

    @position.setter
    def position(self, value):
        raise NotImplementedError()

    # 6

    @property
    def strength(self):
        raise NotImplementedError()

    @strength.setter
    def strength(self, value):
        raise NotImplementedError()

    @property
    def visible(self):
        raise NotImplementedError()

    @visible.setter
    def visible(self, value):
        raise NotImplementedError()

    @property
    def flags(self):
        raise NotImplementedError()

    @flags.setter
    def flags(self, value):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()

    @level.setter
    def level(self, value):
        raise NotImplementedError()

    @property
    def weapon(self):
        raise NotImplementedError()

    @weapon.setter
    def weapon(self, value):
        raise NotImplementedError()

    # 12

    @property
    def helping(self):
        raise NotImplementedError()

    @helping.setter
    def helping(self, value):
        raise NotImplementedError()

    # Flags
    @property
    def sex(self):
        raise NotImplementedError()

    @sex.setter
    def sex(self, value):
        raise NotImplementedError()

    # Other
    @property
    def capacity(self):
        if not self.is_wizard:
            return None
        if self.level < 0:
            return None
        return self.level + 5

    @property
    def dead(self):
        return self.strength < 0

    @property
    def exists(self):
        return not self.name

    @property
    def is_wizard(self):
        return self.level > 9

    @property
    def is_god(self):
        return self.level > 9999

    @property
    def is_faded(self):
        return self.position < 0

    @property
    def is_in_start(self):
        return self.position == -1

    @property
    def is_mobile(self):
        raise NotImplementedError()

    def die(self):
        self.strength = -1

    def dumpstuff(self, *args):
        raise NotImplementedError()

    def fade(self):
        self.position = -2

    def get_lightning(self):
        if not self.is_mobile:
            return
        self.woundmn(10000)
        # DIE

    def is_helping(self, player):
        return self.location_id == player.location_id and self.helping == player.player_id

    def is_timed_out(self, current_position):
        return self.exists and not self.is_faded and self.position < current_position / 2

    def remove(self):
        self.name = ""

    def reset_position(self):
        self.position = -1

    def start(self):
        # self.strength = strength
        # self.level = level
        # self.visible = visible
        self.weapon = None
        # self.flags = sex
        self.helping = None

    def timeout_death(self):
        self.dumpstuff(self.location_id)
        self.remove()

    def woundmn(self, *args):
        raise NotImplementedError()
