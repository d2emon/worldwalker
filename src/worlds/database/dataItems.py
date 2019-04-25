class DataItem:
    def __init__(self, item_id, text):
        self.item_id = item_id
        self.__text = text

    def __str__(self):
        return self.__text


class LengthItem:
    cm2inch = .393701

    def __init__(self, value):
        self.__value = value

    @property
    def cm(self):
        return self.__value

    @property
    def inches(self):
        return int(self.__value * self.cm2inch)
