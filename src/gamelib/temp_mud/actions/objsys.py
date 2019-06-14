from ..item import Item
from .action import Action


class Take(Action):
    # 9
    commands = "get", "take",

    @classmethod
    def action(cls, command, parser):
        item_name = parser.require_next("Get what ?\n")
        item = Item.fobnh(item_name)

        container = None
        word = next(parser)
        if word is not None and word == "from" or word == "out":
            container = Item.fobna(parser.require_next("From what ?\n"))
            if container is None:
                raise CommandError("You can't take things from that - it's not here\n")
            item = Item.fobnin(item_name, container)

        return parser.user.take(item, container)


class Drop(Action):
    # 10
    commands = "drop",

    @classmethod
    def action(cls, command, parser):
        item_name = parser.require_next("Drop what ?\n")
        item = Item.fobnc(item_name)
        return parser.user.drop(item)


class Inventory(Action):
    # 12
    commands = "i", "inv", "inventory",

    @classmethod
    def action(cls, command, parser):
        return parser.user.inventory()


class Who(Action):
    # 13
    commands = "who",

    @classmethod
    def action(cls, command, parser):
        return parser.user.who()


class Users(Action):
    # 155
    commands = "users",

    @classmethod
    def action(cls, command, parser):
        return parser.user.who(users=True)
