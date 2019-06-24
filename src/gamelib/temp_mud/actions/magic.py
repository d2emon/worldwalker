from .action import Action


class DeletePlayer(Action):
    # 31
    commands = "delete",

    @classmethod
    def action(cls, command, parser):
        return parser.user.delete_player(parser.require_next("Who ?\n"))


class ChangePassword(Action):
    # 32
    commands = "pass", "password",

    @classmethod
    def action(cls, command, parser):
        return parser.user.change_password()


class Summon(Action):
    # 33
    commands = "summon",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("Summon who ?\n")

        item = parser.user.get_item(name, mode_0=True)
        if item is not None:
            return parser.user.summon_item(item)

        player = parser.user.find(name)
        if player is None:
            raise CommandError("I dont know who that is\n")
        return parser.user.summon_player(player)


class GoToLocation(Action):
    # 66
    commands = "goto",

    @classmethod
    def action(cls, command, parser):
        zone = parser.require_next("Go where ?\n")
        location_id = next(parser)
        return parser.user.go_to_location(zone, location_id)


class BecomeInvisible(Action):
    # 114
    commands = "invisible",

    @classmethod
    def action(cls, command, parser):
        return parser.user.become_invisible(int(next(parser)))


class BecomeVisible(Action):
    # 115
    commands = "visible",

    @classmethod
    def action(cls, command, parser):
        return parser.user.become_visible()


class Wizards(Action):
    # 134
    commands = "wiz",

    @classmethod
    def action(cls, command, parser):
        return parser.user.wizards(parser.full())


class Ressurect(Action):
    # 149
    commands = "resurrect",

    @classmethod
    def action(cls, command, parser):
        item = parser.user.get_item(parser.require_next("Yes but what ?\n"), mode_0=True)
        return parser.user.ressurect(item)
