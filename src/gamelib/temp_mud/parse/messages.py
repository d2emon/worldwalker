def send2(*args):
    raise NotImplementedError()


class Message:
    def __init__(self, send_to, send_from, code, channel, text):
        self.send_to = send_to
        self.send_from = send_from
        self.code = code
        self.channel = channel
        self.text = text

    def send(self):
        if self.code != -9900 and self.code != -10021:
            text = self.text
        else:
            text = self.text[:3]
        send_to = self.send_to.name if self.send_to is not None else ""
        send_from = self.send_from.name if self.send_from is not None else ""
        send2([
            self.channel,
            self.code,
            "{}.{}.".format(send_to, send_from),
            text,
        ])


