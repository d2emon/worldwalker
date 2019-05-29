from ..objsys import ObjSys, iscarrby


class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def location(self):
        raise NotImplementedError()

    @location.setter
    def location(self, value):
        raise NotImplementedError()

    @property
    def strength(self):
        raise NotImplementedError()

    @strength.setter
    def strength(self, value):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @name.setter
    def name(self, value):
        raise NotImplementedError()

    @property
    def tothlp(self):
        raise NotImplementedError()

    @property
    def damage(self):
        if self.player_id in (18, 19, 20, 21, 22):
            return 6
        elif self.player_id == 23:
            return 32
        elif self.player_id == 24:
            return 8
        elif self.player_id == 28:
            return 6
        elif self.player_id == 30:
            return 20
        elif self.player_id == 31:
            return 14
        elif self.player_id == 32:
            return 15
        elif self.player_id == 33:
            return 10
        else:
            return 10

    @classmethod
    def fpbns(cls, name):
        raise NotImplementedError()

    @classmethod
    def fpbn(cls, name):
        raise NotImplementedError()


class Item:
    def __init__(self, item_id):
        self.item_id = item_id

    @property
    def state(self):
        return ObjSys.objinfo[4 * self.item_id + 1]

    @state.setter
    def state(self, value):
        ObjSys.objinfo[4 * self.item_id + 1] = value
        if self.tstbit(1):
            ObjSys.objinfo[4 * (self.item_id ^ 1) + 1] = value

    @property
    def carry_flag(self):
        # return ObjSys.objinfo[4 * self.item_id + 1]
        raise NotImplementedError()

    @carry_flag.setter
    def carry_flag(self, value):
        ObjSys.objinfo[4 * self.item_id + 3] = value

    @property
    def loc(self):
        raise NotImplementedError()

    @property
    def can_wear(self):
        return self.tstbit(8)

    def destroy(self):
        self.setbit(0)

    def is_worn_by(self, player):
        if not iscarrby(self.item_id, player):
            return False
        if self.carry_flag != 2:
            return False
        return True

    def tstbit(self, *args):
        raise NotImplementedError()

    def setbit(self, *args):
        raise NotImplementedError()

    def clearbit(self, *args):
        raise NotImplementedError()

    def setbyte(self, *args):
        raise NotImplementedError()

    def setoloc(self, *args):
        raise NotImplementedError()

    @classmethod
    def fobna(cls, name):
        raise NotImplementedError()


def ohany(*args):
    raise NotImplementedError()


def syslog(*args):
    raise NotImplementedError()
