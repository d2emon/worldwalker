from .model import Model


class Message(Model):
    items_count = None
    items = None

    offset = None
    length = 128

    @classmethod
    def model(cls):
        return {
            1: None,
            2: "",
        }

    @classmethod
    def load_message(cls, database, message_id):
        offset = message_id * 2 - database.load_start()
        return cls(message_id, database.read(offset, cls.length))

    def __init__(self, message_id, data):
        self.message_id = message_id
        self.data = data

    @property
    def code(self):
        return self.data[1]

    def __str__(self):
        return self.data[2]

    @property
    def is_special(self):
        return self.code < -3
