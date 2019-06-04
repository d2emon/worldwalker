class Player:
    __ublock = []
    __player_ids = len(__ublock)

    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def players(self):
        return (Player(player_id) for player_id in range(self.__player_ids))

    @property
    def __data(self):
        return self.__ublock[self.player_id]

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
    def channel(self):
        return self.location

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
    def sex_all(self):
        return self.__data[9]

    @sex_all.setter
    def sex_all(self, value):
        self.__data[9] = value

    @property
    def sex(self):
        return self.sex_all[0]

    @sex.setter
    def sex(self, value):
        self.sex_all[0] = value

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

    @property
    def is_alive(self):
        return bool(self.name)

    @property
    def is_mobile(self):
        return self.player_id >= 16

    @property
    def helper(self):
        return next((player for player in self.players if player.is_helping(self)), None)

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

    def is_helping(self, player):
        return self.location == player.location and self.helping == player.player_id

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
        self.sex_all[flag_id] = True

    def clear_flag(self, flag_id):
        self.sex_all[flag_id] = False

    def test_flag(self, flag_id):
        if flag_id == 2 and self.name == "Debugger":
            return True
        return self.sex_all[flag_id]
