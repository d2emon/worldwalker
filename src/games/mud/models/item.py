class Item:
    FLAG_DESTROYED = 0
    FLAG_1 = 1
    FLAG_2 = 2
    FLAG_3 = 3
    FLAG_4 = 4
    FLAG_5 = 5
    FLAG_6 = 6
    # 7
    FLAG_8 = 8
    FLAG_9 = 9
    FLAG_10 = 10
    # 11
    FLAG_12 = 12
    FLAG_13 = 13
    FLAG_14 = 14
    FLAG_WEAPON = 15

    IN_CHANNEL = 0
    HELD = 1
    WORN = 2
    IN_ITEM = 3

    def __init__(self, **kwargs):
        self.item_id = kwargs.get('item_id')

        self.__location_id = kwargs.get('location_id', 0)
        # 1
        # 2
        self.__flags = kwargs.get('flags', {})
        self.__values = kwargs.get('values', {})
        self.__location_flag = kwargs.get('location_flag', self.IN_CHANNEL)

        # Static

        self.__name = kwargs.get('name', '')
        self.__descriptions = kwargs.get('descriptions', [])
        self.__max_state = kwargs.get('max_state', 0)
        self.__is_movable = kwargs.get('is_movable', True)
        self.__base_value = kwargs.get('base_value', 0)

    # World props

    @property
    def location_id(self):
        return self.__location_id

    @property
    def flags(self):
        return self.__flags

    @property
    def location_flag(self):
        return self.__location_flag

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

    # Readonly props

    @property
    def is_in_channel(self):
        return self.__location_flag == self.IN_CHANNEL

    @property
    def is_held(self):
        return self.__location_flag == self.HELD

    @property
    def is_worn(self):
        return self.__location_flag == self.WORN

    @property
    def is_carried(self):
        return self.is_held or self.is_worn

    @property
    def is_in_item(self):
        return self.__location_flag == self.IN_ITEM

    @property
    def is_destroyed(self):
        return self.get_flag(Item.FLAG_DESTROYED)

    # Class methods

    @classmethod
    def load(cls, item_id):
        """
        Load item from db

        :param item_id:
        :return:
        """
        # StaticItemData.load(item_id)
        return cls(item_id=item_id)

    @classmethod
    def by_mask(cls, **mask):
        items = []
        return any(i for i in items if i.has_mask(**mask))

    # Methods

    def set_location(self, location_id, location_flag):
        self.__location_id = location_id
        self.__location_flag = location_flag

    def set_location_channel(self, location_id):
        self.set_location(location_id, self.IN_CHANNEL)

    def set_location_held(self, location_id):
        self.set_location(location_id, self.HELD)

    def set_location_item(self, location_id):
        self.set_location(location_id, self.IN_ITEM)

    def get_flag(self, flag_id):
        # bit_fetch(items[4 * self.item_id + 2]),flag_id)
        return True

    def set_flag(self, flag_id, value):
        if value:
            # bit_set(&(items[4 * self.item_id + 2]),flag_id)
            self.__flags[flag_id] = True
        else:
            # bit_clear(&(items[4 * self.item_id + 2]),flag_id)
            self.__flags[flag_id] = False

    def get_value(self, value_id):
        # byte_fetch(&(items[4 * self.item_id + 2]),value_id)
        return 0

    def set_value(self, value_id, value):
        # byte_put(&(items[4 * self.item_id + 2]),value_id, value)
        self.__values[value_id] = value

    def get_description(self, state):
        return self.__descriptions[state]

    def available_for(self, user_id):
        # return is_here(self.item_id) or iscarrby(self, user_id)
        return True

    def create(self):
        self.set_flag(Item.FLAG_DESTROYED, False)

    def has_mask(self, **kwargs):
        is_here = True
        # is_here = iscarrby(item.item_id, my_num) or ishere(item.item_id, my_num)
        has_mask = all(self.__flags[k] == v for k, v in kwargs.items())
        return is_here and has_mask
