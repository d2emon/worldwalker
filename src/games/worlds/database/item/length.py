from .data import DataItem


class LengthItem(DataItem):
    cm2inch = .393701

    def __init__(self, value):
        super().__init__(None, value)

    @property
    def cm(self):
        return int(self.value)

    @property
    def inches(self):
        return int(self.value * self.cm2inch)

    def __str__(self):
        return str(self.cm)
