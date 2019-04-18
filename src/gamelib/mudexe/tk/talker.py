from .dummies import DummyGlobals, makebfr, pbfr
from .tkGlobals import TkGlobals
from .rte import rte
from .sendmsg import sendmsg
from .special import special
from ..aber_opensys.world import World, NoDatabaseException
from ..aber_gamego import crapup
from ..exceptions import CrapupException
from ..database.exceptions import WorldFullException
from .exceptions import WorldUnavailableException


def __setup(user):
    makebfr()  #

    user.message_id = None
    user.put_on()

    World.open()
    if user.person_id >= DummyGlobals.maxu:
        raise WorldFullException
    rte(user)  #
    World.close()

    user.message_id = None

    special(".g", user)  #
    TkGlobals.i_setup = 1  #


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
        raise WorldUnavailableException()  # Crapup
    except CrapupException as message:
        crapup(message)  #
    except WorldFullException as message:
        print(message)
        return 0

    while True:
        __main_loop(user)
