from ..aber_magic import randperc
from ..aber_newuaf1 import initme
from ..aber_parse import sendsys
from ..tk.trapch import trapch
from ..database.world import World


def __g(user):
    user.mode = 1
    user.location_id = -5
    initme()
    World.open()

    user.init_person()

    sendsys(
        user,
        user,
        -10113,
        user.location_id,
        "\001s{name}\001[ {name}  has entered the game ]\n\001".format(name=str(user)),
    )

    user.rte(save=False)

    if randperc() > 50:
        trapch(-5)
    else:
        user.location_id = -183
        trapch(-183)

    sendsys(
        user,
        user,
        -10000,
        user.location_id,
        "\001s{name}\001{name}  has entered the game\n\001".format(name=str(user)),
    )


SPECIAL_COMMANDS = {
    'g': __g,
}
