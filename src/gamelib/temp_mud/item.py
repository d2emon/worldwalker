from .errors import CommandError
from .player import Player
from .world import World


"""
Objects held in format

[Short Text]
[4 Long texts]
[Max State]


Objects in text file in form

Stam:state:loc:flag
"""


class Item:
    CARRY_0 = 0
    CARRY_1 = 1
    WEARING = 2
    IN_CONTAINER = 3

    def __init__(self, item_id):
        self.item_id = item_id

    @classmethod
    def items(cls):
        return (Item(item_id) for item_id in range(World.item_ids))

    @property
    def __object(self):
        return World.objects[self.item_id]

    @property
    def __data(self):
        return World.objinfo[self.item_id]

    # Support
    @property
    def name(self):
        return self.__object.name

    @property
    def description(self):
        return self.__object.description[self.state]

    @property
    def max_state(self):
        return self.__object.max_state

    @property
    def flannel(self):
        return self.__object.flannel

    @property
    def base_value(self):
        return self.__object.value

    @property
    def location(self):
        return self.__data[0]

    def set_location(self, value, carry_flag):
        self.__data[0] = value
        self.carry_flag = carry_flag

    @property
    def carry_flag(self):
        return self.__data[3]

    @carry_flag.setter
    def carry_flag(self, value):
        self.__data[3] = value

    @property
    def is_destroyed(self):
        return self.test_bit(0)

    # Unknown
    @property
    def state(self):
        raise NotImplementedError()

    @state.setter
    def state(self, value):
        raise NotImplementedError()

    @property
    def is_edible(self):
        return self.test_bit(6)

    @property
    def is_light(self):
        if self.item_id == 32:
            return True
        if self.test_bit(13):
            return True
        return False

    @property
    def owner(self):
        if self.carry_flag in (self.CARRY_0, self.IN_CONTAINER):
            return None
        return Player(self.location)

    @classmethod
    def fobna(cls, item_name):
        raise NotImplementedError()

    def iswornby(self, *args):
        raise NotImplementedError()

    # Support
    def create(self):
        self.clear_bit(0)

    def set_bit(self, bit_id):
        self.__data[2] = bit_set(bit_id)

    def clear_bit(self, bit_id):
        self.__data[2] = bit_clear(bit_id)

    def test_bit(self, bit_id):
        return bit_fetch(self.__data[2], bit_id)

    def set_byte(self, byte_id, value):
        self.__data[2] = byte_put(byte_id, value)

    def get_byte(self, byte_id):
        return byte_fetch(self.__data[2], byte_id)

    def test_mask(self, mask):
        return all(self.test_bit(bit_id) for bit_id, value in enumerate(mask) if value)


class Door(Item):
    def __init__(self, door_id):
        super().__init__(door_id - 1000)

    @property
    def other_id(self):
        return self.item_id ^ 1  # other door side

    @property
    def other(self):
        return Item(self.other_id)

    @property
    def invisible(self):
        return self.name != "door" or not self.description

    def go_through(self, player):
        new_location = self.other.location if self.state == 0 else 0
        if new_location >= 0:
            if player.in_dark or self.invisible:
                # Invis doors
                return 0
            else:
                raise CommandError("The door is not open\n")
        return new_location
