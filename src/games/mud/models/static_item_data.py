class StaticItemData:
    def __init__(self, **kwargs):
        self.item_id = kwargs.get('item_id')
        self.__name = kwargs.get('name', '')
        self.__descriptions = kwargs.get('descriptions', [])
        self.__max_state = kwargs.get('max_state', 0)
        self.__is_movable = kwargs.get('is_movable', True)
        self.__base_value = kwargs.get('base_value', 0)

    # Static props

    @property
    def name(self):
        return self.__name

    @property
    def descriptions(self):
        return self.__descriptions

    @property
    def max_state(self):
        return self.__max_state

    @property
    def is_movable(self):
        return self.__is_movable

    @property
    def base_value(self):
        return self.__base_value

    # Class methods

    @classmethod
    def load(cls, item_id):
        """
        Load item from db

        :param item_id:
        :return:
        """
        return cls(item_id=item_id)
