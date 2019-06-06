"""
Some more basic functions

Note

state(obj)
setstate(obj,val)
destroy(obj)

are elsewhere
"""
from ..errors import CommandError, CrapupError
from ..objsys import ObjSys, iscarrby


class Player:
    def __init__(self, player_id):
        self.player_id = player_id

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

    @classmethod
    def fobn(cls, name):
        raise NotImplementedError()

    @classmethod
    def fobna(cls, name):
        raise NotImplementedError()
