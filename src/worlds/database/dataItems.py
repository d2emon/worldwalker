class DataItem:
    def __init__(self, item_id, value):
        self.item_id = item_id
        self.value = value

    def __str__(self):
        return self.value


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
