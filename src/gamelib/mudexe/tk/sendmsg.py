from .dummies import DummyGlobals
from .tkGlobals import TkGlobals
from ..bbc import BBC
from ..aber_bprintf import pbfr
from ..aber_gamego import sig_alon, sig_aloff, set_progname
from ..aber_key import key_input
from ..aber_parse import gamecom
from ..database.world import World


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

    user = TkGlobals.get_user()

    if DummyGlobals.debug_mode:
        prompt += "#"

    if user.level > 9:
        prompt += "----"

    if TkGlobals.convflg == 0:
        prompt += ">"
    elif TkGlobals.convflg == 1:
        prompt += "\""
    elif TkGlobals.convflg == 2:
        prompt += "*"
    else:
        prompt += "?"

    if user.person.vis:
        prompt = "({})".format(prompt)

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
    BBC.bottom_screen()

    prompt = __get_prompt()
    pbfr()

    user = TkGlobals.get_user()
    if user.person.vis > 9999:
        set_progname(0, "-csh")
    elif user.person.vis == 0:
        work = "   --}}----- ABERMUD -----{{--     Playing as {}".format(str(user))
        set_progname(0, work)

    sig_alon()
    key_input(prompt, 80)
    sig_aloff()
    work = DummyGlobals.key_buff

    BBC.top_screen()

    DummyGlobals.sysbuf += "\001l"
    DummyGlobals.sysbuf += work
    DummyGlobals.sysbuf += "\n\001"

    World.open()
    user.rte()
    World.close()

    if TkGlobals.convflg and work == "**":
        TkGlobals.convflg = 0
        sendmsg(user)

    work = __prepare_work(work, TkGlobals.convflg)

    if TkGlobals.curmode == 1:
        gamecom(work)
    elif work and work != ".Q" and work != ".q":
        user.special(work)

    __test_fight()

    return work == ".Q" or work == ".q"
