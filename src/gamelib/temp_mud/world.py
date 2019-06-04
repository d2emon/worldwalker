class World:
    objects = []
    objinfo = []
    item_ids = len(objects)

    ublock = []
    player_ids = len(ublock)

    first_message = 0
    last_message = 0
    __messages = []

    @classmethod
    def load(cls):
        raise NotImplementedError()

    @classmethod
    def save(cls):
        raise NotImplementedError()

    @classmethod
    def get_message_id(cls, message_id):
        return 2 * message_id - cls.first_message

    @classmethod
    def get_message(cls, message_id):
        return cls.__messages[cls.get_message_id(message_id)]

    @classmethod
    def add_message(cls, message):
        message_id = cls.get_message_id(cls.last_message)
        cls.__messages[message_id] = message
        cls.last_message += 1
        return message_id

    @classmethod
    def get_messages(cls, first=None, last=None):
        if last is None:
            last = cls.last_message
        if first is None:
            first = last

        for message_id in range(first, last):
            yield cls.get_message(message_id)

    @classmethod
    def cleanup(cls):
        cls.load()
        for i in range(100):
            cls.__messages[i] = cls.__messages[100 + i]
        cls.first_message += 100
        return cls.first_message
