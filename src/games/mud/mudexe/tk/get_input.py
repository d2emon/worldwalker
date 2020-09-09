from gamelib.mudexe.temp.used.aber_blood import BloodGlobals
from gamelib.mudexe.temp.used.aber_gamego import sig_alon, sig_aloff
from gamelib.mudexe.temp.used.aber_parse import gamecom
from gamelib.mudexe.temp.used.bbc import BBC


class Program:
    program_id = 0
    name = None

    @classmethod
    def update_name(cls, user):
        if user.person.vis > 9999:
            cls.name = "-csh"
        elif user.person.vis == 0:
            cls.name = "   --}}----- ABERMUD -----{{--     Playing as {}".format(user)
        print("PROGRAM:", cls.name)

    @classmethod
    def set_name(cls, name):
        cls.name = name


def __test_fight():
    if BloodGlobals.fighting is not None:
        if not pname(BloodGlobals.fighting):
            BloodGlobals.in_fight = 0
            BloodGlobals.fighting = None

        if ploc(BloodGlobals.fighting) != user.location_id:
            BloodGlobals.in_fight = 0
            BloodGlobals.fighting = None

    if BloodGlobals.in_fight:
        BloodGlobals.in_fight -= 1


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


def get_input(user):
    # Clearing buffer
    user.io.show_output()

    # Enter command block
    BBC.bottom_screen()

    user.io.show_output()
    Program.update_name(user)

    sig_alon()
    work = user.io.get_input(user.prompt, 80)
    sig_aloff()

    user.io.send_raw("\001l{}\n\001".format(work))

    # New screen
    BBC.top_screen()

    user.rte(save=True)

    if user.input_mode and work == "**":
        user.input_mode = 0
        sendmsg(user)

    work = __prepare_work(work, user.input_mode)
    if user.mode == 1:
        gamecom(work)
    elif work and work != ".Q" and work != ".q":
        user.special(work)

    __test_fight()

    return work == ".Q" or work == ".q"