"""
Extensions section 1
"""
from ..errors import CrapupError

from ..bprintf import bprintf
from ..magic import randperc
from ..newuaf import NewUaf, delpers
from ..objsys import ObjSys, dumpitems, dumpstuff, iscarrby
from ..opensys import closeworld, openworld
from ..parse import Parse, calibme
from ..support import Item, Player, syslog
from ..tk import Tk, loseme, sendsys, trapch
from .disease import Diseases
from .utils import get_item


class PlayerData:
    def __init__(self, name, location, strength, sex, level):
        self.name = name
        self.location = location
        self.strength = strength
        self.sex = sex
        self.level = level


SCALES = {
    1: 2,
    2: 3,
    3: 3,
    4: 4,
    5: 4,
    6: 5,
    7: 6,
}


MOBILES = [
    PlayerData("The Wraith", -1077, 60, 0, -2),
    PlayerData("Shazareth", -1080, 99, 0, -30),
    PlayerData("Bomber", -308, 50, 0, -10),
    PlayerData("Owin", -311, 50, 0, -11),
    PlayerData("Glowin", -318, 50, 0, -12),
    PlayerData("Smythe", -320, 50, 0, -13),
    PlayerData("Dio", -332, 50, 0, -14),
    PlayerData("The Dragon", -326, 500, 0, -2),
    PlayerData("The Zombie", -639, 20, 0, -2),
    PlayerData("The Golem", -1056, 90, 0, -2),

    PlayerData("The Haggis", -341, 50, 0, -2),
    PlayerData("The Piper", -630, 50, 0, -2),
    PlayerData("The Rat", -1064, 20, 0, -2),
    PlayerData("The Ghoul", -129, 40, 0, -2),
    PlayerData("The Figure", -130, 90, 0, -2),
    PlayerData("The Ogre", -144, 40, 0, -2),
    PlayerData("Riatha", -165, 50, 0, -31),
    PlayerData("The Yeti", -173, 80, 0, -2),
    PlayerData("The Guardian", -197, 50, 0, -2),
    PlayerData("Prave", -201, 60, 0, -400),

    PlayerData("Wraith", -350, 60, 0, -2),
    PlayerData("Bath", -1, 70, 0, -401),
    PlayerData("Ronnie", -809, 40, 0, -402),
    PlayerData("The Mary", -1, 50, 0, -403),
    PlayerData("The Cookie", -126, 70, 0, -404),
    PlayerData("MSDOS", -1, 50, 0, -405),
    PlayerData("The Devil", -1, 70, 0, -2),
    PlayerData("The Copper", -1, 40, 0, -2),
]


DISEASES = Diseases()


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
    sendsys(
        Tk.globme,
        Tk.globme,
        -10000,
        Tk.curch,
        "{} has just died\n".format(Tk.globme),
    )
    sendsys(
        Tk.globme,
        Tk.globme,
        -10113,
        Tk.curch,
        "[ {} has just died ]\n".format(Tk.globme),
    )
    raise CrapupError("Oh dear you just died\n")


def new1_receive(is_me, channel, to__, from__, code, text):
    if code == -10100:
        if is_me != 1:
            return
        bprintf("All your ailments have been cured\n")

        DISEASES.cure()
    elif code == -10101:
        if is_me != 1:
            return
        DISEASES.crippled.magic(from__)
    elif code == -10102:
        if is_me != 1:
            return
        DISEASES.dumb.magic(from__)
    elif code == -10103:
        if is_me != 1:
            return
        DISEASES.force.magic(from__, text)
    elif code == -10104:
        if is_me == 1:
            return
        bprintf("\001p{}\001 shouts '{}'\n".format(from__, text))
    elif code == -10105:
        if is_me != 1:
            return
        DISEASES.blind.magic(from__)
    elif code == -10106:
        if __iam(from__):
            return
        if Tk.curch != channel:
            return
        bprintf("Bolts of fire leap from the fingers of \001p{}\001\n".format(from__))
        if is_me == 1:
            __wounded(int(text), "You are struck!\n")
        else:
            bprintf("\001p{}\001 is struck\n".format(to__))
    elif code == -10107:
        if is_me != 1:
            return
        bprintf("Your sex has been magically changed!\n")
        NewUaf.my_sex = 1 - NewUaf.my_sex
        bprintf("You are now ")
        if NewUaf.my_sex:
            bprintf("Female\n")
        else:
            bprintf("Male\n")
        calibme()
    elif code == -10109:
        if __iam(from__):
            return
        if Tk.curch != channel:
            return
        bprintf("\001p{}\001 casts a fireball\n".format(from__))
        if is_me == 1:
            __wounded(int(text), "You are struck!\n")
        else:
            bprintf("\001p{}\001 is struck\n".format(to__))
    elif code == -10110:
        if __iam(from__):
            return
        if is_me != 1:
            return
        __wounded(int(text), "\001p{}\001 touches you giving you a sudden electric shock!\n".format(from__))
    elif code == -10111:
        if is_me != 1:
            return
        bprintf("{}\n".format(text))
    elif code == -10113:
        if NewUaf.my_lev > 9:
            bprintf(text)
    elif code == -10120:
        if is_me != 1:
            return
        DISEASES.deaf.magic(from__)


def tscale():
    players = len(list(filter(lambda player: len(player.name) > 0, [Player(b) for b in range(16)])))
    return SCALES.get(players, 7)


def woundmn(enemy, damage):
    new_strength = enemy.strength - damage
    enemy.strength = new_strength

    if new_strength >= 0:
        return mhitplayer(enemy)

    dumpstuff(enemy, enemy.location)
    sendsys(
        "",
        "",
        -10000,
        enemy.location,
        "{} has just died\n".format(enemy.name),
    )
    enemy.name = ""
    sendsys(
        "",
        "",
        -10113,
        enemy.location,
        "[ {} has just died ]\n".format(enemy.name),
    )


def mhitplayer(enemy):
    if enemy.location != Tk.curch:
        return
    if enemy.player_id < 0 or enemy.player_id > 47:
        return
    roll = randperc()
    to_hit = 3 * (15 - NewUaf.my_lev) + 20
    if Item(89).is_worn_by(Tk.mynum) or Item(113).is_worn_by(Tk.mynum) or Item(114).is_worn_by(Tk.mynum):
        to_hit -= 10
    if roll < to_hit:
        data = [
            enemy,
            randperc() % enemy.damage,
            -1,
        ]
    else:
        data = [
            enemy,
            -1,
            -1,
        ]
    sendsys(
        Tk.globme,
        enemy.name,
        -10021,
        enemy.location,
        data,
    )


def resetplayers():
    for mobile_id, mobile in MOBILES:
        player = Player(mobile_id + 16)
        player.name = mobile.name
        player.location = mobile.location
        player.strength = mobile.strength
        player.sex = mobile.sex
        player.weapon = None
        player.visible = 0
        player.level = mobile.level
    for a in range(35, 48):
        Player(a).name = ""


def teletrap(new_channel):
    sendsys(
        Tk.globme,
        Tk.globme,
        -10000,
        Tk.curch,
        "\001s{name}\001{name} has left.\n\001".format(name=Tk.globme),
    )
    Tk.curch = new_channel
    sendsys(
        Tk.globme,
        Tk.globme,
        -10000,
        Tk.curch,
        "\001s{name}\001{name} has arrived.\n\001".format(name=Tk.globme),
    )
    trapch(Tk.curch)


def on_flee_event():
    for item_id in range(ObjSys.numobs):
        item = Item(item_id)
        if iscarrby(item_id, Tk.mynum) and not item.is_worn_by(Tk.mynum):
            item.setoloc(Player(Tk.mynum).location, 0)
