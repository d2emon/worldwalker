from ..errors import CrapupError

from ..bprintf import bprintf
from ..newuaf import NewUaf, delpers
from ..objsys import dumpitems
from ..opensys import closeworld, openworld
from ..parse import Parse
from ..parse.messages import Message
from ..support import syslog
from ..tk import Tk, loseme
from .disease import DISEASES


MSG_GLOBAL = -10000
MSG_WOUND = -10021
MSG_CURE = -10100
MSG_CRIPPLE = -10101
MSG_DUMB = -10102
MSG_FORCE = -10103
MSG_SHOUT = -10104
MSG_BLIND = -10105
MSG_BOLT = -10106
MSG_CHANGE = -10107
MSG_FIREBALL = -10109
MSG_SHOCK = -10110
MSG_PRIVATE = -10111
MSG_WIZARD = -10113
MSG_DEAF = -10120


def __iam(name):
    search = name.lower()
    my_name = Tk.globme.lower()
    if search == my_name:
        return True
    if my_name[:4] == "the " and search == my_name[4:]:
        return True
    return False


def __wounded(damage, message):
    bprintf(message)

    if NewUaf.my_lev > 9:
        return
    NewUaf.my_str -= damage
    Parse.me_cal = 1
    if NewUaf.my_str >= 0:
        return
    closeworld()

    syslog("{} slain magically".format(Tk.globme))
    delpers(Tk.globme)
    Parse.zapped = True

    openworld()
    dumpitems()
    loseme()
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        Tk.curch,
        "{} has just died\n".format(Tk.globme),
    ).send()
    Message(
        Tk,
        Tk,
        MSG_WIZARD,
        Tk.curch,
        "[ {} has just died ]\n".format(Tk.globme),
    ).send()
    raise CrapupError("Oh dear you just died\n")


def new1_receive(is_me, channel, to__, from__, code, text):
    if code == MSG_CURE:
        if is_me != 1:
            return
        bprintf("All your ailments have been cured\n")

        DISEASES.cure()
    elif code == MSG_CRIPPLE:
        if is_me != 1:
            return
        DISEASES.crippled.magic(from__)
    elif code == MSG_DUMB:
        if is_me != 1:
            return
        DISEASES.dumb.magic(from__)
    elif code == MSG_FORCE:
        if is_me != 1:
            return
        DISEASES.force.magic(from__, text)
    elif code == MSG_SHOUT:
        if is_me == 1:
            return
        bprintf("\001p{}\001 shouts '{}'\n".format(from__, text))
    elif code == MSG_BLIND:
        if is_me != 1:
            return
        DISEASES.blind.magic(from__)
    elif code == MSG_BOLT:
        if __iam(from__):
            return
        if Tk.curch != channel:
            return
        bprintf("Bolts of fire leap from the fingers of \001p{}\001\n".format(from__))
        if is_me == 1:
            __wounded(int(text), "You are struck!\n")
        else:
            bprintf("\001p{}\001 is struck\n".format(to__))
    elif code == MSG_CHANGE:
        if is_me != 1:
            return
        bprintf("Your sex has been magically changed!\n")
        NewUaf.my_sex = 1 - NewUaf.my_sex
        bprintf("You are now ")
        if NewUaf.my_sex:
            bprintf("Female\n")
        else:
            bprintf("Male\n")
        Parse.calibme()
    elif code == MSG_FIREBALL:
        if __iam(from__):
            return
        if Tk.curch != channel:
            return
        bprintf("\001p{}\001 casts a fireball\n".format(from__))
        if is_me == 1:
            __wounded(int(text), "You are struck!\n")
        else:
            bprintf("\001p{}\001 is struck\n".format(to__))
    elif code == MSG_SHOCK:
        if __iam(from__):
            return
        if is_me != 1:
            return
        __wounded(int(text), "\001p{}\001 touches you giving you a sudden electric shock!\n".format(from__))
    elif code == MSG_PRIVATE:
        if is_me != 1:
            return
        bprintf("{}\n".format(text))
    elif code == MSG_WIZARD:
        if NewUaf.my_lev > 9:
            bprintf(text)
    elif code == MSG_DEAF:
        if is_me != 1:
            return
        DISEASES.deaf.magic(from__)
