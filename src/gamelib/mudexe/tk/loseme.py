from .dummies import DummyGlobals
from .tkGlobals import TkGlobals
from gamelib.mudexe.temp.used.aber_bprintf import chksnp
from gamelib.mudexe.temp.used.aber_gamego import sig_aloff
from gamelib.mudexe.temp.used.aber_newuaf1 import saveme
from gamelib.mudexe.temp.used.aber_objsys import dumpitems
from gamelib.mudexe.temp.used.aber_parse import sendsys
from gamelib.mudexe.temp.used.aber_support import pname, pvis


def loseme(user=None):
    sig_aloff()
    # No interruptions while you are busy dying
    # ABOUT 2 MINUTES OR SO
    TkGlobals.i_setup = 0

    unit = World.openworld()
    dumpitems()
    if pvis(TkGlobals.mynum) < 10000:
        bk = "{} has departed from AberMUDII\n".format(TkGlobals.globme)
        sendsys(TkGlobals.globme, TkGlobals.globme, -10113, 0, bk)

    pname(TkGlobals.mynum).clear()
    World.closeworld()

    if not DummyGlobals.zapped:
        saveme()
    chksnp()
