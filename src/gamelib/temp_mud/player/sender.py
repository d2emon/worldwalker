from ..message import message_codes
from ..message.message import Message, Broadcast, Silly


class Sender:
    @property
    def location(self):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def visible(self):
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

    def send_change_sex(self, target):
        self.send_message(
            target,
            message_codes.CHANGE_SEX,
            self.location,
            None,
        )

    def send_evil(self):
        self.send_message(
            None,
            message_codes.TOO_EVIL,
            None,
            None,
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

    def send_magic_missile(self, target, code, power):
        self.send_message(
            target,
            code,
            self.location,
            power,
        )

    def send_personal(self, target, message):
        self.send_message(
            target,
            message_codes.PERSONAL,
            self.location,
            message,
        )

    def send_snoop(self, target, snoop):
        if target is None:
            return
        self.send_message(
            target,
            message_codes.START_SNOOP if snoop else message_codes.STOP_SNOOP,
            None,
            None,
        )

    def send_social(self, target, message):
        if message[:4] == "star":
            message = "\001s{name}\001{name} {message}\n\001".format(name=self.name, message=message)
        else:
            message = "\001p{name}\001 {message}\n\001".format(name=self.name, message=message)
        self.send_message(
            target,
            message_codes.SOCIAL,
            self.location,
            message,
        )

    def send_stats(self, target, stats):
        self.send_message(
            target,
            message_codes.CHANGE_STATS,
            None,
            stats,
        )

    def send_summon(self, target):
        self.send_message(
            target,
            message_codes.DEAF,
            self.location,
            None,
        )

    def send_visible(self):
        self.send_message(
            None,
            message_codes.VISIBLE,
            None,
            [
                self,
                self.visible,
            ],
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
