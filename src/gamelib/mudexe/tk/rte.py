from .dummies import DummyGlobals, SIZEOF__LONG, eorte, setppos
from ..aber_blib import sec_read
from ..aber_bprintf import bprintf
from ..aber_gamego import crapup
from ..aber_opensys.world import World
from .tkGlobals import TkGlobals
from .find import findend
from .sysctrl import sysctrl


def mstoout(block, user):
    x = str(block)
    # Print appropriate stuff from data block
    luser = str(user).lower()

    if DummyGlobals.debug_mode:
        bprintf("\n<{}>".format(block[1]))

    if block[1] < -3:
        sysctrl(block, luser)
    else:
        bprintf(x[2 * SIZEOF__LONG:])


def readmsg(channel, num):
    # channel, block, num
    buff = sec_read(channel, 0, 64)
    number = num * 2 - buff[0]
    return sec_read(channel, number, 128)


def update(user):
    xp = TkGlobals.cms - TkGlobals.lasup
    if xp < 0:
        xp = -xp

    if xp < 10:
        return

    unit = World.open()
    setppos(TkGlobals.mynum, TkGlobals.cms)
    TkGlobals.lasup = TkGlobals.cms


def rte(user):
    block = []

    unit = World.open()
    TkGlobals.fl_com = unit
    if unit is None:
        crapup("AberMUD: FILE_ACCESS : Access failed\n")

    if TkGlobals.cms is None:
        TkGlobals.cms = findend(unit)

    too = findend(unit)
    for ct in range(TkGlobals.cms, too):
        readmsg(unit, block, ct)
        mstoout(block, user)
    TkGlobals.cms = too

    update(user)
    eorte()

    DummyGlobals.rdes = 0
    DummyGlobals.tdes = 0
    DummyGlobals.vdes = 0
