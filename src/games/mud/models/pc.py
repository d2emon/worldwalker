class PlayerCharacter:
    MALE = 0
    FEMALE = 1

    FLAG_SEX = 1

    def __init__(self, **kwargs):
        self.character_id = kwargs.get('character_id')

        self.__name = kwargs.get('name', '')
        # 1
        # 2
        # 3

        self.__channel_id = kwargs.get('channel_id', 0)
        self.__event_id = kwargs.get('event_id', 0)
        # 6
        self.__strength = kwargs.get('strength', 0)

        self.__visible = kwargs.get('visible', 0)
        self.__flags = kwargs.get('flags', {})
        self.__level = kwargs.get('level', 0)
        self.__weapon_id = kwargs.get('weapon_id', 0)

        # 12
        self.__helping_id = kwargs.get('helping_id', 0)
        # 14
        # 15

    # World props

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, value):
        self.__channel_id = value

    @property
    def event_id(self):
        return self.__event_id

    @event_id.setter
    def event_id(self, value):
        self.__event_id = value

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, value):
        self.__strength = value

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value

    @property
    def flags(self):
        return self.__flags

    @flags.setter
    def flags(self, value):
        self.__flags = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def weapon_id(self):
        return self.__weapon_id

    @weapon_id.setter
    def weapon_id(self, value):
        self.__weapon_id = value

    @property
    def helping_id(self):
        return self.__helping_id

    @helping_id.setter
    def helping_id(self, value):
        self.__helping_id = value

    # Flags

    @property
    def sex(self):
        return self.__flags[self.FLAG_SEX]

    @sex.setter
    def sex(self, value):
        self.__flags[self.FLAG_SEX] = value

    # Readonly props

    @property
    def exists(self):
        return len(self.__name)

    @property
    def is_dead(self):
        return self.__strength < 0

    @property
    def is_special(self):
        return self.__level < 0

    @property
    def is_moderator(self):
        return self.__level >= 10

    @property
    def is_admin(self):
        return self.__level > 9999

    @property
    def is_absent(self):
        return self.__event_id == 2

    @property
    def helpers(self):
        pcs = []
        return (pc for pc in pcs if (pc.channel_id == self.__channel_id) and (pc.helping_id == self.character_id))

    # Class methods

    @classmethod
    def load(cls, character_id):
        """
        Load character from db

        :param character_id:
        :return:
        """
        return cls(character_id=character_id)

    # Other methods

    def remove(self):
        self.__name = ''

    def kill(self):
        self.__strength = -1

    def visible_for(self, level):
        return self.__visible <= level
