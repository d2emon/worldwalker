from .action import Special


class StartGame(Special):
    @classmethod
    def action(cls, command, parser):
        return parser.user.start()
