from ..errors import CommandError


class BasePlayer:
    SEX_MALE = 0
    SEX_FEMALE = 1

    def __str__(self):
        return self.name

    # Player data
    @property
    def name(self):
        raise NotImplementedError()

    @name.setter
    def name(self, value):
        raise NotImplementedError()

    @property
    def location(self):
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

    # @property
    # def flags(self):
    #     raise NotImplementedError()

    # @flags.setter
    # def flags(self, value):
    #     raise NotImplementedError()

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
    # 0
    @property
    def sex(self):
        raise NotImplementedError()

    @sex.setter
    def sex(self, value):
        raise NotImplementedError()

    # 1
    @property
    def can_be_exorcised(self):
        return True

    # 2
    @property
    def can_set_flags(self):
        return False

    # 3
    @property
    def can_edit(self):
        return False

    # 4
    @property
    def can_debug(self):
        return False

    # 5
    @property
    def can_patch(self):
        return False

    # 6
    @property
    def can_be_snooped(self):
        return True

    # Other
    @property
    def capacity(self):
        if not self.is_wizard:
            return None
        if self.level < 0:
            return None
        return self.level + 5

    @property
    def is_dead(self):
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

    @property
    def items(self):
        return [item for item in ITEMS if item.is_carried_by(self)]

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

    # ObjSys
    @property
    def level_name(self):
        levels = {
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
        if self.level == 19 and self.has_farted:
            return "Raspberry Blower Of Old London Town"

        level_name = levels.get(self.level, ["The Cardboard Box"])
        if len(level_name) > 1:
            return level_name[self.sex]
        return level_name[0]

    def check_kicked(self):
        raise NotImplementedError()

    def die(self):
        self.strength = -1

    def dump_items(self):
        map(lambda item: item.set_location(self.location, 0), self.items)

    def exorcised(self):
        if not self.can_be_exorcised:
            raise CommandError("You can't exorcise them, they dont want to be exorcised\n")
        self.dump_items()
        self.remove()

    def fade(self):
        self.position = -2

    def get_lightning(self):
        if not self.is_mobile:
            return
        self.woundmn(10000)
        # DIE

    def is_helping(self, player):
        return self.location == player.location and self.helping == player.player_id

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
        self.dump_items()
        self.remove()

    def woundmn(self, *args):
        raise NotImplementedError()
