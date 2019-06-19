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


class Change(Action):
    # 121
    commands = "change",

    @classmethod
    def action(cls, command, parser):
        word = parser.require_next("change what (Sex ?) ?\n")
        if word != 'sex':
            raise CommandError("I don't know how to change that\n")
        return parser.user.change(parser.victim_magic())


class Missile(Action):
    # 122
    commands = "missile",

    @classmethod
    def action(cls, command, parser):
        return parser.user.missile(parser.victim_magic_is_here())


class Shock(Action):
    # 123
    commands = "shock",

    @classmethod
    def action(cls, command, parser):
        return parser.user.shock(parser.victim_magic_is_here())


class Fireball(Action):
    # 124
    commands = "fireball",

    @classmethod
    def action(cls, command, parser):
        return parser.user.fireball(parser.victim_magic_is_here())


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


class Kiss(Action):
    # 128
    commands = "kiss",

    @classmethod
    def action(cls, command, parser):
        return parser.user.kiss(parser.victim_is_here)


class Hug(Action):
    # 129
    commands = "hug",

    @classmethod
    def action(cls, command, parser):
        return parser.user.hug(parser.victim_is_here)


class Slap(Action):
    # 130
    commands = "slap",

    @classmethod
    def action(cls, command, parser):
        return parser.user.slap(parser.victim_is_here)


class Tickle(Action):
    # 131
    commands = "tickle",

    @classmethod
    def action(cls, command, parser):
        return parser.user.tickle(parser.victim_is_here)


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


class Stare(Action):
    # 135
    commands = "stare",

    @classmethod
    def action(cls, command, parser):
        return parser.user.stare(parser.victim_is_here)


class Grope(Action):
    # 139
    commands = "grope",

    @classmethod
    def action(cls, command, parser):
        return parser.user.grope(parser.victim_is_here)


class Squeeze(Action):
    # 154
    commands = "squeeze",

    @classmethod
    def action(cls, command, parser):
        return parser.user.squeeze(parser.victim_is_here)


class Cuddle(Action):
    # 166
    commands = "cuddle",

    @classmethod
    def action(cls, command, parser):
        return parser.user.cuddle(parser.victim_is_here)


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
