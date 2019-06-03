MSG_GLOBAL = -10000
MSG_WEATHER = -10030


class Message:
    @classmethod
    def send(cls, user_from, user_to, code, channel_id, message):
        raise NotImplementedError()
