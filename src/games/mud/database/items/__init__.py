class Item:
    items = []

    @classmethod
    def find_by_name(cls, name):
        search = name.lower()
        for item in cls.items:
            if item.name == search:
                return item
        return None
