from ..errors import CrapupError, ServiceError
from ..message.message import Message
from ..message.process import handle
from ..world import World


class Reader:
    def __init__(self):
        self.force_read = False

        self.before_message = lambda message: None

    @property
    def message_id(self):
        raise NotImplementedError()

    @message_id.setter
    def message_id(self, value):
        raise NotImplementedError()

    def reset_position(self):
        raise NotImplementedError()

    # Tk
    def __get_messages(self):
        try:
            World.load()
            return Message.messages(self.message_id)
        except ServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def read_messages(self, unique=False, reset_after_read=False, **kwargs):
        if unique and self.force_read:
            return

        for message in self.__get_messages():
            yield from self.before_message(message)
            yield from handle(self, message)

        yield from self.on_messages(**kwargs)

        if reset_after_read:
            self.reset_position()

        World.save()
        if unique:
            self.force_read = False

    # Events
    def on_messages(self, **kwargs):
        pass
