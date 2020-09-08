class Message:
    messages = []
    first_id = 0
    last_id = 0

    def __init__(self):
        self.code = 0
        self.text = ""

    def __str__(self):
        return self.text

    def mstoout(self, user):
        # Print appropriate stuff from data block
        if DummyGlobals.debug_mode:
            bprintf("\n<{}>".format(self.code))

        if self.is_special:
            sysctrl(self, str(user).lower())
        else:
            bprintf(str(self))

    @property
    def is_special(self):
        return self.code < -3

    @classmethod
    def get(cls, message_id):
        offset = message_id * 2 - cls.first_id
        print("Message #{}".format(offset))
        return cls.messages[message_id]

    @classmethod
    def select(cls, first_id, last_id):
        return cls.messages[first_id:last_id]
