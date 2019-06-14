from .action import Action


class Inventory(Action):
    # 12
    commands = "i", "inv", "inventory",

    @classmethod
    def action(cls, command, parser):
        parser.user.inventory()
