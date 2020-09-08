from .action import Action


class Exits(Action):
    # 136
    commands = "exits",

    @classmethod
    def action(cls, command, parser):
        parser.user.list_exits()


class Loc(Action):
    # 153
    commands = "loc",

    @classmethod
    def action(cls, command, parser):
        parser.user.list_nodes()
