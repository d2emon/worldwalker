from .action import Action


class Log(Action):
    # 150
    commands = "log",

    @classmethod
    def action(cls, command, parser):
        return parser.user.log()


class Snoop(Action):
    # 162
    commands = "snoop",

    @classmethod
    def action(cls, command, parser):
        name = next(parser)
        if name is None:
            target = None
        else:
            target = parser.user.find(name)
            if target is None:
                raise CommandError("Who is that ?\n")
        return parser.user.snoop(target)
