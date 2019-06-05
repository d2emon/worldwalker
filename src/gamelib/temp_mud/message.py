from .errors import ServiceError,LooseError
from .player import Player
from .world import World


MAX_MESSAGES = 199

MSG_BROADCAST = -1
MSG_GLOBAL = -10000
MSG_WEATHER = -10030
MSG_WIZARD = -10113


class Message:
    def __init__(self, user_to, user_from, code, channel_id, message):
        self.message_id = None
        self.channel_id = channel_id
        self.code = code
        self.user_to = user_to
        self.user_from = user_from
        self.message = message

    @classmethod
    def load(cls, message_id):
        return World.get_message(message_id)

    def save(self):
        self.message_id = World.add_message(self)
        return self.message_id

    @classmethod
    def messages(cls, first=None, last=None):
        return World.get_messages(first, last)

    def serialize(self):
        return [
            self.channel_id,
            self.code,
            [self.user_to, self.user_from],
            self.message,
        ]

    def send(self, user):
        try:
            World.load()
            message_id = self.save()
            if message_id >= MAX_MESSAGES:
                self.cleanup(user)
                autochange_weather(user)
        except ServiceError:
            raise LooseError("\nAberMUD: FILE_ACCESS : Access failed\n")

    @classmethod
    def cleanup(cls, user):
        for player in cls.__revise(World.clear_old_messages()):
            Broadcast("{} has been timed out\n".format(player)).send(user)

    @classmethod
    def __revise(cls, timeout):
        World.load()
        for player in Player.get_timed_out(timeout):
            yield player
            player.timeout_death()


class Broadcast(Message):
    def __init__(self, message):
        super().__init__(
            None,
            None,
            MSG_BROADCAST,
            None,
            message,
        )


class Silly(Message):
    def __init__(self, user, message):
        super().__init__(
            user,
            user,
            MSG_GLOBAL,
            user.location.location_id,
            message.format(user),
        )
