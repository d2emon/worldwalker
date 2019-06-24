from ..location import Location
from ..player.player import Player
from ..services.items import ItemsService
from ..world import World
from .base_item import BaseItem
from .item_data import ItemData


class WorldItem(ItemData, BaseItem):
    IN_LOCATION = 0
    CARRIED = 1
    WEARING = 2
    IN_CONTAINER = 3

    def __init__(self, item_id):
        self.__item_id = item_id

    @property
    def item_id(self):
        return self.__item_id

    @classmethod
    def items(cls):
        return (WorldItem(item_id) for item_id in range(World.item_ids))

    @property
    def __data(self):
        return ItemsService.get_info(item_id=self.item_id)

    # Support
    @property
    def location(self):
        if self.room is not None:
            return self.room
        elif self.owner is not None:
            return self.owner
        elif self.container is not None:
            return self.container
        return None

    def __get_location(self, location_class, *carry_flags):
        if self.__carry_flag not in carry_flags:
            return None
        return location_class(self.__data[0])

    def __set_location(self, value, carry_flag):
        self.__carry_flag = carry_flag
        self.__data[0] = value.location_id

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

    # 2

    # Support
    @property
    def __carry_flag(self):
        return self.__data[3]

    @__carry_flag.setter
    def __carry_flag(self, value):
        self.__data[3] = value

    # Flag utils
    # Support
    def __set_bit(self, bit_id):
        self.__data[2][bit_id] = True

    def __clear_bit(self, bit_id):
        self.__data[2][bit_id] = False

    def __test_bit(self, bit_id):
        return self.__data[2][bit_id]

    def __test_mask(self, mask):
        return all(self.__test_bit(bit_id) for bit_id, value in enumerate(mask) if value)

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
        raise NotImplementedError()

    @property
    def is_light(self):
        return self.__test_bit(13)

    @property
    def is_container(self):
        return self.__test_bit(14)

    @property
    def is_weapon(self):
        raise NotImplementedError()

    # Flag setters
    def create(self):
        self.__clear_bit(0)
        return self

    def destroy(self):
        self.__set_bit(0)
        return self

    def extinguish(self, actor):
        self.state = 1
        self.__clear_bit(13)

    def light(self, actor):
        self.state = 0
        self.__set_bit(13)

    def on_taken(self, actor):
        if self.__test_bit(12):
            self.state = 0

    # Bytes
    def get_byte(self, byte_id):
        return self.__data[2][byte_id]

    def set_byte(self, byte_id, value):
        self.__data[2][byte_id] = value

    # Locations
    @property
    def is_located(self):
        return self.__carry_flag == self.IN_LOCATION

    @property
    def is_carried(self):
        return self.__carry_flag in (self.CARRIED, self.WEARING)

    @property
    def is_worn(self):
        return self.__carry_flag == self.WEARING

    @property
    def is_contained(self):
        return self.__carry_flag == self.IN_CONTAINER

    @property
    def room(self):
        return self.__get_location(Location, self.IN_LOCATION)

    @room.setter
    def room(self, value):
        self.__set_location(value, self.IN_LOCATION)

    @property
    def owner(self):
        return self.__get_location(Player, self.CARRIED, self.WEARING)

    @owner.setter
    def owner(self, value):
        self.__set_location(value, self.CARRIED)

    @property
    def wearer(self):
        return self.__get_location(Player, self.WEARING)

    @wearer.setter
    def wearer(self, value):
        self.__set_location(value, self.WEARING)

    @property
    def container(self):
        return self.__get_location(self.__get, self.IN_CONTAINER)

    @container.setter
    def container(self, value):
        self.__set_location(value, self.IN_CONTAINER)

    # States
    @property
    def is_open(self):
        return self.can_open and self.state == 0

    @property
    def is_locked(self):
        return self.can_lock and self.state == 2

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

    # Equals
    def equal(self, item):
        return item is not None and self.item_id == item.item_id

    # Search
    @classmethod
    def __get(cls, item_id):
        return WorldItem(item_id)

    @classmethod
    def __by_name(cls, items, name):
        return (item for item in items if item.name.lower() == name)

    # ObjSys
    @classmethod
    def __patch_color(cls, name):
        colors = {
            "red": WorldItem(4),
            "blue": WorldItem(5),
            "green": WorldItem(6),
        }
        item = colors.get(name, None)
        if item is not None:
            # word = next(parser)
            pass
        return item

    @classmethod
    def __patch_shields(cls, item, user):
        # Patch for shields
        shields = WorldItem(113), WorldItem(114)
        if item.item_id == 112:
            for shield in shields:
                if shield.is_carried_by(user):
                    return shield
        return item

    @classmethod
    def __filter(cls, item, **kwargs):
        name = kwargs.get('name')
        available = kwargs.get('available')  # 1
        owner = kwargs.get('owner')  # 2, 3
        location = kwargs.get('owner')  # 4
        container = kwargs.get('container')  # 5
        destroyed = kwargs.get('destroyed', False)

        if name is not None and item.name.lower() != name:
            return None
        else:
            # wd_it = item_name
            pass

        if available is not None:
            item = cls.__patch_shields(item, available)
            if not available.item_is_available(item):
                return None
        # elif
        if owner is not None and not item.is_carried_by(owner):
            return None
        # elif
        if location is not None and not item.is_in_location(location):
            return None
        # elif
        if container is not None and not item.is_contained_in(container):
            return None

        if not destroyed and item.is_destroyed:
            return None
        return item

    @classmethod
    def __find(cls, **kwargs):
        name = kwargs.get("name")
        if name is None:
            return ()

        color = cls.__patch_color(name)
        if color is not None:
            return color,

        kwargs["name"] = name.lower()

        return (item for item in map(lambda item: cls.__filter(item, **kwargs), cls.items()) if item is not None)

    @classmethod
    def __first(cls, **kwargs):
        return next(cls.__find(**kwargs), None)

    @classmethod
    def find(cls, **kwargs):
        item = cls.__first(**kwargs)
        if item is None:
            return None
        if not kwargs.get("mode_0", False):
            return item
        return cls.__first(
            name=item.name,
            destroyed=kwargs.get("destroyed", False)
        )

    @classmethod
    def find_at(cls, location, carry_flag, destroyed=False):
        """
        Carried Loc !

        :param location:
        :param carry_flag:
        :param destroyed:
        :return:
        """
        items = map(lambda item: cls.__filter(item, destroyed=destroyed), cls.items())
        if carry_flag == cls.CARRIED:
            return (item for item in items if item is not None and item.is_carried_by(location))
        elif carry_flag == cls.IN_CONTAINER:
            return (item for item in items if item is not None and item.is_contained_in(location))
        else:
            return ()
