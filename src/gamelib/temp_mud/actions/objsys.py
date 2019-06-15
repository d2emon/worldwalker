from ..item import Item
from .action import Action


class Take(Action):
    # 9
    commands = "get", "take",

    @classmethod
    def action(cls, command, parser):
        item_name = parser.require_next("Get what ?\n")
        item = Item.find(
            item_name,
            here=True,
            destroyed=parser.user.is_wizard,
        )
        container = None
        word = next(parser)
        if word is not None and word == "from" or word == "out":
            container = Item.find(
                parser.require_next("From what ?\n"),
                available=True,
                destroyed=parser.user.is_wizard,
            )
            if container is None:
                raise CommandError("You can't take things from that - it's not here\n")
            item = Item.find(
                item_name,
                container=container,
                destroyed=parser.user.is_wizard,
            )

        return parser.user.take(item, container)


class Drop(Action):
    # 10
    commands = "drop",

    @classmethod
    def action(cls, command, parser):
        item_name = parser.require_next("Drop what ?\n")
        item = Item.find(
            item_name,
            owner=parser.user,
            destroyed=parser.user.is_wizard,
        )
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
