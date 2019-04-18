from .dummies import DummyGlobals, eorte
from ..aber_bprintf import bprintf
from ..aber_gamego import crapup
from .sysctrl import sysctrl
from ..database.world import World
from ..database.exceptions import NoWorldFileException


def mstoout(message, user):
    # Print appropriate stuff from data block
    if DummyGlobals.debug_mode:
        bprintf("\n<{}>".format(message.code))

    if message.is_special:
        sysctrl(message, str(user).lower())
    else:
        bprintf(str(message))


def rte(user):
    try:
        unit = World.open()

        if user.message_id is None:
            user.message_id = World.database.load_end()

        too = World.database.find_end(unit)
        for message_id in range(user.message_id, too):
            message = World.load_message(message_id)
            mstoout(message, user)
        user.message_id = too

        user.update()
        eorte()

        DummyGlobals.rdes = 0
        DummyGlobals.tdes = 0
        DummyGlobals.vdes = 0
    except NoWorldFileException:
        crapup("AberMUD: FILE_ACCESS : Access failed\n")
