from .world import World


class Player:
    FLAG_SEX = 0
    # May not be exorcised
    FLAG_CAN_CHANGE_FLAGS = 2
    # 3 May use rmedit
    # 4 May use debugmode
    # 5 May use patch
    # 6 May be snooped upon

    SEX_MALE = 0
    SEX_FEMALE = 1

    def __init__(self, player_id):
        self.player_id = player_id

    def __str__(self):
        return self.name

    @classmethod
    def players(cls):
        return (Player(player_id) for player_id in range(World.player_ids))

    @property
    def __data(self):
        return World.ublock[self.player_id]

    # Support
    @property
    def name(self):
        return self.__data[0]

    @name.setter
    def name(self, value):
        self.__data[0] = value

    @property
    def location(self):
        return self.__data[4]

    @location.setter
    def location(self, value):
        self.__data[4] = value

    @property
    def position(self):
        return self.__data[5]

    @position.setter
    def position(self, value):
        self.__data[5] = value

    @property
    def strength(self):
        return self.__data[7]

    @strength.setter
    def strength(self, value):
        self.__data[7] = value

    @property
    def visible(self):
        return self.__data[8]

    @visible.setter
    def visible(self, value):
        self.__data[8] = value

    @property
    def flags(self):
        return self.__data[9]

    @flags.setter
    def flags(self, value):
        self.__data[9] = value

    @property
    def sex(self):
        return self.__data[9][self.FLAG_SEX]

    @sex.setter
    def sex(self, value):
        self.__data[9][self.FLAG_SEX] = value

    @property
    def level(self):
        return self.__data[10]

    @level.setter
    def level(self, value):
        self.__data[10] = value

    @property
    def weapon(self):
        return self.__data[11]

    @weapon.setter
    def weapon(self, value):
        self.__data[11] = value

    @property
    def helping(self):
        return self.__data[13]

    @helping.setter
    def helping(self, value):
        self.__data[13] = value

    # Unknown
    @property
    def exists(self):
        return not self.name

    @property
    def is_dead(self):
        return self.strength < 0

    @property
    def is_faded(self):
        return self.position < 0

    @property
    def is_mobile(self):
        return self.player_id >= 16

    # Support
    @property
    def helper(self):
        return next(self.helpers, None)

    @property
    def helpers(self):
        return (player for player in self.players() if player.__is_helping(self))

    # Unknown
    @classmethod
    def fpbn(cls, player_name, not_found_error=None):
        raise NotImplementedError()

    def die(self):
        self.strength = -1

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
        self.flags = sex
        self.helping = None

    def remove(self):
        self.name = ""

    # Support
    def __is_helping(self, player):
        return self.location == player.location and self.helping == player.player_id

    # Unknown
    def is_timed_out(self, current_position):
        return not self.is_dead and self.position != 2 and self.position < current_position / 2

    # Support
    def set_flag(self, flag_id):
        """
        Pflags

        0 sex
        1 May not be exorcised ok
        2 May change pflags ok
        3 May use rmedit ok
        4 May use debugmode ok
        5 May use patch
        6 May be snooped upon

        :param flag_id:
        :return:
        """
        self.__data[9][flag_id] = True

    def clear_flag(self, flag_id):
        self.__data[9][flag_id] = False

    def test_flag(self, flag_id):
        if flag_id == self.FLAG_CAN_CHANGE_FLAGS and self.name == "Debugger":
            return True
        return self.flags[flag_id]

    # Unknown
    def timeout_death(self):
        self.dumpstuff(self.location)
        self.remove()

    def dumpstuff(self, location):
        raise NotImplementedError()

    @classmethod
    def get_timed_out(cls, timeout):
        return (player for player in cls.players()[:16] if player.is_timed_out(timeout))
