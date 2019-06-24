from .action import Action


class Help(Action):
    # 27
    commands = "help",

    @classmethod
    def action(cls, command, parser):
        name = next(parser)
        if word is not None:
            return parser.user.help(parser.user.find(name))

        return parser.user.show_help_message()
