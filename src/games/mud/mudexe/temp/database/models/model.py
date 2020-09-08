class Model:
    items_count = 255

    @classmethod
    def model(cls):
        return None

    @classmethod
    def load(cls, database):
        cls.items = [cls.model() for _ in range(cls.items_count)]
