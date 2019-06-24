from .action import Action


class Levels(Action):
    # 26
    commands = "levels",

    @classmethod
    def action(cls, command, parser):
        return parser.user.levels()


class Help(Action):
    # 27
    commands = "help",

    @classmethod
    def action(cls, command, parser):
        name = next(parser)
        if word is not None:
            return parser.user.help(parser.user.find(name))

        return parser.user.show_help_message()


class Value(Action):
    # 28
    commands = "value",

    @classmethod
    def action(cls, command, parser):
        item = Item.find(
            parser.require_next("Value what ?\n"),
            available=True,
            destroyed=parser.user.is_wizard,
        )
        return parser.user.value(item)
