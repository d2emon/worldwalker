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


class Item:
    @property
    def can_wear(self):
        return self.tstbit(8)
