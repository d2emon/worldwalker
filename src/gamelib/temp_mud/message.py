from .world import World


MSG_BROADCAST = -1
MSG_GLOBAL = -10000
MSG_WEATHER = -10030
MSG_WIZARD = -10113


class Message:
    def __init__(self, user_from, user_to, code, channel_id, message):
        self.user_from = user_from
        self.user_to = user_to
        self.code = code
        self.channel_id = channel_id
        self.message = message

    @classmethod
    def send(cls, user_from, user_to, code, channel_id, message):
        raise NotImplementedError()

    @classmethod
    def load(cls, message_id):
        return World.get_message(message_id)

    def save(self):
        return World.add_message(self)

    @classmethod
    def messages(cls, first=None, last=None):
        return World.get_messages(first, last)
