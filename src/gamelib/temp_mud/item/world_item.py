from ..errors import CommandError, ServiceError
from ..location import Location
from ..player.player import Player
from ..services.items import ItemsService
from .base_item import BaseItem
from .item_data import ItemData


class Item(ItemData, BaseItem):
    # Flags
    __IN_LOCATION = 0
    __CARRIED = 1
    __WEARING = 2
    __IN_CONTAINER = 3

    # States
    STATE_ON = 0
    STATE_OFF = 1
    STATE_LOCKED = 2

    def __init__(self, item_id):
        super().__init__(item_id)
        self.__item_id = item_id

    @property
    def item_id(self):
        return self.__item_id

    @property
    def __data(self):
        return ItemsService.get_info(item_id=self.item_id)

    @classmethod
    def __get(cls, item_id):
        return WorldItem(item_id)

    def reload(self):
        pass

    # Support
    # Locations
    @property
    def location(self):
        return self.__get_location(Location, self.__IN_LOCATION)

    @location.setter
    def location(self, value):
        self.__set_location(value, self.__IN_LOCATION)

    @property
    def owner(self):
        return self.__get_location(Player, self.__CARRIED, self.__WEARING)

    @owner.setter
    def owner(self, value):
        self.__set_location(value, self.__CARRIED)

    @property
    def wearer(self):
        return self.__get_location(Player, self.__WEARING)

    @wearer.setter
    def wearer(self, value):
        self.__set_location(value, self.__WEARING)

    @property
    def container(self):
        return self.__get_location(self.__get, self.__IN_CONTAINER)

    @container.setter
    def container(self, value):
        self.__set_location(value, self.__IN_CONTAINER)

    # New1
    @property
    def state(self):
        if self.__is_pair:
            return self.pair.state
        return self.__data[1]

    @state.setter
    def state(self, value):
        if self.__is_pair:
            self.pair.state = value
            return
        self.__data[1] = value

    # Flags
    @property
    def is_destroyed(self):
        return self.__test_bit(0)

    @property
    def has_pair(self):
        return self.__test_bit(1)

    @property
    def can_open(self):
        return self.__test_bit(2)

    @property
    def can_lock(self):
        return self.__test_bit(3)

    @property
    def can_turn(self):
        return self.__test_bit(4)

    @property
    def can_toggle(self):
        return self.__test_bit(5)

    @property
    def is_food(self):
        return self.__test_bit(6)

    # 7

    @property
    def can_wear(self):
        return self.__test_bit(8)

    @property
    def can_light(self):
        return self.__test_bit(9)

    @property
    def can_extinguish(self):
        return self.__test_bit(10)

    @property
    def is_key(self):
        return self.__test_bit(11)

    @property
    def can_change_state_on_take(self):
        return self.__test_bit(12)

    @property
    def is_light(self):
        return self.__test_bit(13)

    @is_light.setter
    def is_light(self, value):
        if value:
            if not self.can_light:
                raise CommandError("You can't light that!\n")
            if self.state == self.STATE_ON:
                raise CommandError("It is lit\n")
            self.state = self.STATE_ON
            self.__set_bit(13)
        else:
            if not self.can_extinguish:
                raise CommandError("You can't extinguish that!\n")
            if not self.is_light:
                raise CommandError("That isn't lit\n")
            self.state = self.STATE_OFF
            self.__clear_bit(13)

    @property
    def is_container(self):
        return self.__test_bit(14)

    @property
    def is_weapon(self):
        raise NotImplementedError()

    # Support
    @property
    def __carry_flag(self):
        return self.__data[3]

    @__carry_flag.setter
    def __carry_flag(self, value):
        self.__data[3] = value

    # Pair
    @property
    def __is_pair(self):
        if not self.has_pair:
            return False
        return self.item_id & 1

    @property
    def pair(self):
        # other door side
        if not self.has_pair:
            return None
        return self.__get(self.item_id ^ 1)

    # States
    @property
    def is_open(self):
        return self.can_open and self.state == self.STATE_ON

    @is_open.setter
    def is_open(self, value):
        if value:
            if not self.can_open:
                raise CommandError("You can't open that\n")
            elif self.is_open:
                raise CommandError("It already is\n")
            elif self.is_locked:
                raise CommandError("It's locked!\n")
            self.state = self.STATE_ON
        else:
            if not self.can_open:
                raise CommandError("You can't close that\n")
            if not self.is_open:
                raise CommandError("It is open already\n")
            self.state = self.STATE_OFF

    @property
    def is_locked(self):
        return self.can_lock and self.state == self.STATE_LOCKED

    @is_locked.setter
    def is_locked(self, value):
        if value:
            if not self.can_lock:
                raise CommandError("You can't lock that!\n")
            if self.is_locked:
                raise CommandError("It's already locked\n")
            self.state = self.STATE_LOCKED
        else:
            if not self.can_lock:
                raise CommandError("You can't unlock that\n")
            if not self.is_locked:
                raise CommandError("Its not locked!\n")
            self.state = self.STATE_OFF

    @property
    def text(self):
        try:
            return ItemsService.get_description(item_id=self.item_id)
        except ServiceError:
            return super().text

    @property
    def is_visible(self):
        return len(self.description) > 0

    # Utils
    # Location utils
    def __get_location(self, location_class, *carry_flags):
        if self.__carry_flag not in carry_flags:
            return None
        return location_class(self.__data[0])

    def __set_location(self, value, carry_flag):
        self.__carry_flag = carry_flag
        self.__data[0] = value.location_id

    # Flag utils
    # Support
    def __set_bit(self, bit_id):
        self.__data[2][0][bit_id] = True

    def __clear_bit(self, bit_id):
        self.__data[2][0][bit_id] = False

    def __test_bit(self, bit_id):
        return self.__data[2][0][bit_id]

    def __test_mask(self, mask):
        return all(self.__test_bit(bit_id) for bit_id, value in enumerate(mask) if value)

    # Bytes
    def __get_byte(self, byte_id):
        return self.__data[2][byte_id + 1]

    def __set_byte(self, byte_id, value):
        self.__data[2][byte_id + 1] = value

    # Flag setters
    def create(self):
        self.__clear_bit(0)
        return self

    def destroy(self):
        self.__set_bit(0)
        return self

    def extinguish(self, actor):
        self.is_light = False
        return self

    def light(self, actor):
        self.is_light = True
        return self

    # Equals
    def equal(self, item):
        return item is not None and self.item_id == item.item_id

    # Actions
    def push(self, actor):
        if self.can_turn:
            self.state = self.STATE_ON
            actor.get_message(actor.show_item_description(self))
            return self

        if self.can_toggle:
            self.state = self.STATE_OFF if self.state == self.STATE_ON else self.STATE_ON
            actor.get_message(actor.show_item_description(self))
            return self

        actor.get_message("Nothing happens\n")
        return self

    def put_in(self, item, actor):
        super().put_in(item, actor)

        if actor.get_dragon():
            return self

        item.on_put(actor, self)
        item.container = self

        actor.get_message("Ok\n")
        actor.send_global("\001D{}\001\001c puts the {} in the {}.\n\001".format(actor.name, item.name, self.name))

        item.on_taken(actor)
        # if item.can_change_state_on_take:
        #     item.state = self.STATE_ON

        actor.location.on_put(actor, item, self)

    # Events
    def on_taken(self, actor):
        if self.can_change_state_on_take:
            self.state = self.STATE_ON
