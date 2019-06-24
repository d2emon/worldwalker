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


class Stats(Action):
    # 29
    commands = "stats",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("STATS what ?\n")
        item = Item.find(
            name,
            available=True,
            mode_0=True,
            destroyed=parser.user.is_wizard,
        )
        if item is None:
            player = parser.user.find(name)
            return parser.user.player_stats(player)
        return parser.user.item_stats(item)


class Examine(Action):
    # 30
    commands = "examine", "read",

    @classmethod
    def action(cls, command, parser):
        item = Item.find(
            parser.require_next("Examine what ?\n"),
            available=True,
            destroyed=parser.user.is_wizard,
        )
        return parser.user.examine(item)


class ListWizards(Action):
    # 145
    commands = "wizlist",

    @classmethod
    def action(cls, command, parser):
        return parser.user.list_wizards()


class InCommand(Action):
    # 146
    commands = "in",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("In where ?\n")
        offset = parser.require_next("In where ?\n")
        location = Location.find(parser.user, name, offset)
        return parser.user.in_command(location, parser.full())


class Jump(Action):
    # 172
    commands = "jump",

    @classmethod
    def action(cls, command, parser):
        return parser.user.jump()


class Smoke(Light):
    pass
