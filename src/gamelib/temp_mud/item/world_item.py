from ..world import World
from .item_data import ItemData


class BaseItem:
    @property
    def location(self):
        raise NotImplementedError()

    @property
    def state(self):
        raise NotImplementedError()

    # Flags
    @property
    def is_destroyed(self):
        # 0     Destroyed
        raise NotImplementedError()

    @property
    def is_pair(self):
        # 1     Item is paired in state with then item number which is its num XOR 1
        raise NotImplementedError()

    @property
    def can_open(self):
        # 2     Can open/close   1=closed 0=open
        raise NotImplementedError()

    @property
    def can_lock(self):
        # 3     Can lock/unlock   2=locked
        raise NotImplementedError()

    @property
    def can_turn(self):
        # 4     Push sets to state 0
        raise NotImplementedError()

    @property
    def can_toggle(self):
        # 5     Push toggles state 1-0-1
        raise NotImplementedError()

    @property
    def is_food(self):
        # 6     Is Food	(normal food)
        raise NotImplementedError()

    # 7

    @property
    def can_wear(self):
        # 8     Can Wear
        raise NotImplementedError()

    @property
    def can_light(self):
        # 9     Can Light	(state 0 is lit)
        raise NotImplementedError()

    @property
    def can_extinguish(self):
        # 10    Can Extinguish (state 1 is extinguished)
        raise NotImplementedError()

    @property
    def is_key(self):
        # 11    Is A Key
        raise NotImplementedError()

    @property
    def can_change_state_on_take(self):
        # 12    State 0 if taken
        raise NotImplementedError()

    @property
    def is_light(self):
        # 13    Is lit  (state 0 is lit)
        raise NotImplementedError()

    @property
    def is_container(self):
        # 14    container
        raise NotImplementedError()

    @property
    def is_weapon(self):
        # 15    weapon
        raise NotImplementedError()

    # Locations
    @property
    def room(self):
        raise NotImplementedError()

    @property
    def owner(self):
        raise NotImplementedError()

    @property
    def container(self):
        raise NotImplementedError()

    # States
    @property
    def is_open(self):
        raise NotImplementedError()

    @property
    def is_locked(self):
        raise NotImplementedError()


class WorldItem(ItemData, BaseItem):
    __OBMUL = 8
    __NOBS = 196

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
        return (cls(item_id) for item_id in range(World.item_ids))

    @property
    def __data(self):
        return World.objinfo[self.item_id]

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

    def set_location(self, value, carry_flag):
        self.__carry_flag = carry_flag
        self.__data[0] = value.location_id

    # New1
    @property
    def state(self):
        return self.__data[1]

    @state.setter
    def state(self, value):
        self.__data[1] = value
        if self.is_pair:
            self.pair.__data[1] = value

    # 2

    # Support
    @property
    def __carry_flag(self):
        return self.__data[3]

    @__carry_flag.setter
    def __carry_flag(self, value):
        self.__data[3] = value

    # Flags
    @property
    def is_destroyed(self):
        return self.__test_bit(0)

    @property
    def is_pair(self):
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
        if self.is_in_location:
            return Location(self.__data[0])
        return None

    @property
    def owner(self):
        if self.is_carried:
            return Player(self.__data[0])
        return None

    @property
    def container(self):
        if self.is_contained:
            return self.by_item_id(self.__data[0])
        return None

    # States
    @property
    def is_open(self):
        return self.can_open and self.state == 0

    @property
    def is_locked(self):
        return self.can_lock and self.state == 2

    # Pair
    @property
    def __pair_id(self):
        if not self.is_pair:
            return None
        return self.item_id ^ 1  # other door side

    @property
    def pair(self):
        return self.by_item_id(self.__pair_id)

    # Search
    @classmethod
    def by_item_id(cls, item_id):
        return WorldItem(item_id)

    # ObjSys
    @classmethod
    def __find(
        cls,
        name,
        destroyed=False,
        available=None,  # 1
        owner=None,  # 2, 3
        location=None,  # 4
        container=None,  # 5
    ):
        if name is None:
            return None

        name = name.lower()
        if name == "red":
            # word = next(parser)
            return 4
        if name == "blue":
            # word = next(parser)
            return 5
        if name == "green":
            # word = next(parser)
            return 6

        items = cls.items()
        items = (item for item in items if item.name.lower() == name)
        # wd_it = item_name

        if available:
            # Patch for shields
            # if item.item_id == 112 and cls(113).is_carried_by(user):
            #     return 113
            # if item.item_id == 112 and cls(114).is_carried_by(user):
            #     return 114
            # if user.item_is_available(item):
            #     return item
            items = (item for item in items)
        elif owner is not None:
            items = (item for item in items if item.is_carried_by(owner))
        elif location is not None:
            items = (item for item in items if item.is_in_location(location))
        elif container is not None:
            items = (item for item in items if item.is_contained_in(container))
        if not destroyed:
            items = (item for item in items if not item.is_destroyed)
        return items

    @classmethod
    def find(
        cls,
        name,
        destroyed=False,
        mode_0=False,  # 0
        available=False,  # 1
        owner=None,  # 2, 3
        location=None,  # 4
        container=None,  # 5
    ):
        item = next(
            cls.__find(
                name,
                destroyed=destroyed,
                available=available,
                owner=owner,
                location=location,
                container=container,
            ),
            None
        )
        if not mode_0:
            return item

        if item is None:
            return None
        return next(
            cls.__find(
                item.name,
                destroyed=destroyed,
            ),
            None
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
        items = cls.items()
        if carry_flag == cls.CARRIED:
            items = (item for item in items if item.is_carried_by(location))
        elif carry_flag == cls.IN_CONTAINER:
            items = (item for item in items if item.is_contained_in(location))
        else:
            items = []
        if not destroyed:
            items = (item for item in items if not item.is_destroyed)
        return items

    # Flag utils
    # Support
    def __set_bit(self, bit_id):
        self.__data[2][bit_id] = True

    def __clear_bit(self, bit_id):
        self.__data[2][bit_id] = False

    def __test_bit(self, bit_id):
        """
        15=weapon
        14=container
        13=Is lit  (state 0 is lit)
        12=State 0 if taken
        11=Is A Key
        10=Can Extinguish (state 1 is extinguished)
        09=Can Light	(state 0 is lit)
        08=Can Wear
        07=
        06=Is Food	(normal food)
        05=Push toggles state 1-0-1
        04=Push sets to state 0
        03=Can lock/unlock   2=locked
        02=Can open/close   1=closed 0=open
        01=Item is paired in state with then item number which is its num XOR 1
        00=Destroyed

        :param bit_id:
        :return:
        """
        return self.__data[2][bit_id]

    def __set_byte(self, byte_id, value):
        self.__data[2][byte_id] = value

    def __get_byte(self, byte_id):
        return self.__data[2][byte_id]

    def __test_mask(self, mask):
        return all(self.__test_bit(bit_id) for bit_id, value in enumerate(mask) if value)

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

    # Compare location
    def is_worn_by(self, owner):
        return self.is_carried_by(owner) and self.is_worn

    def is_carried_by(self, owner):
        # if is_wizard
        return self.location == owner.location_id and self.is_carried

    def is_contained_in(self, container):
        # if is_wizard
        return self.location == container.item_id and self.is_contained

    def is_in_location(self, location):
        return self.location == location.location_id and self.is_located
