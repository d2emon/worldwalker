from ..errors import CommandError


class BasePlayerData:
    SEX_NONE = None
    SEX_MALE = 0
    SEX_FEMALE = 1

    def __str__(self):
        return self.name

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def score(self):
        raise NotImplementedError()

    @property
    def strength(self):
        raise NotImplementedError()

    @property
    def sex(self):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()


class BasePlayer(BasePlayerData):
    # Player data
    @property
    def name(self):
        raise NotImplementedError()

    @property
    def score(self):
        raise NotImplementedError()

    @property
    def location(self):
        raise NotImplementedError()

    @property
    def message_id(self):
        raise NotImplementedError()

    # 6

    @property
    def strength(self):
        raise NotImplementedError()

    @property
    def visible(self):
        raise NotImplementedError()

    # Flags
    @property
    def sex(self):
        # 0 sex
        raise NotImplementedError()

    @property
    def can_be_exorcised(self):
        # 1 May not be exorcised ok
        return True

    @property
    def can_set_flags(self):
        # 2 May change pflags ok
        return False

    @property
    def can_edit(self):
        # 3 May use rmedit ok
        return False

    @property
    def can_debug(self):
        # 4 May use debugmode ok
        return False

    @property
    def can_patch(self):
        # 5 May use patch
        return False

    @property
    def can_be_snooped(self):
        # 6 May be snooped upon
        return True

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

    # Other
    @property
    def can_modify_messages(self):
        return False

    @property
    def exists(self):
        raise NotImplementedError()

    @property
    def is_dead(self):
        raise NotImplementedError()

    @property
    def is_god(self):
        raise NotImplementedError()

    @property
    def is_mobile(self):
        raise NotImplementedError()

    @property
    def is_wizard(self):
        raise NotImplementedError()

    @property
    def max_items(self):
        raise NotImplementedError()

    @property
    def items(self):
        raise NotImplementedError()

    @property
    def value(self):
        raise NotImplementedError()

    @property
    def level_name(self):
        raise NotImplementedError()

    @property
    def overweight(self):
        if self.max_items is None:
            return False
        return len(self.items) >= self.max_items

    # Equals
    def equal(self, player):
        raise NotImplementedError()

    # ObjSys
    def check_kicked(self):
        raise NotImplementedError()

    def die(self):
        raise NotImplementedError()

    def dump_items(self):
        raise NotImplementedError()

    def get_damage(self, enemy, damage):
        raise NotImplementedError()

    def get_lightning(self, enemy):
        raise NotImplementedError()

    def is_helping(self, player):
        raise NotImplementedError()

    def look(self):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()

    def woundmn(self, *args):
        raise NotImplementedError()

    def exorcised(self):
        if not self.can_be_exorcised:
            raise CommandError("You can't exorcise them, they dont want to be exorcised\n")
        self.dump_items()
        self.remove()

    def timeouted(self):
        self.dump_items()
        self.remove()
