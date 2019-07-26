# from ..item import find_items
# from ..location import Location
from ..database import LocationData, ItemsData
from ..services.players import PlayersService
from .base_player import BasePlayer


class Level:
    SCORES = (
        0,
        500,
        1000,
        3000,
        6000,

        10000,
        20000,
        32000,
        44000,
        70000,
    )
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

    def __init__(self, player, level=None):
        self.player = player
        self.level = level if level is not None else player.level

    @property
    def name(self):
        if self.player.level == 19 and self.player.has_farted:
            return "Raspberry Blower Of Old London Town"

        level_names = self.LEVELS.get(self.level, ["The Cardboard Box"])
        if len(level_names) > 1:
            return level_names[self.player.sex]
        return level_names[0]

    # Parse
    @classmethod
    def by_score(cls, player, score=None):
        if score is None:
            score = player.score
        score = score / 2  # Scaling factor
        if player.level > 10:
            return cls(player)

        level = next((level for (level, max_score) in enumerate(cls.LEVELS) if max_score > score), 10)
        return cls(player, level)


class WorldPlayer(BasePlayer):
    def __init__(self, player_id):
        self.__player_id = player_id
        self.__data = self.reload()

        # Unknown
        self.damage = 0
        self.has_farted = False

    @property
    def player_id(self):
        return self.__player_id

    @classmethod
    def __get(cls, player_id):
        return WorldPlayer(player_id)

    def reload(self):
        if self.player_id is None:
            return [None] * 16

        return list(PlayersService.get_info(player_id=self.player_id))

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
        self.__data[4] = value.location_id
        self.look()

    @property
    def location(self):
        return LocationData().filter(location_id=self.location_id).first

    @property
    def message_id(self):
        return self.__data[5] or -1

    @message_id.setter
    def message_id(self, value):
        self.__data[5] = value

    @property
    def strength(self):
        return self.__data[7] or 0

    @strength.setter
    def strength(self, value):
        self.__data[7] = value

    @property
    def visible(self):
        return self.__data[8]

    @property
    def level(self):
        return self.__data[10] or 0

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
    def is_god(self):
        return self.level > 9999

    @property
    def is_mobile(self):
        return self.player_id >= 16

    @property
    def is_wizard(self):
        return self.level > 9

    @property
    def items(self):
        return ItemsData().filter(owner=self)

    @property
    def level_name(self):
        # ObjSys
        return Level(self, self.level).name

    @property
    def max_items(self):
        if not self.is_wizard:
            return None
        if self.level < 0:
            return None
        return self.level + 5

    @property
    def score(self):
        raise NotImplementedError()

    @property
    def value(self):
        if self.is_mobile:
            return 10 * self.damage
        return self.level * self.level * 100

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
        raise NotImplementedError()

    def die(self):
        self.strength = -1

    def dump_items(self):
        for item in self.items.items:
            item.location = self.location

    def get_damage(self, enemy, damage):
        raise NotImplementedError()

    def get_lightning(self, enemy):
        if not self.is_mobile:
            return
        self.get_damage(enemy, 10000)
        # DIE

    def is_helping(self, player):
        return self.location == player.location and self.helping == player.player_id

    def look(self):
        raise NotImplementedError()

    def remove(self):
        self.name = ""

    def start(self):
        # self.strength = strength
        # self.level = level
        # self.visible = visible
        self.weapon = None
        # self.flags = sex
        self.helping = None

    def woundmn(self, *args):
        raise NotImplementedError()
