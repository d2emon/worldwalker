MSG_GLOBAL = -10000
MSG_WEATHER = -10030


class Message:
    @classmethod
    def send(cls, user_from, user_to, code, channel_id, message):
        raise NotImplementedError()

    @classmethod
    def get_message_data(cls, world):
        return world[0]

    @classmethod
    def get_position(cls, world, message_id):
        return 2 * message_id - cls.first(world)

    @classmethod
    def read(cls, world, message_id):
        return world[cls.get_position(world, message_id)]

    def send2(self, world):
        message_id = self.get_position(world, self.last(world))
        message_data = self.get_message_data(world)
        message_data[1] += 1

        world[message_id] = self
        world[0] = message_data

        return message_id

    @classmethod
    def read_all(cls, world, message_id):
        last_message_id = cls.last(world)
        if message_id is None:
            message_id = last_message_id

        for message_id in range(message_id, last_message_id):
            yield Message.read(world, message_id)

    @classmethod
    def first(cls, world):
        return cls.get_message_data(world)[0]

    @classmethod
    def last(cls, world):
        return cls.get_message_data(world)[1]
