from .dummies import DummyGlobals, setploc
from .tkGlobals import TkGlobals
from .loseme import loseme
from ..aber_blib import getstr
from ..aber_bprintf import bprintf
from ..aber_gamego import crapup
from ..aber_mobile import onlook
from ..aber_new1 import ail_blind
from ..aber_newuaf1 import my_lev
from ..aber_objsys import lisobs, lispeople
from ..aber_opensys.world import World
from ..aber_parse import openroom
from ..aber_weather import isdark, showname
from ..aber_zones import lodex


def lookin(room):
    def xx1():
        xxx = 0

        lodex(un1)
        if isdark():
            un1.close()
            bprintf("It is dark\n")
            World.openworld()
            onlook()
            return True

        while True:
            s = getstr(un1, s)
            if not s:
                return False

            if s == "#DIE":
                if ail_blind:
                    un1.rewind()
                    ail_blind = 0
                    return xx1()
                if my_lev > 9:
                    bprintf("<DEATH ROOM>\n")
                else:
                    loseme(TkGlobals.globme)
                    crapup("bye bye.....\n")
            else:
                if s == "#NOBR":
                    brmode = 0
                elif not ail_blind and not xxx:
                    bprintf("{}\n".format(str))
                xxx = brmode

    # Lords ????
    World.closeworld()

    if ail_blind:
        bprintf("You are blind... you can't see a thing!\n")

    if my_lev > 9:
        showname(room)

    un1 = openroom(room, "r")
    if un1 is not None:
        if xx1():
            return
    else:
        bprintf("\nYou are on channel {}\n".format(room))
    un1.close()

    World.openworld()
    if not ail_blind:
        lisobs()
        if TkGlobals.curmode == 1:
            lispeople()
    bprintf("\n")
    onlook()


def __ndie(chan):
    World.openworld()
    setploc(TkGlobals.mynum, chan)
    lookin(chan)


def trapch(chan):
    if DummyGlobals.my_lev > 9:
        return __ndie(chan)
    return __ndie(chan)
