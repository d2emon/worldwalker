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
    CARRIED = 1
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
    def is_closable(self):
        return self.test_bit(2)

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
    def is_container(self):
        return self.test_bit(14)

    @property
    def is_closed(self):
        return self.is_closable and self.state != 0

    @property
    def owner(self):
        if self.carry_flag in (self.CARRY_0, self.IN_CONTAINER):
            return None
        return Player(self.location)

    @classmethod
    def fobn(cls, item_name):
        raise NotImplementedError()

    @classmethod
    def fobna(cls, item_name):
        raise NotImplementedError()

    @classmethod
    def fobncb(cls, item_name, owner):
        raise NotImplementedError()

    def iswornby(self, *args):
        raise NotImplementedError()

    def iscarrby(self, *args):
        raise NotImplementedError()

    def iscontin(self, *args):
        raise NotImplementedError()

    def contain(self):
        return [item for item in self.items() if item.iscontin(self)]

    def eat(self, actor):
        if not self.is_edible:
            raise CommandError("That's sure not the latest in health food....\n")

        self.destroy()
        yield "Ok....\n"
        actor.strength += 12
        yield from actor.update()

    def play(self, actor):
        pass

    def roll(self, actor):
        raise CommandError("You can't roll that\n")

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

    # Events
    def on_give(self, actor):
        return None

    def on_dig(self, actor):
        return None

    def on_dig_here(self, actor):
        return None


class Door(Item):
    def __init__(self, door_id):
        super().__init__(door_id - 1000)

    @property
    def is_closed(self):
        return self.state != 0

    @property
    def other_id(self):
        return self.item_id ^ 1  # other door side

    @property
    def other(self):
        return Item(self.other_id)

    @property
    def invisible(self):
        return self.name != "door" or not self.description

    def go_through(self, actor):
        new_location = self.other.location if not self.is_closed else 0
        if new_location < 0:
            return new_location

        if actor.in_dark or self.invisible:
            # Invis doors
            return 0
        else:
            raise CommandError("The door is not open\n")


class Item11(Item):
    def __init__(self):
        super().__init__(11)

    def eat(self, actor):
        yield "You feel funny, and then pass out\n"
        yield "You wake up elsewhere....\n"
        actor.teleport(-1076)


class Item32(Item):
    def __init__(self):
        super().__init__(32)

    def on_give(self, actor):
        if not actor.is_wizard:
            raise CommandError("It doesn't wish to be given away.....\n")


class Item75(Item):
    def __init__(self):
        super().__init__(75)

    def eat(self, actor):
        yield "very refreshing\n"


class Item122(Item):
    def __init__(self, item_id=122):
        super().__init__(item_id)

    def roll(self, actor):
        actor.push("pillar")


class Item123(Item122):
    def __init__(self):
        super().__init__(123)


class Item175(Item):
    def __init__(self):
        super().__init__(175)

    def eat(self, actor):
        if actor.level < 3:
            actor.score += 40
            yield "You feel a wave of energy sweeping through you.\n"
        else:
            yield "Faintly magical by the taste.\n"
            if actor.strength < 40:
                actor.strength += 2
        yield from actor.update()


class Item176(Item):
    def __init__(self):
        super().__init__(176)

    def on_dig(self, actor):
        if self.state == 0:
            raise CommandError("You widen the hole, but with little effect.\n")
        self.state = 0
        yield "You rapidly dig through to another passage.\n"


class Item186(Item):
    def __init__(self):
        super().__init__(176)

    def on_dig_here(self, actor):
        if self.location == actor.location_id and self.is_destroyed:
            yield "You uncover a stone slab!\n"
            self.create()
            return


ITEMS = [
    Item11(),
    Item32(),
    Item75(),
    Item122(),
    Item123(),
    Item175(),
    Item176(),
    Item186(),
]