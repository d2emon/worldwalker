from .action import Action


class Frobnicate(Action):
    # 182
    commands = "frobnicate",

    @classmethod
    def action(cls, command, parser):
        target = parser.user.find(parser.require_next("Frobnicate who ?\n"))
        return parser.user.frobnicate(target)
