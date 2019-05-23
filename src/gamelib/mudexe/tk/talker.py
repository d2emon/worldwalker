from .tkGlobals import TkGlobals
from gamelib.mudexe.temp.used.aber_gamego import crapup

from gamelib.mudexe.temp.exceptions import CrapupException, GameException
from gamelib.mudexe.temp.database import WorldFullException, NoDatabaseException
from .get_input import get_input


def __main_loop(user):
    user.io.show_output()
    get_input(user)
    if TkGlobals.rd_qd:
        user.rte(save=True)
    TkGlobals.rd_qd = 0  #
    user.io.show_output()


def talker(user):
    # TODO: Remove this
    TkGlobals.set_user(user)

    try:
        user.prepare()
    except NoDatabaseException:
        crapup("Sorry AberMUD is currently unavailable") #
    except CrapupException as message:
        crapup(message)  #
    except WorldFullException as message:
        print(message)
        return 0
    except GameException as message:
        print(message)

    while True:
        __main_loop(user)
