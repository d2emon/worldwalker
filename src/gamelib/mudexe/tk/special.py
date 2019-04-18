from .dummies import DummyGlobals, initme, setpstr, setplev, setpvis, setpwpn, setpsexall, setphelping, cuserid,\
    sendsys, randperc
from .tkGlobals import TkGlobals
from .rte import rte
from .trapch import trapch
from ..aber_opensys.world import World


def __g(user):
    us = ""

    TkGlobals.curmode = 1
    TkGlobals.curch = -5
    initme()
    ufl = World.openworld()

    setpstr(TkGlobals.mynum, DummyGlobals.my_str)
    setplev(TkGlobals.mynum, DummyGlobals.my_lev)
    if DummyGlobals.my_lev < 10000:
        setpvis(TkGlobals.mynum, 0)
    else:
        setpvis(TkGlobals.mynum, 10000)
    setpwpn(TkGlobals.mynum, None)
    setpsexall(TkGlobals.mynum, DummyGlobals.my_sex)
    setphelping(TkGlobals.mynum, None)

    cuserid(us)
    xy = "\001s{name}\001{name}  has entered the game\n\001".format(name=str(user))
    xx = "\001s{name}\001[ {name}  has entered the game ]\n\001".format(name=str(user))
    sendsys(str(user), str(user), -10113, TkGlobals.curch, xx)

    rte(user)

    if randperc() > 50:
        trapch(-5)
    else:
        TkGlobals.curch = -183
        trapch(-183)
    sendsys(str(user), str(user), -10000, TkGlobals.curch, xy)


def special(code_string, user):
    bk = code_string.lower()
    if bk[0] != '.':
        return 0

    ch = bk[1]
    if ch == 'g':
        __g(user)
    else:
        print("\nUnknown . option\n")
    return 1
