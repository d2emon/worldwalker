class DataItem:
    def __init__(self, item_id, value):
        self.item_id = item_id
        self.value = value

    def __str__(self):
        return self.value
