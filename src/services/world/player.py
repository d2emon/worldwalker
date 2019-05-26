from . import WorldService


class Player:
    PLAYERS_COUNT = 48

    GENDER_IT = 0
    GENDER_HE = 1
    GENDER_SHE = 2

    players = []
    maxu = 16

    def __init__(self, player_id, name=None, channel=None):
        self.player_id = player_id

        self.name = name
        self.location = channel
        self.position = None
        self.level = 1
        self.visible = 0
        self.strength = -1
        self.weapon = None
        self.sex = 0

        self.helping = None

    @property
    def __data(self):
        # 0  Name
        # 1
        # 2
        # 3
        # 4  Location
        # 5  Position
        # 6
        # 7  Strength
        # 8  Visible
        # 9  Flags
        # 10 Level
        # 11 Weapon
        # 12
        # 13 Helping
        # 14
        # 15
        return WorldService.get_player(self.player_id)

    # Properties
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
        return self.__data[4]

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
        """
        Pflags

        0 sex
        1 May not be exorcised ok
        2 May change pflags ok
        3 May use rmedit ok
        4 May use debugmode ok
        5 May use patch
        6 May be snooped upon

        :return:
        """
        return self.__data[9]

    @sex_all.setter
    def sex_all(self, value):
        self.__data[9] = value

    @property
    def sex(self):
        return self.__data[9][0]

    @sex.setter
    def sex(self, value):
        self.__data[9][0] = value

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
    def exists(self):
        return self.name is not None

    @property
    def gender(self):
        """

        :return:
        """
        riatha = self.fpbns('riatha')
        shazareth = self.fpbns('shazareth')
        if self.player_id > 15 and self not in [riatha, shazareth]:
            return self.GENDER_IT
        elif self.sex:
            return self.GENDER_SHE
        else:
            return self.GENDER_HE

    # Add and remove
    def add(self):
        self.players[self.player_id] = self

    def remove(self):
        self.name = None

    @classmethod
    def __find_empty(cls):
        for player_id, player in enumerate(cls.players):
            if not player.exists:
                return player_id
        raise OverflowError()

    @classmethod
    def put_on(cls, name, channel):
        player_id = cls.__find_empty()
        cls(player_id, name, channel).add()
        return player_id

    # Fill players
    @classmethod
    def fill(cls):
        cls.players = [cls(player_id) for player_id in range(cls.PLAYERS_COUNT)]

    # Objsys
    @classmethod
    def fpbns(cls, name):
        search = name.lower()
        for player in cls.players:
            if not player.exists:
                continue

            player_name = player.name.lower()
            if player_name == search:
                return player
            if player_name[:4] == "the " and player_name[4:] == search:
                return player
        return None

    @classmethod
    def fpbn(cls, name):
        player_id = cls.fpbns(name)
        # if new1.ail_blind:
        #     return None
        if player_id is None:
            return None
        # if player_id == Talker.player_id:
        #     return player_id
        # if not Talker.see_player(player_id):
        #     return None

        return player_id
