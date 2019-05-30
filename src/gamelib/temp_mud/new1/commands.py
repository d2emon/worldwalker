from ..errors import CommandError, CrapupError
from ..blood import Blood
from ..mobile import dragget
from ..newuaf import NewUaf
from ..parse.messages import Message
from ..support import Item, Player, ohany, iscarrby
from ..tk import Tk, broad, loseme, trapch
from ..weather import sillycom
from . import teletrap, woundmn
from .disease import DISEASES
from .messages import MSG_GLOBAL, MSG_CURE, MSG_CRIPPLE, MSG_DUMB, MSG_FORCE, MSG_BOLT, MSG_BLIND, MSG_CHANGE, \
    MSG_FIREBALL, MSG_SHOCK, MSG_DEAF
from .utils import get_item, victim_is_here, victim_magic, victim_magic_is_here, social


def bouncecom():
    sillycom("\001s%s\001%s bounces around\n\001")
    yield "B O I N G !!!!\n"


def sighcom():
    DISEASES.dumb.check()
    sillycom("\001P%s\001\001d sighs loudly\n\001")
    yield "You sigh\n"


def screamcom():
    DISEASES.dumb.check()
    sillycom("\001P%s\001\001d screams loudly\n\001")
    yield "ARRRGGGGHHHHHHHHHHHH!!!!!!\n"


def opencom(parser):
    item = get_item(parser)
    if item.item_id == 21:
        if Item(21).state == 0:
            raise CommandError("It is\n")
        else:
            raise CommandError("It seems to be magically closed\n")
    elif item.item_id == 1:
        if Item(1).state == 1:
            raise CommandError("It is\n")
        else:
            Item(1).state = 1
            yield "The Umbrella Opens\n"
    elif item.item_id == 20:
        raise CommandError("You can't shift the door from this side!!!!\n")
    else:
        if item.tstbit(2) == 0:
            raise CommandError("You can't open that\n")
        elif item.state == 0:
            raise CommandError("It already is\n")
        elif item.state == 2:
            raise CommandError("It's locked!\n")
        else:
            item.state = 0
            yield "Ok\n"


def closecom(parser):
    item = get_item(parser)
    if item.item_id == 1:
        if Item(1).state == 0:
            raise CommandError("It is closed, silly!\n")
        else:
            Item(1).state = 0
            yield "Ok\n"
    else:
        if item.tstbit(2) == 0:
            raise CommandError("You can't close that\n")
        elif item.state != 0:
            raise CommandError("It is open already\n")
        else:
            item.state = 1
            yield "Ok\n"


def lockcom(parser):
    item = get_item(parser)
    if not ohany(1 << 11):
        raise CommandError("You haven't got a key\n")
    else:
        if item.tstbit(3) == 0:
            raise CommandError("You can't lock that!\n")
        elif item.state != 0:
            raise CommandError("It's already locked\n")
        else:
            item.state = 2
            yield "Ok\n"


def unlockcom(parser):
    item = get_item(parser)
    if not ohany(1 << 11):
        raise CommandError("You have no keys\n")
    else:
        if item.tstbit(3) == 0:
            raise CommandError("You can't unlock that\n")
        elif item.state != 0:
            raise CommandError("Its not locked!\n")
        else:
            item.state = 1
            yield "Ok...\n"


def wavecom(parser):
    item = get_item(parser)
    if item.item_id == 136:
        if Item(151).state == 1 and Item(151).loc == Tk.curch:
            Item(150).state = 0
            yield "The drawbridge is lowered!\n"
        return
    elif item.item_id == 158:
        yield "You are teleported!\n"
        teletrap(-114)
        return
    else:
        yield "Nothing happens\n"


def blowcom(parser):
    get_item(parser)
    raise CommandError("You can't blow that\n")


def putcom(parser):
    item = get_item(parser)
    word = parser.brkword()
    if word is None:
        raise CommandError("where ?\n")
    if word in ['on', 'in']:
        word = parser.brkword()
    if word is None:
        raise CommandError("What ?\n")

    c = Item.fobna(word)
    if c is None:
        raise CommandError("There isn't one of those here.\n")
    elif c.item_id == 10:
        if item.item_id < 4 or item.item_id > 6:
            raise CommandError("You can't do that\n")
        if Item(10).state != 2:
            raise CommandError("There is already a candle in it!\n")

        yield "The candle fixes firmly into the candlestick\n"
        NewUaf.my_sco += 50
        item.destroy()
        Item(10).setbyte(1, item)
        Item(10).setbit(9)
        Item(10).setbit(10)
        if item.tstbit(13):
            Item(10).setbit(13)
            Item(10).state = 0
        else:
            Item(10).state = 1
            Item(10).clearbit(13)
        return
    elif c.item_id == 137:
        if c.state == 0:
            item.setloc(-162, 0)
            yield "ok\n"
            return
        item.destroy()
        yield "It dissappears with a fizzle into the slime\n"
        if item.item_id == 108:
            yield "The soap dissolves the slime away!\n"
            Item(137).state = 0
        return
    elif c.item_id == 193:
        raise CommandError("You can't do that, the chute leads up from here!\n")
    elif c.item_id == 192:
        if item.item_id == 32:
            raise CommandError("You can't let go of it!\n")
        yield "It vanishes down the chute....\n"
        Message(
            None,
            None,
            MSG_GLOBAL,
            Item(193).loc,
            "The {} comes out of the chute!\n".format(item.name)
        ).send()
        item.setloc(Item(193).loc, 0)
        return
    elif c.item_id == 23:
        if item.item_id == 19 and Item(21).state == 1:
            yield "The door clicks open!\n"
            Item(20).state = 0
            return
        yield "Nothing happens\n"
        return
    elif c.item_id == item.item_id:
        raise CommandError("What do you think this is, the goon show ?\n")
    else:
        if c.tstbit(14) == 0:
            raise CommandError("You can't do that\n")
        if item.obflannel:
            raise CommandError("You can't take that !\n")
        if dragget():
            return
        if item.item_id == 32:
            raise CommandError("You can't let go of it!\n")
        item.setoloc(c.item_id, 23)
        yield "Ok.\n"
        Message(
            Tk,
            Tk,
            MSG_GLOBAL,
            Tk.curch,
            "\001D{}\001\001c puts the {} in the {}.\n\001".format(Tk.globme, item.name, c.name)
        ).send()
        if item.tstbit(12):
            item.state = 0
        if Tk.curch == -1081:
            Item(20).state = 1
            yield "The door clicks shut....\n"


def lightcom(parser):
    item = get_item(parser)
    if not ohany(1 << 13):
        raise CommandError("You have nothing to light things from\n")
    else:
        if not item.tstbit(9):
            raise CommandError("You can't light that!\n")
        elif item.state == 0:
            raise CommandError("It is lit\n")
        item.state = 0
        item.setbit(13)
        yield "Ok\n"


def extinguishcom(parser):
    item = get_item(parser)
    if not item.tstbit(13):
        raise CommandError("That isn't lit\n")
    if not item.tstbit(10):
        raise CommandError("You can't extinguish that!\n")
    item.state = 1
    item.clearbit(13)
    yield "Ok\n"


def pushcom(parser):
    word = parser.brkword()
    if word is None:
        raise CommandError("Push what ?\n")
    x = Item.fobna(word)
    if x is None:
        raise CommandError("That is not here\n")
    elif x.item_id == 126:
        yield "The tripwire moves and a huge stone crashes down from above!\n"
        broad("\001dYou hear a thud and a squelch in the distance.\n\001")
        loseme()
        raise CrapupError("             S   P    L      A         T           !")
    elif x.item_id == 162:
        yield "A trapdoor opens at your feet and you plumment downwards!\n"
        Tk.curch = -140
        trapch(Tk.curch)
        return
    elif x.item_id == 130:
        if Item(132).state == 1:
            Item(132).state = 0
            yield "A secret panel opens in the east wall!\n"
        else:
            yield "Nothing happens\n"
    elif x.item_id == 131:
        if Item(134).state == 1:
            yield "Uncovering a hole behind it.\n"
            Item(134).state = 0
    elif x.item_id == 138:
        if Item(137).state == 0:
            yield "Ok...\n"
        else:
            yield "You hear a gurgling noise and then silence.\n"
            Item(137).state = 0
    elif x.item_id in (146, 147):
        Item(146).state = 1 - Item(146).state
        yield "Ok...\n"
    elif x.item_id == 30:
        Item(28).state = 1 - Item(28).state
        if Item(28).state:
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(28).loc,
                "\001cThe portcullis falls\n\001",
            ).send()
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(29).loc,
                "\001cThe portcullis falls\n\001",
            ).send()
        else:
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(28).loc,
                "\001cThe portcullis rises\n\001",
            ).send()
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(29).loc,
                "\001cThe portcullis rises\n\001",
            ).send()
    elif x.item_id == 149:
        Item(150).state = 1 - Item(150).state
        if Item(150).state:
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(150).loc,
                "\001cThe drawbridge rises\n\001",
            ).send()
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(151).loc,
                "\001cThe drawbridge rises\n\001",
            ).send()
        else:
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(150).loc,
                "\001cThe drawbridge is lowered\n\001",
            ).send()
            Message(
                None,
                None,
                MSG_GLOBAL,
                Item(151).loc,
                "\001cThe drawbridge is lowered\n\001",
            ).send()
    elif x.item_id == 24:
        if Item(26).state == 1:
            Item(26).state = 0
            yield "A secret door slides quietly open in the south wall!!!\n"
        else:
            yield "It moves but nothing seems to happen\n"
    elif x.item_id == 49:
        broad("\001dChurch bells ring out around you\n\001")
    elif x.item_id == 104:
        if Player(Tk.mynum).tothlp == -1:
            raise CommandError("You can't shift it alone, maybe you need help\n")
        broad("\001dChurch bells ring out around you\n\001")
    else:
        # ELSE RUN INTO DEFAULT
        if x.tstbit(4):
            x.state = 0
            x.oplong()
            return
        if x.tstbit(5):
            x.state = 1 - x.state
            x.oplong()
            return
        yield "Nothing happens\n"


def cripplecom(parser):
    victim = victim_magic(parser)
    Message(
        victim,
        Tk,
        MSG_CRIPPLE,
        Tk.curch,
        "",
    ).send()


def curecom(parser):
    victim = victim_magic_is_here(parser)
    Message(
        victim,
        Tk,
        MSG_CURE,
        Tk.curch,
        "",
    ).send()


def dumbcom(parser):
    victim = victim_magic(parser)
    Message(
        victim,
        Tk,
        MSG_DUMB,
        Tk.curch,
        "",
    ).send()


def forcecom(parser):
    victim = victim_magic(parser)
    Message(
        victim,
        Tk,
        MSG_FORCE,
        Tk.curch,
        parser.getreinput(),
    ).send()


def missilecom(parser):
    victim = victim_magic_is_here(parser)
    Message(
        victim,
        Tk,
        MSG_BOLT,
        Tk.curch,
        NewUaf.my_lev * 2,
    ).send()
    if victim.strength - 2 * NewUaf.my_lev < 0:
        yield "Your last spell did the trick\n"
        if victim.strength >= 0:
            # Bonus ?
            if victim.player_id < 16:
                NewUaf.my_sco += victim.level * victim.level * 100
            else:
                NewUaf.my_sco += 10 * victim.damage
        victim.strength = -1  # MARK ALREADY DEAD
        Blood.in_fight = 0
        Blood.fighting = -1
    if victim.player_id > 15:
        woundmn(victim, 2 * NewUaf.my_lev)


def changecom(parser):
    word = parser.brkword()
    if word is None:
        raise CommandError("change what (Sex ?) ?\n")
    if word != 'sex':
        raise CommandError("I don't know how to change that\n")
    victim = victim_magic(parser)
    Message(
        victim,
        Tk,
        MSG_CHANGE,
        Tk.curch,
        "",
    ).send()
    if victim.player_id < 16:
        return
    victim.sex = 1 - victim.sex


def fireballcom(parser):
    victim = victim_magic_is_here(parser)
    if Tk.mynum == victim.player_id:
        raise CommandError("Seems rather dangerous to me....\n")
    wound = 6 if victim.player_id == Player.fpbns('yeti').player_id else 2
    if victim.strength - wound * NewUaf.my_lev < 0:
        yield "Your last spell did the trick\n"
        if victim.strength >= 0:
            # Bonus ?
            if victim.player_id < 16:
                NewUaf.my_sco += victim.level * victim.level * 100
            else:
                NewUaf.my_sco += 10 * victim.damage
        victim.strength = -1  # MARK ALREADY DEAD
        Blood.in_fight = 0
        Blood.fighting = -1
    Message(
        victim,
        Tk,
        MSG_FIREBALL,
        Tk.curch,
        2 * NewUaf.my_lev,
    ).send()
    if victim.player_id == Player.fpbns('yeti').player_id:
        woundmn(victim, 6 * NewUaf.my_lev)
        return
    if victim.player_id > 15:
        woundmn(victim, 2 * NewUaf.my_lev)


def shockcom(parser):
    victim = victim_magic_is_here(parser)
    if victim.player_id == Tk.mynum:
        raise CommandError("You are supposed to be killing other people not yourself\n")
    if victim.strength - 2 * NewUaf.my_lev < 0:
        yield "Your last spell did the trick\n"
        if victim.strength >= 0:
            # Bonus ?
            if victim.player_id < 16:
                NewUaf.my_sco += victim.level * victim.level * 100
            else:
                NewUaf.my_sco += 10 * victim.damage
        victim.strength = -1  # MARK ALREADY DEAD
        Blood.in_fight = 0
        Blood.fighting = -1
    Message(
        victim,
        Tk,
        MSG_SHOCK,
        Tk.curch,
        2 * NewUaf.my_lev,
    ).send()
    if victim.player_id > 15:
        woundmn(victim, 2 * NewUaf.my_lev)


def starecom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        raise CommandError("That is pretty neat if you can do it!\n")
    social(victim, "stares deep into your eyes\n")
    yield "You stare at \001p{}\001\n".format(victim.name)


def gropecom(parser):
    if DISEASES.force.is_force:
        raise CommandError("You can't be forced to do that\n")
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        yield "With a sudden attack of morality the machine edits your persona\n"
        loseme()
        raise CrapupError("Bye....... LINE TERMINATED - MORALITY REASONS")
    social(victim, "gropes you")
    yield "<Well what sort of noise do you want here ?>\n"


def squeezecom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        yield "Ok....\n"
    social(victim, "gives you a squeeze\n")
    yield "You give them a squeeze\n"


def kisscom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        raise CommandError("Weird!\n")
    social(victim, "kisses you")
    yield "Slurp!\n"


def cuddlecom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        raise CommandError("You aren't that lonely are you ?\n")
    social(victim, "cuddles you")


def hugcom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        raise CommandError("Ohhh flowerr!\n")
    social(victim, "hugs you")


def slapcom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        yield "You slap yourself\n"
        return
    social(victim, "slaps you")


def ticklecom(parser):
    victim = victim_is_here(parser)
    if victim.player_id == Tk.mynum:
        yield "You tickle yourself\n"
        return
    social(victim, "tickles you")


def wearcom(parser):
    item = get_item(parser)
    if not iscarrby(item.item_id, Tk.mynum):
        raise CommandError("You are not carrying this\n")
    if item.is_worn_by(Tk.mynum):
        raise CommandError("You are wearing this\n")
    if (Item(89).is_worn_by(Tk.mynum) or Item(113).is_worn_by(Tk.mynum) or Item(114).is_worn_by(Tk.mynum)) \
            and (item.item_id == 89 or item.item_id == 113 or item.item_id == 114):
        raise CommandError("You can't use TWO shields at once...\n")
    if not item.can_wear:
        raise CommandError("Is this a new fashion ?\n")
    item.carry_flag = 2
    yield "OK\n"


def removecom(parser):
    item = get_item(parser)
    if item.is_worn_by(Tk.mynum):
        raise CommandError("You are not wearing this\n")
    item.carry_flag = 1


def deafcom():
    victim = victim_magic()
    Message(
        victim,
        Tk,
        MSG_DEAF,
        Tk.curch,
        "",
    ).send()


def blindcom():
    victim = victim_magic()
    Message(
        victim,
        Tk,
        MSG_BLIND,
        Tk.curch,
        "",
    ).send()
