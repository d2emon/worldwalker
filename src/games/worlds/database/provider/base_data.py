class BaseDataProvider:
    item_class = None

    def by_value(self, value):
        return self.item_class(value) if self.item_class is not None else value

    def __next__(self):
        raise NotImplementedError
