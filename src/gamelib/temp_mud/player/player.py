from ..world import World
from .base_player import BasePlayer


class Player(BasePlayer):
    __FLAG_SEX = 0
    # May not be exorcised
    __FLAG_CAN_CHANGE_FLAGS = 2
    # 3 May use rmedit
    # 4 May use debugmode
    # 5 May use patch
    # 6 May be snooped upon

    def __init__(self, player_id):
        self.player_id = player_id

    @classmethod
    def players(cls):
        return (Player(player_id) for player_id in range(World.player_ids))  # 49

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
    def location_id(self):
        return self.__data[4]

    @location_id.setter
    def location_id(self, value):
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
        return self.__test_flag(self.__FLAG_SEX)

    @sex.setter
    def sex(self, value):
        if value:
            self.__set_flag(self.__FLAG_SEX)
        else:
            self.__clear_flag(self.__FLAG_SEX)

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
    def is_mobile(self):
        return self.player_id >= 16

    @property
    def can_be_exorcised(self):
        return not self.__test_flag(1)

    @property
    def can_set_flags(self):
        return not self.__test_flag(2)

    @property
    def is_editor(self):
        return not self.__test_flag(3)

    @property
    def is_debugger(self):
        return not self.__test_flag(4)

    # Support
    @property
    def helper(self):
        return next(self.helpers, None)

    @property
    def helpers(self):
        return (player for player in self.players() if player.is_helping(self))

    # Unknown
    @classmethod
    def fpbn(cls, player_name, not_found_error=None):
        player = cls.fpbns(player_name)
        if player is None:
            return player
        if not seeplayer(player):
            return None
        return player

    @classmethod
    def fpbns(cls, player_name):
        n1 = player_name.lower()
        for player in cls.players():
            if player.is_dead:
                continue
            n2 = player.name.lower()
            if not player.is_dead and n2 == n1:
                return player
            if n2[:4] == "the " and n2[4:] == n1:
                return player
        return None

    # Support
    # Flags
    # 0 sex
    # 1 May not be exorcised ok
    # 2 May change pflags ok
    # 3 May use rmedit ok
    # 4 May use debugmode ok
    # 5 May use patch
    # 6 May be snooped upon
    def __set_flag(self, flag_id):
        self.__data[9][flag_id] = True

    def __clear_flag(self, flag_id):
        self.__data[9][flag_id] = False

    def __test_flag(self, flag_id):
        if flag_id == self.__FLAG_CAN_CHANGE_FLAGS and self.name == "Debugger":
            return True
        return self.flags[flag_id]

    # Unknown
    @classmethod
    def get_timed_out(cls, timeout):
        return (player for player in cls.players()[:16] if player.is_timed_out(timeout))

    # Tk
    @classmethod
    def new_player_id(cls):
        return next((player.player_id for player in cls.players() if not player.exists), None)

    # Unknown
    def dispuser(self, viewer):
        if self.is_dead:
            # On  Non game mode
            return
        if self.visible > viewer.level:
            return
        if self.visible:
            yield "("
        yield "{} ".format(self.name)
        yield self.level_name
        if self.visible:
            yield ")"
        if self.is_faded:
            yield " [Absent From Reality]"
        yield "\n"
