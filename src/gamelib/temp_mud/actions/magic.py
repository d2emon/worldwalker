from .action import Action


class DeletePlayer(Action):
    # 31
    commands = "delete",

    @classmethod
    def action(cls, command, parser):
        return parser.player.delete_player(parser.require_next("Who ?\n"))


class ChangePassword(Action):
    # 32
    commands = "pass", "password",

    @classmethod
    def action(cls, command, parser):
        return parser.player.change_password()


class Summon(Action):
    # 33
    commands = "summon",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("Summon who ?\n")

        item = Item.find(
            name,
            available=True,
            mode_0=True,
            destroyed=parser.user.is_wizard,
        )
        if item is not None:
            return parser.player.summon_item(item)

        player = parser.user.find(name)
        if player is None:
            raise CommandError("I dont know who that is\n")
        return parser.player.summon_player(player)
