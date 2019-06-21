from .action import Action


class Crash(Action):
    # 137
    commands = "crash",

    @classmethod
    def action(cls, command, parser):
        return parser.user.crash()


class Sing(Action):
    # 138
    commands = "crash",

    @classmethod
    def action(cls, command, parser):
        return parser.user.sing()


class Spray(Action):
    # 140
    commands = "spray",

    @classmethod
    def action(cls, command, parser):
        target = parser.get_target()
        item_name = parser.require_next("With what ?\n")
        if item_name == "with":
            item_name = parser.require_next("With what ?\n")
        item = Item.find(
            item_name,
            available=True,
            destroyed=parser.user.is_wizard,
        )
        return parser.user.spray(item, target)


class Directory(Action):
    # 143
    commands = "directory",

    @classmethod
    def action(cls, command, parser):
        return parser.user.directory()
