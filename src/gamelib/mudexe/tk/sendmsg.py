from .dummies import DummyGlobals, pbfr, pname, ploc, pvis, gamecom, btmscr, topscr, set_progname, sig_alon,\
    sig_aloff, key_input
from .tkGlobals import TkGlobals
from .rte import rte
from .special import special
from ..aber_opensys.world import World
from ..aber_newuaf1 import my_lev


def __test_fight():
    if DummyGlobals.fighting is not None:
        if not pname(DummyGlobals.fighting):
            DummyGlobals.in_fight = 0
            DummyGlobals.fighting = None

        if ploc(DummyGlobals.fighting) != TkGlobals.curch:
            DummyGlobals.in_fight = 0
            DummyGlobals.fighting = None

    if DummyGlobals.in_fight:
        DummyGlobals.in_fight -= 1


def __get_prompt():
    prompt = "\r"

    if pvis(TkGlobals.mynum):
        prompt += "("

    if DummyGlobals.debug_mode:
        prompt += "#"

    if my_lev > 9:
        prompt += "----"

    if TkGlobals.convflg == 0:
        prompt += ">"
    elif TkGlobals.convflg == 1:
        prompt += "\""
    elif TkGlobals.convflg == 2:
        prompt += "*"
    else:
        prompt += "?"

    if pvis(TkGlobals.mynum):
        prompt += ")"

    return prompt


def __prepare_work(work, flag=0):
    if not work:
        return ""

    if work != "*" and work[0] == "*":
        return " " + work[1:]

    if not flag:
        return work

    if flag == 1:
        return "say {}".format(work)
    else:
        return "tss {}".format(work)


def sendmsg(user):
    pbfr()
    if DummyGlobals.tty == 4:
        btmscr()

    prompt = __get_prompt()
    pbfr()

    if pvis(TkGlobals.mynum) > 9999:
        set_progname(0, "-csh")
    elif pvis(TkGlobals.mynum) == 0:
        work = "   --}}----- ABERMUD -----{{--     Playing as {}".format(str(user))
        set_progname(0, work)

    sig_alon()
    key_input(prompt, 80)
    sig_aloff()
    work = DummyGlobals.key_buff

    if DummyGlobals.tty == 4:
        topscr()

    DummyGlobals.sysbuf += "\001l"
    DummyGlobals.sysbuf += work
    DummyGlobals.sysbuf += "\n\001"

    World.open()
    rte(user)
    World.close()

    if TkGlobals.convflg and work == "**":
        TkGlobals.convflg = 0
        sendmsg(user)

    work = __prepare_work(work, TkGlobals.convflg)

    if TkGlobals.curmode == 1:
        gamecom(work)
    elif work and work != ".Q" and work != ".q":
        special(work, user)

    __test_fight()

    return work == ".Q" or work == ".q"
