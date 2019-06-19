from .action import Action


class Put(Action):
    # 102
    commands = "put",

    @classmethod
    def action(cls, command, parser):
        item = parser.get_item()

        container_name = next(parser)
        if container_name is None:
            raise CommandError("where ?\n")
        if container_name in ['on', 'in']:
            container_name = next(parser)
        if container_name is None:
            raise CommandError("What ?\n")

        container = Item.find(
            container_name,
            available=True,
            destroyed=parser.user.is_wizard,
        )
        return parser.user.put(item, container)


class Wave(Action):
    # 103
    commands = "wave",

    @classmethod
    def action(cls, command, parser):
        return parser.user.wave(parser.get_item())


class Open(Action):
    # 105
    commands = "open",

    @classmethod
    def action(cls, command, parser):
        return parser.user.open(parser.get_item())


class Close(Action):
    # 106
    commands = "close", "shut",

    @classmethod
    def action(cls, command, parser):
        return parser.user.close(parser.get_item())


class Lock(Action):
    # 107
    commands = "lock",

    @classmethod
    def action(cls, command, parser):
        return parser.user.lock(parser.get_item())


class Unlock(Action):
    # 108
    commands = "unlock",

    @classmethod
    def action(cls, command, parser):
        return parser.user.unlock(parser.get_item())


class Force(Action):
    # 109
    commands = "force",

    @classmethod
    def action(cls, command, parser):
        return parser.user.force(parser.victim_magic(), parser.full())


class Light(Action):
    # 110
    commands = "light",

    @classmethod
    def action(cls, command, parser):
        return parser.user.light(parser.get_item())


class Extinguish(Action):
    # 111
    commands = "extinguish",

    @classmethod
    def action(cls, command, parser):
        return parser.user.extinguish(parser.get_item())


class Push(Action):
    # 117
    commands = "turn", "pull", "press", "push",

    @classmethod
    def action(cls, command, parser):
        item = Item.find(
            parser.require_next("Push what ?\n"),
            available=True,
            destroyed=parser.user.is_wizard,
        )
        return parser.user.push(item)


class Cripple(Action):
    # 118
    commands = "cripple",

    @classmethod
    def action(cls, command, parser):
        return parser.user.cripple(parser.victim_magic())


class Cure(Action):
    # 119
    commands = "cure",

    @classmethod
    def action(cls, command, parser):
        return parser.user.cure(parser.victim_magic_is_here())


class Dumb(Action):
    # 120
    commands = "dumb",

    @classmethod
    def action(cls, command, parser):
        return parser.user.dumb(parser.victim_magic())


class Missile(Action):
    # 122
    commands = "missile",

    @classmethod
    def action(cls, command, parser):
        return parser.user.missile(parser.victim_magic_is_here())


class Blow(Action):
    # 126
    commands = "blow",

    @classmethod
    def action(cls, command, parser):
        return parser.user.blow(parser.get_item())


class Sigh(Action):
    # 127
    commands = "sigh",

    @classmethod
    def action(cls, command, parser):
        return parser.user.sigh()


class Scream(Action):
    # 132
    commands = "scream",

    @classmethod
    def action(cls, command, parser):
        return parser.user.scream()


class Bounce(Action):
    # 133
    commands = "bounce",

    @classmethod
    def action(cls, command, parser):
        return parser.user.bounce()


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
