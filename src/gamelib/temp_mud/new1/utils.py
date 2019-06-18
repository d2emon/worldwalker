from ..errors import CommandError

from ..bprintf import bprintf
from ..magic import randperc
from ..newuaf import NewUaf
from ..opensys import openworld
from ..objsys import iscarrby
from ..parse.messages import Message
from ..support import Item, Player
from ..tk import Tk
from .messages import MSG_PRIVATE


def __victim_base(parser):
    word = parser.brkword()
    if word is None:
        raise CommandError("Who ?\n")
    openworld()
    if word == "at":
        return __victim_base(parser)  # STARE AT etc
    player = Player.fpbn(word)
    if player is None:
        raise CommandError("Who ?\n")
    return player


def __victim_magic(parser, reflectable=True):
    player = __victim_base(parser)
    if NewUaf.my_str < 10:
        raise CommandError("You are too weak to cast magic\n")
    if NewUaf.my_lev < 10:
        NewUaf.my_str -= 2

    i = 5
    if iscarrby(111, Tk.mynum):
        i += 1
    if iscarrby(121, Tk.mynum):
        i += 1
    if iscarrby(163, Tk.mynum):
        i += 1

    if NewUaf.my_lev < 10 and randperc() > i * NewUaf.my_lev:
        bprintf("You fumble the magic\n")
        if reflectable:
            bprintf("The spell reflects back\n")
            return Player(Tk.mynum)
        else:
            raise CommandError()
    else:
        if NewUaf.my_lev < 10:
            bprintf("The spell succeeds!!\n")
    return player


def __victim_no_reflect(parser):
    return __victim_magic(parser, False)


# This one isnt for magic
def victim_is_here(parser):
    victim = __victim_base(parser)
    if victim.location != Tk.curch:
        raise CommandError("They are not here\n")
    return victim


def victim_magic_is_here(parser):
    victim = __victim_no_reflect(parser)
    if victim.location != Tk.curch:
        raise CommandError("They are not here\n")
    return victim


def victim_magic(parser):
    return __victim_magic(parser, True)


def social(victim, message):
    if message[:4] == "star":
        bk = "\001s{name}\001{name} {message}\n\001".format(name=Tk.globme, message=message)
    else:
        bk = "\001p{name}\001 {message}\n\001".format(name=Tk.globme, message=message)
    Message(
        victim,
        Tk,
        MSG_PRIVATE,
        Tk.curch,
        bk,
    ).send()
