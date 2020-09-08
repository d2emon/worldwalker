class WorldService:
    __objinfo = []

    @classmethod
    def get_item(cls, **kwargs):
        item_id = kwargs.get('item_id')
        return cls.__objinfo[item_id]
