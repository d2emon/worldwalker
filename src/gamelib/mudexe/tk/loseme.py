from .dummies import DummyGlobals, sig_aloff, dumpitems, sendsys, saveme, chksnp
from .tkGlobals import TkGlobals
from ..aber_support import pname, pvis


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
