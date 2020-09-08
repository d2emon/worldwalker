from .action import Action, Spell


class Wear(Action):
    # 100
    commands = "wear",

    @classmethod
    def action(cls, command, parser):
        item = parser.get_item()
        return parser.user.wear(item)


class Remove(Action):
    # 101
    commands = "remove",

    @classmethod
    def action(cls, command, parser):
        item = parser.get_item()
        return parser.user.remove_clothes(item)


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

        container = parser.user.get_item(container_name)
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


class Force(Spell):
    # 109
    commands = "force",

    @classmethod
    def cast(cls, parser, target):
        return parser.user.force(target, parser.full())


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
        item = parser.user.get_item(parser.require_next("Push what ?\n"))
        return parser.user.push(item)


class Cripple(Spell):
    # 118
    commands = "cripple",

    @classmethod
    def cast(cls, parser, target):
        return parser.user.cripple(target)


class Cure(Spell):
    # 119
    commands = "cure",
    reflect = True

    @classmethod
    def cast(cls, parser, target):
        return parser.user.cure(target)


class Dumb(Spell):
    # 120
    commands = "dumb",

    @classmethod
    def cast(cls, parser, target):
        return parser.user.dumb(target)


class Change(Spell):
    # 121
    commands = "change",

    @classmethod
    def cast(cls, parser, target):
        return parser.user.change(target)

    @classmethod
    def action(cls, command, parser):
        word = parser.require_next("change what (Sex ?) ?\n")
        if word != 'sex':
            raise CommandError("I don't know how to change that\n")
        return super().action(command, parser)


class Missile(Spell):
    # 122
    commands = "missile",
    reflect = True

    @classmethod
    def cast(cls, parser, target):
        return parser.user.missile(target)


class Shock(Spell):
    # 123
    commands = "shock",
    reflect = True

    @classmethod
    def cast(cls, parser, target):
        return parser.user.shock(target)


class Fireball(Spell):
    # 124
    commands = "fireball",
    reflect = True

    @classmethod
    def cast(cls, parser, target):
        return parser.user.fireball(target)


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
        return parser.user.kiss(parser.get_target())


class Hug(Action):
    # 129
    commands = "hug",

    @classmethod
    def action(cls, command, parser):
        return parser.user.hug(parser.get_target())


class Slap(Action):
    # 130
    commands = "slap",

    @classmethod
    def action(cls, command, parser):
        return parser.user.slap(parser.get_target())


class Tickle(Action):
    # 131
    commands = "tickle",

    @classmethod
    def action(cls, command, parser):
        return parser.user.tickle(parser.get_target())


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
        return parser.user.stare(parser.get_target())


class Grope(Action):
    # 139
    commands = "grope",

    @classmethod
    def action(cls, command, parser):
        return parser.user.grope(parser.get_target())


class Deaf(Spell):
    # 148
    commands = "deafen",

    @classmethod
    def cast(cls, parser, target):
        return parser.user.deafen(target)


class Squeeze(Action):
    # 154
    commands = "squeeze",

    @classmethod
    def action(cls, command, parser):
        return parser.user.squeeze(parser.get_target())


class Cuddle(Action):
    # 166
    commands = "cuddle",

    @classmethod
    def action(cls, command, parser):
        return parser.user.cuddle(parser.get_target())


class Blind(Spell):
    # 178
    commands = "blind",

    @classmethod
    def cast(cls, parser, target):
        return parser.user.blind(target)
