from ..errors import CrapupError, ServiceError
from ..message.message import Message
from ..message.process import handle
from ..world import World


class Reader:
    def __init__(self):
        self.__position = -1
        self.force_read = False

        self.before_message = lambda message: None

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    def reset_position(self):
        raise NotImplementedError()

    # Tk
    def __get_messages(self):
        try:
            World.load()
            return Message.messages(self.position)
        except ServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def read_messages(self, unique=False, reset_after_read=False):
        if unique and self.force_read:
            return

        for message in self.__get_messages():
            yield from self.before_message(message)
            yield from handle(self, message)

        yield from self.on_messages()

        if reset_after_read:
            self.reset_position()

        World.save()
        if unique:
            self.force_read = False

    # Events
    def on_messages(self):
        pass
