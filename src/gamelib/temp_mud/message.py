"""
Data format for mud packets

Sector 0
[64 words]
0   Current first message pointer
1   Control Word
Sectors 1-n  in pairs ie [128 words]

[channel][controlword][text data]

[controlword]
0 = Text
-1 = general request
"""
from .errors import ServiceError, LooseError
from .player import Player
from .world import World


MAX_MESSAGES = 199


class Message:
    BROADCAST = -1
    STOP_SNOOP = -400
    START_SNOOP = -401
    CHANGE_STATS = -599
    TOO_EVIL = -666
    MSG_750 = -750
    VISIBLE = -9900
    GLOBAL = -10000
    MSG_10001 = -10001
    MSG_10002 = -10002
    MSG_10003 = -10003
    MSG_10004 = -10004
    MSG_10010 = -10010
    MSG_10011 = -10011
    MSG_10020 = -10020
    MSG_10021 = -10021
    WEATHER = -10030
    WIZARD = -10113
    FLEE = - 20000

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

    # Tk
    @classmethod
    def messages(cls, first=None, last=None):
        return World.get_messages(first, last)

    @classmethod
    def cleanup(cls, user):
        World.load()
        for player in Player.get_timed_out(World.clear_old_messages()):
            user.broadcast("{} has been timed out\n".format(player))
            player.timeout_death()

    def send(self, user):
        try:
            World.load()
            message_id = self.save()
            if message_id >= MAX_MESSAGES:
                self.cleanup(user)
                autochange_weather(user)
        except ServiceError:
            raise LooseError("\nAberMUD: FILE_ACCESS : Access failed\n")

    # Parser
    def serialize(self):
        return [
            self.channel_id,
            self.code,
            [self.user_to, self.user_from],
            self.message,
        ]

    def is_my(self, name):
        name = name.lower()
        user_to = self.user_to.lower()
        if user_to == name:
            return True
        if user_to[:4] == "the " and user_to[4:] == name:
            return True
        return False


class Broadcast(Message):
    def __init__(self, message):
        super().__init__(
            None,
            None,
            self.BROADCAST,
            None,
            message,
        )


class Silly(Message):
    def __init__(self, user, message):
        super().__init__(
            user,
            user,
            self.GLOBAL,
            user.location.location_id,
            message.format(user),
        )
