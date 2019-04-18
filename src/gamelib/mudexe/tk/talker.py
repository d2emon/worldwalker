from .dummies import DummyGlobals
from .tkGlobals import TkGlobals
from .rte import rte
from .sendmsg import sendmsg
from .special import special
from ..aber_bprintf import makebfr, pbfr
from ..aber_gamego import crapup

from ..database.world import World
from ..exceptions import CrapupException
from ..database.exceptions import WorldFullException, NoDatabaseException


def __setup(user):
    makebfr()  #

    user.message_id = None
    user.put_on()

    World.open()
    rte(user)
    World.close()

    user.message_id = None
    special(".g", user)  #

    user.in_setup = True


def __main_loop(user):
    pbfr()  #
    sendmsg(user)  #
    if TkGlobals.rd_qd:
        rte(user)  #
    TkGlobals.rd_qd = 0  #
    World.close()  #
    pbfr()  #


def talker(user):
    # TODO: Remove this
    TkGlobals.set_user(user)

    try:
        __setup(user)
    except NoDatabaseException:
        crapup("Sorry AberMUD is currently unavailable") #
    except CrapupException as message:
        crapup(message)  #
    except WorldFullException as message:
        print(message)
        return 0

    while True:
        __main_loop(user)
