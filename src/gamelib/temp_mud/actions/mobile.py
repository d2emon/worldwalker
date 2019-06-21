from .action import Action


class Crash(Action):
    # 137
    commands = "crash",

    @classmethod
    def action(cls, command, parser):
        return parser.user.crash()
