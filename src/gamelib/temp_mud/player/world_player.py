from ..item import find_items
from ..location import Location
from ..services.players import PlayersService
from .base_player import BasePlayer


class WorldPlayer(BasePlayer):
    LEVELS = {
        1: ["The Novice"],
        2: ["The Adventurer", "The Adventuress"],
        3: ["The Hero", "The Heroine"],
        4: ["The Champion"],
        5: ["The Conjurer", "The Conjuress"],
        6: ["The Magician"],
        7: ["The Enchanter", "The Enchantress"],
        8: ["The Sorceror", "The Sorceress"],
        9: ["The Warlock"],
        10: ["The Apprentice Wizard", "The Apprentice Witch"],
        11: ["The 370"],
        12: ["The Hilbert-Space"],
        # 13:
        14: ["The Completely Normal Naughty Spud"],
        15: ["The Wimbledon Weirdo"],
        16: ["The DangerMouse"],
        17: ["The Charred Wizard", "The Charred Witch"],
        18: ["The Cuddly Toy"],
        19: ["Of The Opera"],
        20: ["The 50Hz E.R.C.S"],
        21: ["who couldn't decide what to call himself"],
        22: ["The Summoner"],

        10000: ["The 159 IQ Mega-Creator"],
        10001: ["The Arch-Wizard", "The Arch-Witch"],
        10002: ["The Wet Kipper"],
        10003: ["The Thingummy"],
        10033: ["The Arch-Wizard", "The Arch-Witch"],
        68000: ["The Wanderer"],

        -2: ["\010"],
        -10: ["The Heavy-Fan Dwarf"],
        -11: ["The Broke Dwarf"],
        -12: ["The Radioactive Dwarf"],
        -13: ["The Upper Class Dwarven Smith"],
        -14: ["The Singing Dwarf"],
        -30: ["The Sorceror"],
        -31: ["the Acolyte"],
    }

    def __init__(self, player_id):
        self.__player_id = player_id

    @property
    def player_id(self):
        return self.__player_id

    @property
    def __data(self):
        return PlayersService.get_info(player_id=self.player_id)

    @classmethod
    def __get(cls, player_id):
        return WorldPlayer(player_id)

    def reload(self):
        pass

    @property
    def name(self):
        return self.__data[0]

    @name.setter
    def name(self, value):
        self.__data[0] = value

    @property
    def score(self):
        return None

    @property
    def location(self):
        return Location(self.__data[4])

    @location.setter
    def location(self, value):
        self.__data[4] = value.location_id
        self.look()

    @property
    def message_id(self):
        return self.__data[5]

    @message_id.setter
    def message_id(self, value):
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

    @property
    def level(self):
        return self.__data[10]

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

    # Flags
    @property
    def sex(self):
        return self.SEX_FEMALE if self.__test_bit(0) else self.SEX_MALE

    @sex.setter
    def sex(self, value):
        if value == self.SEX_MALE:
            self.__clear_bit(0)
        elif value == self.SEX_FEMALE:
            self.__set_bit(0)

    @property
    def can_be_exorcised(self):
        return not self.__test_bit(1)

    @property
    def can_set_flags(self):
        return self.__test_bit(2)

    @property
    def can_edit(self):
        return self.__test_bit(3)

    @property
    def can_debug(self):
        return self.__test_bit(4)

    @property
    def can_patch(self):
        return self.__test_bit(5)

    @property
    def can_be_snooped(self):
        return not self.__test_bit(6)

    # Other
    @property
    def can_modify_messages(self):
        return self.is_god or self.name == "Lorry"

    @property
    def exists(self):
        return not self.name

    @property
    def is_dead(self):
        return self.strength < 0

    @property
    def is_faded(self):
        return self.message_id < 0

    @property
    def is_in_start(self):
        return self.message_id == -1

    @property
    def is_god(self):
        return self.level > 9999

    @property
    def is_mobile(self):
        return self.player_id >= 16

    @property
    def is_wizard(self):
        return self.level > 9

    @property
    def max_items(self):
        if not self.is_wizard:
            return None
        if self.level < 0:
            return None
        return self.level + 5

    @property
    def items(self):
        return find_items(
            owner=self,
            destroyed=False,
        )

    @property
    def value(self):
        if self.is_mobile:
            return 10 * self.damage
        return self.level * self.level * 100

    # ObjSys
    @property
    def level_name(self):
        if self.level == 19 and self.has_farted:
            return "Raspberry Blower Of Old London Town"

        level_names = self.LEVELS.get(self.level, ["The Cardboard Box"])
        if len(level_names) > 1:
            return level_names[self.sex]
        return level_names[0]

    # Utils
    # Flag utils
    # Support
    def __set_bit(self, bit_id):
        self.__data[9][bit_id] = True

    def __clear_bit(self, bit_id):
        self.__data[9][bit_id] = False

    def __test_bit(self, bit_id):
        return self.__data[9][bit_id]

    # Equals
    def equal(self, player):
        return player is not None and self.player_id == player.player_id

    # Other
    def check_kicked(self):
        pass

    def die(self):
        self.strength = -1

    def dump_items(self):
        for item in self.items:
            item.location = self.location

    def fade(self):
        self.message_id = -2

    def get_damage(self, enemy, damage):
        raise NotImplementedError()

    def get_lightning(self, enemy):
        if not self.is_mobile:
            return
        self.get_damage(enemy, 10000)
        # DIE

    def is_helping(self, player):
        return self.location == player.location and self.helping == player.player_id

    def is_timed_out(self, current_position):
        return self.exists and not self.is_faded and self.position < current_position / 2

    def look(self):
        pass

    def remove(self):
        self.name = ""

    def reset_position(self):
        self.message_id = -1

    def start(self):
        # self.strength = strength
        # self.level = level
        # self.visible = visible
        self.weapon = None
        # self.flags = sex
        self.helping = None

    def woundmn(self, *args):
        pass

    # Parse
    def level_of(self, score):
        score = score / 2  # Scaling factor
        if self.level > 10:
            return self.level
        elif score < 500:
            return 1
        elif score < 1000:
            return 2
        elif score < 3000:
            return 3
        elif score < 6000:
            return 4
        elif score < 10000:
            return 5
        elif score < 20000:
            return 6
        elif score < 32000:
            return 7
        elif score < 44000:
            return 8
        elif score < 70000:
            return 9
        else:
            return 10
