from ..message import message_codes
from ..message.message import Message, Broadcast, Silly


class Sender:
    @property
    def location(self):
        raise NotImplementedError()

    # Tk
    def send_message(self, to_user, code, channel_id, message):
        Message(to_user, self, code, channel_id, message).send(self)

    def broadcast(self, message):
        Broadcast(message).send(self)

    # Unknown
    def communicate(self, code, message, target=None):
        target = target or self
        self.send_message(
            target,
            code,
            self.location,
            message,
        )

    def send_exorcise(self, target):
        self.send_message(
            target,
            message_codes.EXORCISE,
            self.location,
            None,
        )

    def send_flee(self):
        self.send_message(
            self,
            message_codes.FLEE,
            self.location,
            None,
        )

    def send_global(self, message):
        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location,
            message,
        )

    def send_magic(self, target, code, message=None):
        self.send_message(
            target,
            code,
            target.location,
            message,
        )

    def send_personal(self, target, message):
        self.send_message(
            target,
            message_codes.PERSONAL,
            self.location,
            message,
        )

    def send_wizard(self, message):
        self.send_message(
            self,
            message_codes.WIZARD,
            None,
            message,
        )

    # Weather
    def send_silly(self, message):
        Silly(self, message).send(self)
