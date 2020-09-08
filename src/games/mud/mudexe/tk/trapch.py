from .tkGlobals import TkGlobals
from .loseme import loseme
from gamelib.mudexe.temp.used.aber_blib import getstr
from gamelib.mudexe.temp.used.aber_bprintf import bprintf
from gamelib.mudexe.temp.used.aber_gamego import crapup
from gamelib.mudexe.temp.used.aber_mobile import onlook
from gamelib.mudexe.temp.used.aber_new1 import ail_blind
from gamelib.mudexe.temp.used.aber_newuaf1 import my_lev
from gamelib.mudexe.temp.used.aber_objsys import lisobs, lispeople
from gamelib.mudexe.temp.used.aber_parse import openroom
from gamelib.mudexe.temp.used.aber_weather import isdark, showname
from gamelib.mudexe.temp.used.aber_zones import lodex
from gamelib.mudexe.temp.database import World


def lookin(room):
    def xx1():
        xxx = 0

        lodex(un1)
        if isdark():
            un1.close()
            bprintf("It is dark\n")
            World.open()
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
    World.close()

    if ail_blind:
        bprintf("You are blind... you can't see a item!\n")

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


def __ndie(user, chan):
    World.open()
    user.person.location = chan
    lookin(chan)


def trapch(chan):
    user = TkGlobals.get_user()
    if user.level > 9:
        return __ndie(user, chan)
    return __ndie(user, chan)
