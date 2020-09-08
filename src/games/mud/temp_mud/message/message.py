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
from ..services.messages import MessagesService
from . import message_codes


class Message:
    def __init__(self, user_to, user_from, code, channel_id, message):
        self.message_id = None
        self.channel_id = channel_id
        self.code = code
        self.user_to = user_to
        self.user_from = user_from
        self.message = message

    # Parser
    @classmethod
    def __deserialize(cls, channel_id, code, users, message):
        return cls(
            users[1],
            users[0],
            code,
            channel_id,
            message
        )

    def __serialize(self):
        return [
            self.channel_id,
            self.code,
            [self.user_to, self.user_from],
            self.message,
        ]

    @classmethod
    def __on_overflow(cls, first_message_id):
        # World.load()
        # for player in Player.get_timed_out(first_message_id):
        #     Broadcast("{} has been timed out\n".format(player)).send()
        #     player.timeout_death()

        # user.location.weather.autochange(user)
        # next(Weather())
        pass

    @classmethod
    def load(cls, message_id):
        return cls.__deserialize(*MessagesService.get(
            message_id=message_id,
        ).get('message'))

    # Tk
    @classmethod
    def messages(cls, first=None, last=None):
        return cls.__deserialize(*MessagesService.get(
            first=first,
            last=last,
        ).get('message'))

    def send(self):
        result = MessagesService.post(
            message=self.__serialize(),
        )
        self.message_id = result.get('message_id')
        if result.get('overflow', False):
            self.__on_overflow(result.get('first_message_id'))
        return self.message_id


class Broadcast(Message):
    def __init__(self, message):
        super().__init__(
            None,
            None,
            message_codes.BROADCAST,
            None,
            message,
        )


class Silly(Message):
    def __init__(self, user, message):
        super().__init__(
            user,
            user,
            message_codes.GLOBAL,
            user.location.location_id,
            message.format(user),
        )
