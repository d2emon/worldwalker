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

    @property
    def flags(self):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()

    @property
    def weapon(self):
        raise NotImplementedError()

    # 12

    @property
    def helping(self):
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
    def dead(self):
        return self.strength < 0

    @property
    def exists(self):
        return not self.name

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

    def dumpstuff(self, location):
        raise NotImplementedError()

    def fade(self):
        self.position = -2

    def is_helping(self, player):
        return self.location_id == player.location_id and self.helping == player.player_id

    def is_timed_out(self, current_position):
        return self.exists and not self.is_faded and self.position < current_position / 2

    def remove(self):
        self.name = ""

    def reset_position(self):
        self.position = -1

    def timeout_death(self):
        self.dumpstuff(self.location_id)
        self.remove()
