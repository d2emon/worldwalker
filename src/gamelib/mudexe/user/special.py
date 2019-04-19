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

    user.person.strength = user.strength
    user.person.level = user.level
    if user.level < 10000:
        user.person.vis = 0
    else:
        user.person.vis = 10000
    user.person.weapon = None
    user.person.sexall = user.sex
    user.person.helping = None

    xy = "\001s{name}\001{name}  has entered the game\n\001".format(name=str(user))
    xx = "\001s{name}\001[ {name}  has entered the game ]\n\001".format(name=str(user))
    sendsys(str(user), str(user), -10113, user.location_id, xx)

    user.rte()

    if randperc() > 50:
        trapch(-5)
    else:
        user.location_id = -183
        trapch(-183)
    sendsys(str(user), str(user), -10000, user.location_id, xy)


SPECIAL_COMMANDS = {
    'g': __g,
}
