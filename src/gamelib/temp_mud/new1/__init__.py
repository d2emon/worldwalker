"""
Extensions section 1
"""


def bprintf(*args):
    raise NotImplementedError()


def brkword(*args):
    raise NotImplementedError()


def broad(*args):
    raise NotImplementedError()


def calibme(*args):
    raise NotImplementedError()


def closeworld(*args):
    raise NotImplementedError()


def delpers(*args):
    raise NotImplementedError()


def dragget(*args):
    raise NotImplementedError()


def dumpitems(*args):
    raise NotImplementedError()


def dumpstuff(*args):
    raise NotImplementedError()


def gamecom(*args):
    raise NotImplementedError()


def getreinput(*args):
    raise NotImplementedError()


def iscarrby(*args):
    raise NotImplementedError()


def loseme(*args):
    raise NotImplementedError()


def ohany(*args):
    raise NotImplementedError()


def openworld(*args):
    raise NotImplementedError()


def randperc(*args):
    raise NotImplementedError()


def sendsys(*args):
    raise NotImplementedError()


def sillycom(*args):
    raise NotImplementedError()


def syslog(*args):
    raise NotImplementedError()


def trapch(*args):
    raise NotImplementedError()


class CommandError(Exception):
    pass


class CrapupError(Exception):
    pass


class Extras:
    curch = None
    my_sco = None
    my_lev = None
    my_str = None
    wordbuf = None
    objinfo = None
    globme = None
    mynum = None
    isforce = None
    numobs = None


class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    @property
    def location(self):
        raise NotImplementedError()

    @location.setter
    def location(self, value):
        raise NotImplementedError()

    @property
    def strength(self):
        raise NotImplementedError()

    @strength.setter
    def strength(self, value):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @name.setter
    def name(self, value):
        raise NotImplementedError()

    @property
    def tothlp(self):
        raise NotImplementedError()

    @property
    def damage(self):
        if self.player_id in (18, 19, 20, 21, 22):
            return 6
        elif self.player_id == 23:
            return 32
        elif self.player_id == 24:
            return 8
        elif self.player_id == 28:
            return 6
        elif self.player_id == 30:
            return 20
        elif self.player_id == 31:
            return 14
        elif self.player_id == 32:
            return 15
        elif self.player_id == 33:
            return 10
        else:
            return 10

    @classmethod
    def fpbns(cls, name):
        raise NotImplementedError()

    @classmethod
    def fpbn(cls, name):
        raise NotImplementedError()


class Item:
    def __init__(self, item_id):
        self.item_id = item_id

    @property
    def state(self):
        return Extras.objinfo[4 * self.item_id + 1]

    @state.setter
    def state(self, value):
        Extras.objinfo[4 * self.item_id + 1] = value
        if self.tstbit(1):
            Extras.objinfo[4 * (self.item_id ^ 1) + 1] = value

    @property
    def carry_flag(self):
        # return Extras.objinfo[4 * self.item_id + 1]
        raise NotImplementedError()

    @carry_flag.setter
    def carry_flag(self, value):
        Extras.objinfo[4 * self.item_id + 3] = value

    @property
    def loc(self):
        raise NotImplementedError()

    @property
    def can_wear(self):
        return self.tstbit(8)

    def destroy(self):
        self.setbit(0)

    def is_worn_by(self, player):
        if not iscarrby(self.item_id, player):
            return False
        if self.carry_flag != 2:
            return False
        return True

    def tstbit(self, *args):
        raise NotImplementedError()

    def setbit(self, *args):
        raise NotImplementedError()

    def clearbit(self, *args):
        raise NotImplementedError()

    def setbyte(self, *args):
        raise NotImplementedError()

    def setoloc(self, *args):
        raise NotImplementedError()

    @classmethod
    def fobna(cls, name):
        raise NotImplementedError()


class PlayerRes:
    def __init__(self, name, location, strength, sex, level):
        self.name = name
        self.location = location
        self.strength = strength
        self.sex = sex
        self.level = level


class Disease:
    def __init__(self, active=False):
        self.__active = active

    @property
    def active(self):
        return self.__active

    def activate(self):
        self.__active = False

    def cure(self):
        self.__active = False


class Dumb(Disease):
    pass


class Crip(Disease):
    pass


class Blind(Disease):
    pass


class Deaf(Disease):
    pass


class New1:
    ail_dumb = Dumb()
    ail_crip = Crip()
    ail_blind = Blind()
    ail_deaf = Deaf()

    __pinit = [
        PlayerRes("The Wraith", -1077, 60, 0, -2),
        PlayerRes("Shazareth", -1080, 99, 0, -30),
        PlayerRes("Bomber", -308, 50, 0, -10),
        PlayerRes("Owin", -311, 50, 0, -11),
        PlayerRes("Glowin", -318, 50, 0, -12),
        PlayerRes("Smythe", -320, 50, 0, -13),
        PlayerRes("Dio", -332, 50, 0, -14),
        PlayerRes("The Dragon", -326, 500, 0, -2),
        PlayerRes("The Zombie", -639, 20, 0, -2),
        PlayerRes("The Golem", -1056, 90, 0, -2),

        PlayerRes("The Haggis", -341, 50, 0, -2),
        PlayerRes("The Piper", -630, 50, 0, -2),
        PlayerRes("The Rat", -1064, 20, 0, -2),
        PlayerRes("The Ghoul", -129, 40, 0, -2),
        PlayerRes("The Figure", -130, 90, 0, -2),
        PlayerRes("The Ogre", -144, 40, 0, -2),
        PlayerRes("Riatha", -165, 50, 0, -31),
        PlayerRes("The Yeti", -173, 80, 0, -2),
        PlayerRes("The Guardian", -197, 50, 0, -2),
        PlayerRes("Prave", -201, 60, 0, -400),

        PlayerRes("Wraith", -350, 60, 0, -2),
        PlayerRes("Bath", -1, 70, 0, -401),
        PlayerRes("Ronnie", -809, 40, 0, -402),
        PlayerRes("The Mary", -1, 50, 0, -403),
        PlayerRes("The Cookie", -126, 70, 0, -404),
        PlayerRes("MSDOS", -1, 50, 0, -405),
        PlayerRes("The Devil", -1, 70, 0, -2),
        PlayerRes("The Copper", -1, 40, 0, -2),
    ]

    __forf = False
    __acfor = ""

    __is_force = False

    @classmethod
    def bouncecom(cls):
        sillycom("\001s%s\001%s bounces around\n\001")
        yield "B O I N G !!!!\n"

    @classmethod
    def sighcom(cls):
        cls.chkdumb()
        sillycom("\001P%s\001\001d sighs loudly\n\001")
        yield "You sigh\n"

    @classmethod
    def screamcom(cls):
        cls.chkdumb()
        sillycom("\001P%s\001\001d screams loudly\n\001")
        yield "ARRRGGGGHHHHHHHHHHHH!!!!!!\n"

    # Door is 6 panel 49

    @classmethod
    def __ohereandget(cls):
        if brkword() is None:
            raise CommandError("Tell me more ?\n")
        openworld()
        onm = Item.fobna(Extras.wordbuf)
        if onm is None:
            raise CommandError("There isn't one of those here\n")
        return onm

    @classmethod
    def opencom(cls):
        a = cls.__ohereandget()
        if a.item_id == 21:
            if Item(21).state == 0:
                raise CommandError("It is\n")
            else:
                raise CommandError("It seems to be magically closed\n")
        elif a.item_id == 1:
            if Item(1).state == 1:
                raise CommandError("It is\n")
            else:
                Item(1).state = 1
                yield "The Umbrella Opens\n"
        elif a.item_id == 20:
            raise CommandError("You can't shift the door from this side!!!!\n")
        else:
            if a.tstbit(2) == 0:
                raise CommandError("You can't open that\n")
            elif a.state == 0:
                raise CommandError("It already is\n")
            elif a.state == 2:
                raise CommandError("It's locked!\n")
            else:
                a.state = 0
                yield "Ok\n"

    @classmethod
    def closecom(cls):
        a = cls.__ohereandget()
        if a.item_id == 1:
            if Item(1).state == 0:
                raise CommandError("It is closed, silly!\n")
            else:
                Item(1).state = 0
                yield "Ok\n"
        else:
            if a.tstbit(2) == 0:
                raise CommandError("You can't close that\n")
            elif a.state != 0:
                raise CommandError("It is open already\n")
            else:
                a.state = 1
                yield "Ok\n"

    @classmethod
    def lockcom(cls):
        a = cls.__ohereandget()
        if not ohany(1 << 11):
            raise CommandError("You haven't got a key\n")
        else:
            if a.tstbit(3) == 0:
                raise CommandError("You can't lock that!\n")
            elif a.state != 0:
                raise CommandError("It's already locked\n")
            else:
                a.state = 2
                yield "Ok\n"

    @classmethod
    def unlockcom(cls):
        a = cls.__ohereandget()
        if not ohany(1 << 11):
            raise CommandError("You have no keys\n")
        else:
            if a.tstbit(3) == 0:
                raise CommandError("You can't unlock that\n")
            elif a.state != 0:
                raise CommandError("Its not locked!\n")
            else:
                a.state = 1
                yield "Ok...\n"

    @classmethod
    def wavecom(cls):
        a = cls.__ohereandget()
        if a.item_id == 136:
            if Item(151).state == 1 and Item(151).loc == Extras.curch:
                Item(150).state = 0
                yield "The drawbridge is lowered!\n"
            return
        elif a.item_id == 158:
            yield "You are teleported!\n"
            cls.__teletrap(-114)
            return
        else:
            yield "Nothing happens\n"

    @classmethod
    def blowcom(cls):
        cls.__ohereandget()
        raise CommandError("You can't blow that\n")

    @classmethod
    def putcom(cls):
        a = cls.__ohereandget()
        if brkword() is None:
            raise CommandError("where ?\n")
        elif Extras.wordbuf in ['on', 'in']:
            if brkword() is None:
                raise CommandError("What ?\n")

        c = Item.fobna(Extras.wordbuf)
        if c is None:
            raise CommandError("There isn't one of those here.\n")
        elif c.item_id == 10:
            if a.item_id < 4 or a.item_id > 6:
                raise CommandError("You can't do that\n")
            if Item(10).state != 2:
                raise CommandError("There is already a candle in it!\n")

            yield "The candle fixes firmly into the candlestick\n"
            Extras.my_sco += 50
            a.destroy()
            Item(10).setbyte(1, a)
            Item(10).setbit(9)
            Item(10).setbit(10)
            if a.tstbit(13):
                Item(10).setbit(13)
                Item(10).state = 0
            else:
                Item(10).state = 1
                Item(10).clearbit(13)
            return
        elif c.item_id == 137:
            if c.state == 0:
                a.setloc(-162, 0)
                yield "ok\n"
                return
            a.destroy()
            yield "It dissappears with a fizzle into the slime\n"
            if a.item_id == 108:
                yield "The soap dissolves the slime away!\n"
                Item(137).state = 0
            return
        elif c.item_id == 193:
            raise CommandError("You can't do that, the chute leads up from here!\n")
        elif c.item_id == 192:
            if a.item_id == 32:
                raise CommandError("You can't let go of it!\n")
            yield "It vanishes down the chute....\n"
            sendsys(
                '',
                '',
                -10000,
                Item(193).loc,
                "The {} comes out of the chute!\n".format(a.name)
            )
            a.setloc(Item(193).loc, 0)
            return
        elif c.item_id == 23:
            if a.item_id == 19 and Item(21).state == 1:
                yield "The door clicks open!\n"
                Item(20).state = 0
                return
            yield "Nothing happens\n"
            return
        elif c.item_id == a.item_id:
            raise CommandError("What do you think this is, the goon show ?\n")
        else:
            if c.tstbit(14) == 0:
                raise CommandError("You can't do that\n")
            if a.obflannel:
                raise CommandError("You can't take that !\n")
            if dragget():
                return
            if a.item_id == 32:
                raise CommandError("You can't let go of it!\n")
            a.setoloc(c.item_id, 23)
            yield "Ok.\n"
            sendsys(
                Extras.globme,
                Extras.globme,
                -10000,
                Extras.curch,
                "\001D{}\001\001c puts the {} in the {}.\n\001".format(Extras.globme, a.name, c.name)
            )
            if a.tstbit(12):
                a.state = 0
            if Extras.curch == -1081:
                Item(20).state = 1
                yield "The door clicks shut....\n"

    @classmethod
    def lightcom(cls):
        a = cls.__ohereandget()
        if not ohany(1 << 13):
            raise CommandError("You have nothing to light things from\n")
        else:
            if not a.tstbit(9):
                raise CommandError("You can't light that!\n")
            elif a.state == 0:
                raise CommandError("It is lit\n")
            a.state = 0
            a.setbit(13)
            yield "Ok\n"

    @classmethod
    def extinguishcom(cls):
        a = cls.__ohereandget()
        if not a.tstbit(13):
            raise CommandError("That isn't lit\n")
        if not a.tstbit(10):
            raise CommandError("You can't extinguish that!\n")
        a.state = 1
        a.clearbit(13)
        yield "Ok\n"

    @classmethod
    def pushcom(cls):
        if brkword() is None:
            raise CommandError("Push what ?\n")
        x = Item.fobna(Extras.wordbuf)
        if x is None:
            raise CommandError("That is not here\n")
        elif x.item_id == 126:
            yield "The tripwire moves and a huge stone crashes down from above!\n"
            broad("\001dYou hear a thud and a squelch in the distance.\n\001")
            loseme()
            raise CrapupError("             S   P    L      A         T           !")
        elif x.item_id == 162:
            yield "A trapdoor opens at your feet and you plumment downwards!\n"
            Extras.curch = -140
            trapch(Extras.curch)
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
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(28).loc,
                    "\001cThe portcullis falls\n\001",
                )
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(29).loc,
                    "\001cThe portcullis falls\n\001",
                )
            else:
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(28).loc,
                    "\001cThe portcullis rises\n\001",
                )
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(29).loc,
                    "\001cThe portcullis rises\n\001",
                )
        elif x.item_id == 149:
            Item(150).state = 1 - Item(150).state
            if Item(150).state:
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(150).loc,
                    "\001cThe drawbridge rises\n\001",
                )
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(151).loc,
                    "\001cThe drawbridge rises\n\001",
                )
            else:
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(150).loc,
                    "\001cThe drawbridge is lowered\n\001",
                )
                sendsys(
                    "",
                    "",
                    -10000,
                    Item(151).loc,
                    "\001cThe drawbridge is lowered\n\001",
                )
        elif x.item_id == 24:
            if Item(26).state == 1:
                Item(26).state = 0
                yield "A secret door slides quietly open in the south wall!!!\n"
            else:
                yield "It moves but nothing seems to happen\n"
        elif x.item_id == 49:
            broad("\001dChurch bells ring out around you\n\001")
        elif x.item_id == 104:
            if Player(Extras.mynum).tothlp == -1:
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

    @classmethod
    def cripplecom(cls):
        a = cls.__victim()
        sendsys(
            a.name,
            Extras.globme,
            -10101,
            Extras.curch,
            "",
        )

    @classmethod
    def curecom(cls):
        a = cls.__vichfb()
        sendsys(
            a.name,
            Extras.globme,
            -10100,
            Extras.curch,
            "",
        )

    @classmethod
    def dumbcom(cls):
        a = cls.__victim()
        sendsys(
            a.name,
            Extras.globme,
            -10102,
            Extras.curch,
            "",
        )

    @classmethod
    def forcecom(cls):
        a = cls.__victim()
        sendsys(
            a.name,
            Extras.globme,
            -10103,
            Extras.curch,
            getreinput(),
        )

    @classmethod
    def missilecom(cls):
        a = cls.__vichfb()
        sendsys(
            a.name,
            Extras.globme,
            -10106,
            Extras.curch,
            Extras.my_lev * 2,
        )
        if a.strength - 2 * Extras.my_lev < 0:
            yield "Your last spell did the trick\n"
            if a.strength >= 0:
                # Bonus ?
                if a.player_id < 16:
                    Extras.my_sco += a.level * a.level * 100
                else:
                    Extras.my_sco += 10 * a.damage
            a.strength = -1  # MARK ALREADY DEAD
            Extras.in_fight = 0
            Extras.fighting = -1
        if a.player_id > 15:
            cls.__woundmn(a, 2 * Extras.my_lev)

    @classmethod
    def changecom(cls):
        if brkword() is None:
            raise CommandError("change what (Sex ?) ?\n")
        if Extras.wordbuf != 'sex':
            raise CommandError("I don't know how to change that\n")
        a = cls.__victim()
        sendsys(
            a.name,
            Extras.globme,
            -10107,
            Extras.curch,
            "",
        )
        if a.player_id < 16:
            return
        a.sex = 1 - a.sex

    @classmethod
    def fireballcom(cls):
        a = cls.__vichfb()
        if Extras.mynum == a.player_id:
            raise CommandError("Seems rather dangerous to me....\n")
        wound = 6 if a.player_id == Player.fpbns('yeti').player_id else 2
        if a.strength - wound * Extras.my_lev < 0:
            yield "Your last spell did the trick\n"
            if a.strength >= 0:
                # Bonus ?
                if a.player_id < 16:
                    Extras.my_sco += a.level * a.level * 100
                else:
                    Extras.my_sco += 10 * a.damage
            a.strength = -1  # MARK ALREADY DEAD
            Extras.in_fight = 0
            Extras.fighting = -1
        sendsys(
            a.name,
            Extras.globme,
            -10109,
            Extras.curch,
            2 * Extras.my_lev,
        )
        if a.player_id == Player.fpbns('yeti').player_id:
            cls.__woundmn(a, 6 * Extras.my_lev)
            return
        if a > 15:
            cls.__woundmn(a, 2 * Extras.my_lev)

    @classmethod
    def shockcom(cls):
        a = cls.__vichfb()
        if a.player_id == Extras.mynum:
            raise CommandError("You are supposed to be killing other people not yourself\n")
        if a.strength - 2 * Extras.my_lev < 0:
            yield "Your last spell did the trick\n"
            if a.strength >= 0:
                # Bonus ?
                if a.player_id < 16:
                    Extras.my_sco += a.level * a.level * 100
                else:
                    Extras.my_sco += 10 * a.damage
            a.strength = -1  # MARK ALREADY DEAD
            Extras.in_fight = 0
            Extras.fighting = -1
        sendsys(
            a.name,
            Extras.globme,
            -10110,
            Extras.curch,
            2 * Extras.my_lev,
        )
        if a.player_id > 15:
            cls.__woundmn(a, 2 * Extras.my_lev)

    @classmethod
    def starecom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            raise CommandError("That is pretty neat if you can do it!\n")
        cls.__sillytp(a, "stares deep into your eyes\n")
        yield "You stare at \001p{}\001\n".format(a.name)

    @classmethod
    def gropecom(cls):
        if Extras.isforce:
            raise CommandError("You can't be forced to do that\n")
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            yield "With a sudden attack of morality the machine edits your persona\n"
            loseme()
            raise CrapupError("Bye....... LINE TERMINATED - MORALITY REASONS")
        cls.__sillytp(a, "gropes you")
        yield "<Well what sort of noise do you want here ?>\n"

    @classmethod
    def squeezecom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            yield "Ok....\n"
        cls.__sillytp(a, "gives you a squeeze\n")
        yield "You give them a squeeze\n"

    @classmethod
    def kisscom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            raise CommandError("Weird!\n")
        cls.__sillytp(a, "kisses you")
        yield "Slurp!\n"

    @classmethod
    def cuddlecom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            raise CommandError("You aren't that lonely are you ?\n")
        cls.__sillytp(a, "cuddles you")

    @classmethod
    def hugcom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            raise CommandError("Ohhh flowerr!\n")
        cls.__sillytp(a, "hugs you")

    @classmethod
    def slapcom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            yield "You slap yourself\n"
            return
        cls.__sillytp(a, "slaps you")

    @classmethod
    def ticklecom(cls):
        a = cls.__vichere()
        if a.player_id == Extras.mynum:
            yield "You tickle yourself\n"
            return
        cls.__sillytp(a, "tickles you")

    # This one isnt for magic

    @classmethod
    def __vicbase(cls):
        if brkword() is None:
            raise CommandError("Who ?\n")
        openworld()
        if Extras.wordbuf == "at":
            return cls.__vicbase()  # STARE AT etc
        player = Player.fpbn(Extras.wordbuf)
        if player is None:
            raise CommandError("Who ?\n")
        return player

    @classmethod
    def __vichere(cls):
        player = cls.__vicbase()
        if player.location != Extras.curch:
            raise CommandError("They are not here\n")
        return player

    @classmethod
    def __vicf2(cls, reflectable=False):
        player = cls.__vicbase()
        if Extras.my_str < 10:
            raise CommandError("You are too weak to cast magic\n")
        if Extras.my_lev < 10:
            Extras.my_str -= 2

        i = 5
        if iscarrby(111, Extras.mynum):
            i += 1
        if iscarrby(121, Extras.mynum):
            i += 1
        if iscarrby(163, Extras.mynum):
            i += 1
        if Extras.my_lev < 10 and randperc() > i * Extras.my_lev:
            bprintf("You fumble the magic\n")
            if reflectable:
                bprintf("The spell reflects back\n")
                return Player(Extras.mynum)
            else:
                raise CommandError()
        else:
            if Extras.my_lev < 10:
                bprintf("The spell succeeds!!\n")
        return player

    @classmethod
    def __vicfb(cls):
        return cls.__vicf2()

    @classmethod
    def __vichfb(cls):
        player = cls.__vicfb()
        if player.location != Extras.curch:
            raise CommandError("They are not here\n")
        return player

    @classmethod
    def __victim(cls):
        return cls.__vicf2(True)

    @classmethod
    def __sillytp(cls, per, message):
        if message[:4] == "star":
            bk = "\001s{name}\001{name} {message}\n\001".format(name=Extras.globme, message=message)
        else:
            bk = "\001p{name}\001 {message}\n\001".format(name=Extras.globme, message=message)
        sendsys(
            per.name,
            Extras.globme,
            -10111,
            Extras.curch,
            bk,
        )

    @classmethod
    def new1rcv(cls, isme, chan, to__, from__, code, text):
        if code == -10100:
            if isme != 1:
                return
            bprintf("All your ailments have been cured\n")

            cls.ail_dumb.cure()
            cls.ail_crip.cure()
            cls.ail_blind.cure()
            cls.ail_deaf.cure()
        elif code == -10101:
            if isme != 1:
                return
            if Extras.my_lev < 10:
                bprintf("You have been magically crippled\n")
                cls.ail_crip.activate()
            else:
                bprintf("\001p{}\001 tried to cripple you\n".format(from__))
        elif code == -10102:
            if isme != 1:
                return
            if Extras.my_lev < 10:
                bprintf("You have been struck magically dumb\n")
                cls.ail_dumb.activate()
            else:
                bprintf("\001p{}\001 tried to dumb you\n".format(from__))
        elif code == -10103:
            if isme != 1:
                return
            if Extras.my_lev < 10:
                bprintf("\001p{}\001 has forced you to {}\n".format(from__, text))
                cls.__addforce(text)
            else:
                bprintf("\001p{}\001 tried to force you to {}\n".format(from__, text))
        elif code == -10104:
            if isme == 1:
                return
            bprintf("\001p{}\001 shouts '{}'\n".format(from__, text))
        elif code == -10105:
            if isme != 1:
                return
            if Extras.my_lev < 10:
                bprintf("You have been struck magically blind\n")
                cls.ail_blind.activate()
            else:
                bprintf("\001p{}\001 tried to blind you\n".format(from__))
        elif code == -10106:
            if cls.__iam(from__):
                return
            if Extras.curch != chan:
                return
            bprintf("Bolts of fire leap from the fingers of \001p{}\001\n".format(from__))
            if isme == 1:
                bprintf("You are struck!\n")
                cls.__wounded(int(text))
            else:
                bprintf("\001p{}\001 is struck\n".format(to__))
        elif code == -10107:
            if isme != 1:
                return
            bprintf("Your sex has been magically changed!\n")
            Extras.my_sex = 1 - Extras.my_sex
            bprintf("You are now ")
            if Extras.my_sex:
                bprintf("Female\n")
            else:
                bprintf("Male\n")
            calibme()
        elif code == -10109:
            if cls.__iam(from__):
                return
            if Extras.curch != chan:
                return
            bprintf("\001p{}\001 casts a fireball\n".format(from__))
            if isme == 1:
                bprintf("You are struck!\n")
                cls.__wounded(int(text))
            else:
                bprintf("\001p{}\001 is struck\n".format(to__))
        elif code == -10110:
            if cls.__iam(from__):
                return
            if isme != 1:
                return
            bprintf("\001p{}\001 touches you giving you a sudden electric shock!\n".format(from__))
            cls.__wounded(int(text))
        elif code == -10111:
            if isme != 1:
                return
            bprintf("{}\n".format(text))
        elif code == -10113:
            if Extras.my_lev > 9:
                bprintf(text)
        elif code == -10120:
            if isme != 1:
                return
            if Extras.my_lev > 9:
                bprintf("\001p{}\001 tried to deafen you\n".format(from__))
                return
            else:
                bprintf(bprintf("You have been magically deafened\n"))
                cls.ail_deaf.activate()

    @classmethod
    def tscale(cls):
        scales = {
            1: 2,
            2: 3,
            3: 3,
            4: 4,
            5: 4,
            6: 5,
            7: 6,
        }
        players = len(list(filter(lambda player: len(player.name) > 0, [Player(b) for b in range(16)])))
        return scales.get(players, 7)

    @classmethod
    def chkdumb(cls):
        if cls.ail_dumb.active:
            raise CommandError("You are dumb...\n")

    @classmethod
    def chkcrip(cls):
        if cls.ail_crip.active:
            raise CommandError("You are crippled\n")

    @classmethod
    def chkblind(cls):
        if cls.ail_blind.active:
            raise CommandError("You are blind, you cannot see\n")

    @classmethod
    def chkdeaf(cls):
        if cls.ail_blind.active:
            raise CommandError()

    @classmethod
    def __wounded(cls, n):
        if Extras.my_lev > 9:
            return
        Extras.my_str -= n
        Extras.me_cal = 1
        if Extras.my_str >= 0:
            return
        closeworld()

        syslog("{} slain magically".format(Extras.globme))
        delpers(Extras.globme)
        Extras.zapped = True

        openworld()
        dumpitems()
        loseme()
        sendsys(
            Extras.globme,
            Extras.globme,
            -10000,
            Extras.curch,
            "{} has just died\n".format(Extras.globme),
        )
        sendsys(
            Extras.globme,
            Extras.globme,
            -10113,
            Extras.curch,
            "[ {} has just died ]\n".format(Extras.globme),
        )
        raise CrapupError("Oh dear you just died\n")

    @classmethod
    def __woundmn(cls, mon, am):
        a = Player(mon).strength - am
        Player(mon).strength = a

        if a >= 0:
            cls.__mhitplayer(mon)
        else:
            dumpstuff(mon, Player(mon).location)
            sendsys(
                "",
                "",
                -10000,
                Player(mon).location,
                "{} has just died\n".format(Player(mon).name),
            )
            Player(mon).name = ""
            sendsys(
                "",
                "",
                -10113,
                Player(mon).location,
                "[ {} has just died ]\n".format(Player(mon).name),
            )

    @classmethod
    def __mhitplayer(cls, mon):
        if Player(mon).location != Extras.curch:
            return
        if mon < 0 or mon > 47:
            return
        a = randperc()
        b = 3 * (15 - Extras.my_lev) + 20
        if Item(89).is_worn_by(Extras.mynum) or Item(113).is_worn_by(Extras.mynum) or Item(114).is_worn_by(Extras.mynum):
            b -= 10
        if a < b:
            data = [
                mon,
                randperc() % mon.damage,
                -1,
            ]
        else:
            data = [
                mon,
                -1,
                -1,
            ]
        sendsys(
            Extras.globme,
            Player(mon).name,
            -10021,
            Player(mon).location,
            data,
        )

    @classmethod
    def resetplayers(cls):
        for bot_id, bot in cls.__pinit:
            a = bot_id + 16
            Player(a).name = bot.name
            Player(a).location = bot.location
            Player(a).strength = bot.strength
            Player(a).sex = bot.sex
            Player(a).weapon = None
            Player(a).visible = 0
            Player(a).level = bot.level
        for a in range(35, 48):
            Player(a).name = ""

    @classmethod
    def wearcom(cls):
        a = cls.__ohereandget()
        if not iscarrby(a.item_id, Extras.mynum):
            raise CommandError("You are not carrying this\n")
        if a.is_worn_by(Extras.mynum):
            raise CommandError("You are wearing this\n")
        if (Item(89).is_worn_by(Extras.mynum) or Item(113).is_worn_by(Extras.mynum) or Item(114).is_worn_by(Extras.mynum)) \
                and (a.item_id == 89 or a.item_id == 113 or a.item_id == 114):
            raise CommandError("You can't use TWO shields at once...\n")
        if not a.can_wear:
            raise CommandError("Is this a new fashion ?\n")
        a.carry_flag = 2
        yield "OK\n"

    @classmethod
    def removecom(cls):
        a = cls.__ohereandget()
        if a.is_worn_by(Extras.mynum):
            raise CommandError("You are not wearing this\n")
        a.carry_flag = 1

    @classmethod
    def __addforce(cls, action):
        if cls.__forf:
            bprintf("The compulsion to {} is overridden\n".format(cls.__acfor))
        cls.__forf = True
        cls.__acfor = action

    @classmethod
    def __forchk(cls):
        cls.__is_force = True
        if cls.__forf:
            gamecom(cls.__acfor)
        cls.__is_force = False
        cls.__forf = False

    @classmethod
    def __iam(cls, x):
        a = x.lower()
        b = Extras.globme.lower()
        if a == b:
            return True
        if b[:4] == "the " and a == b[4:]:
            return True
        return False

    @classmethod
    def deafcom(cls):
        a = cls.__victim()
        sendsys(
            a.name,
            Extras.globme,
            -10120,
            Extras.curch,
            "",
        )

    @classmethod
    def blindcom(cls):
        a = cls.__victim()
        sendsys(
            a.name,
            Extras.globme,
            -10105,
            Extras.curch,
            "",
        )

    @classmethod
    def __teletrap(cls, newch):
        sendsys(
            Extras.globme,
            Extras.globme,
            -10000,
            Extras.curch,
            "\001s{name}\001{name} has left.\n\001".format(name=Extras.globme),
        )
        Extras.curch = newch
        sendsys(
            Extras.globme,
            Extras.globme,
            -10000,
            Extras.curch,
            "\001s{name}\001{name} has arrived.\n\001".format(name=Extras.globme),
        )
        trapch(Extras.curch)

    @classmethod
    def on_flee_event(cls):
        for ct in range(Extras.numobs):
            if iscarrby(ct, Extras.mynum) and not Item(ct).is_worn_by(Extras.mynum):
                Item(ct).setoloc(Player(Extras.mynum).location, 0)
