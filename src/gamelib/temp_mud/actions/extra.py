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


class Where(Action):
    # 112
    commands = "where",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("What is that ?\n")
        return parser.user.where(name)


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


class Patch(Action):
    # 179
    commands = "patch",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("Must Specify Player or Object\n")
        if name == "player":
            player = Player(parser.get_number(max_value=47))
            value_id = parser.get_number(max_value=15)
            return parser.user.patch(player=player, value_id=value_id, value=parser.get_number())
        elif name == "object":
            item = Item(parser.get_number(max_value=len(ITEMS) - 1))
            value_id = parser.get_number(max_value=3)
            return parser.user.patch(item=item, value_id=value_id, value=parser.get_number())
        else:
            raise CommandError("Must specify Player or Object\n")


class Smoke(Light):
    pass
