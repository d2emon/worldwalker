from ..message import Message
from ..world import World
from .action import Special


class StartGame(Special):
    @classmethod
    def action(cls, parser, user):
        parser.mode = parser.MODE_GAME

        user.reset_location_id()
        user.initme()

        World.load()
        visible = 0 if not user.is_god else 10000
        user.player.start(user.NewUaf.strength, user.NewUaf.level, visible, user.NewUaf.sex)

        user.send_message(
            user,
            Message.WIZARD,
            user.location_id,
            "\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=user),
        )

        yield from parser.read_messages()
        user.reset_location_id(True)
        user.go_to_channel(user.location_id)

        user.send_message(
            user,
            Message.GLOBAL,
            user.location_id,
            "\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=user),
        )
