"""
AberMUD II

This game systems, its code scenario and design are (C) 1987/88  Alan Cox,Jim Finnis,Richard Acott

This file holds the basic communications routines
"""
from .dummies import DummyGlobals
from ..aber_blib import sec_read, sec_write, scan
from ..aber_gamego import crapup
from ..aber_objsys import fpbns, dumpstuff
from ..aber_support import syslog, pname, ppos, ploc
from ..aber_weather import longwthr

from ..database.world import World

from .tkGlobals import TkGlobals
from .filelock import fcloselock
from .loseme import loseme
from .rte import mstoout, rte
from .sendmsg import sendmsg
from .special import special
from .sysctrl import sysctrl
from .talker import talker
from .trapch import trapch, lookin


"""
Data format for mud packets

Sector 0
[64 words]
0   Current first message pointer
1   Control Word
Sectors 1-n  in pairs ie [128 words]

[channel][controlword][text data]

[controlword]
0 = Text
- 1 = general request
"""


def putmeon(user):
    return user.put_on()


def readmsg(message_id):
    return World.load_message(message_id)


def update(user):
    return user.update()


def findstart():
    return World.database.load_start


def findend():
    return World.database.load_end

# =======================================


def vcpy(dest, offd, source, offs, len__):
    # dest, offd, source, offs, len__
    for c in range(len__):
        dest[c + offd] = source[c + offs]
    return dest


def send2(block):
    unit = World.open()
    if unit is None:
        loseme()
        crapup("\nAberMUD: FILE_ACCESS : Access failed\n")

    inpbk = sec_read(unit, 0, 64)

    number = 2 * inpbk[1] - inpbk[0]
    inpbk[1] += 1

    sec_write(unit, block, number, 128)
    sec_write(unit, inpbk, 0, 64)

    if number >= 199:
        cleanup(inpbk)
    if number >= 199:
        longwthr()


def cleanup(inpbk):
    unit = World.open()

    for i in range(1, 100, 20):
        bk = sec_read(unit, i + 100, 1280)
        sec_write(unit, bk, i, 1280)

    inpbk[0] = inpbk[0] + 100
    sec_write(unit, inpbk, 0, 64)
    revise(inpbk)


def broad(mesg):
    TkGlobals.rd_qd = 1
    block = vcpy([0, -1], 2, mesg, 0, 126)
    send2(block)


def tbroad(message):
    broad(message)


def split(block, nam1, nam2, work, user):
    wkblock = vcpy([], 0, block, 2, 126)
    work = vcpy(work, 0, block, 64, 64)

    a = scan(nam1, wkblock, 0, "", ".")
    scan(nam2, wkblock, a + 1, "", ".")

    if nam1[:4] == "The " or nam1[:4] == "the ":
        if nam1[4:].lower() == str(user).lower():
            return 1

    return nam1.lower() == str(user).lower()


def revise(cutoff):
    unit = World.open()
    for ct in range(16):
        if not pname(ct) and ppos(ct) < cutoff / 2 and ppos(ct) != -2:
            mess = "{} has been timed out\n".format(pname(ct))
            broad(mess)
            dumpstuff(ct, ploc(ct))
            pname(ct).value = None


def loodrv():
    lookin(TkGlobals.curch)


def userwrap():
    if fpbns(TkGlobals.globme) is not None:
        loseme()
        syslog("System Wrapup exorcised {}".format(TkGlobals.globme))
