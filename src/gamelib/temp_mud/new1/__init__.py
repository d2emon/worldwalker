"""
Extensions section 1
"""
from ..magic import randperc
from ..newuaf import NewUaf
from ..objsys import ObjSys, dumpstuff, iscarrby
from ..parse.messages import Message
from ..support import Item, Player
from ..tk import Tk, trapch
from .disease import Diseases
from .messages import MSG_GLOBAL, MSG_WIZARD, MSG_WOUND
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


def tscale():
    players = len(list(filter(lambda player: len(player.name) > 0, [Player(b) for b in range(16)])))
    return SCALES.get(players, 7)


def woundmn(enemy, damage):
    new_strength = enemy.strength - damage
    enemy.strength = new_strength

    if new_strength >= 0:
        return mhitplayer(enemy)

    dumpstuff(enemy, enemy.location)
    Message(
        None,
        None,
        MSG_GLOBAL,
        enemy.location,
        "{} has just died\n".format(enemy.name),
    ).send()
    enemy.name = ""
    Message(
        None,
        None,
        MSG_WIZARD,
        enemy.location,
        "[ {} has just died ]\n".format(enemy.name),
    ).send()


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
    Message(
        Tk,
        enemy,
        MSG_WOUND,
        enemy.location,
        data,
    ).send()


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
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        Tk.curch,
        "\001s{name}\001{name} has left.\n\001".format(name=Tk.globme),
    ).send()
    Tk.curch = new_channel
    Message(
        Tk,
        Tk,
        MSG_GLOBAL,
        Tk.curch,
        "\001s{name}\001{name} has arrived.\n\001".format(name=Tk.globme),
    ).send()
    trapch(Tk.curch)


def on_flee_event():
    for item_id in range(ObjSys.numobs):
        item = Item(item_id)
        if iscarrby(item_id, Tk.mynum) and not item.is_worn_by(Tk.mynum):
            item.setoloc(Player(Tk.mynum).location, 0)
