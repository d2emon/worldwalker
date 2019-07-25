from ..message.message import Message
from ..message.process import handle
from ..world import World


class Reader:
    def __init__(self):
        self.force_read = False

    @property
    def message_id(self):
        raise NotImplementedError()

    @message_id.setter
    def message_id(self, value):
        raise NotImplementedError()

    def reset_position(self):
        self.message_id = -1

    # Tk
    def read_messages(self, unique=False, reset_after_read=False, **kwargs):
        if unique and self.force_read:
            return

        for message in Message.messages(self.message_id):
            yield from self.on_message(message)

        yield from self.on_messages(**kwargs)

        if reset_after_read:
            self.reset_position()

        World.save()
        if unique:
            self.force_read = False

    # Events
    def on_message(self, message):
        return handle(self, message)

    def on_messages(self, **kwargs):
        pass
