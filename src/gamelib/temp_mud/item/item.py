from gamelib.temp_mud.errors import CommandError
from gamelib.temp_mud.player import Player
from gamelib.temp_mud.world import World


"""
Object structure

Name,
Long Text 1
Long Text 2
Long Text 3
Long Text 4
statusmax
Value
flags (0=Normal 1+flannel)


Objinfo

Loc
Status
Stamina
Flag 1=carr 0=here


Objects held in format

[Short Text]
[4 Long texts]
[Max State]


Objects in text file in form

Stam:state:loc:flag
"""


class Item:
    __OBMUL = 8
    __NOBS = 196

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
        return self.__test_bit(0)

    # Unknown
    @property
    def state(self):
        raise NotImplementedError()

    @state.setter
    def state(self, value):
        raise NotImplementedError()

    @property
    def is_closable(self):
        return self.__test_bit(2)

    @property
    def is_edible(self):
        return self.__test_bit(6)

    @property
    def is_light(self):
        if self.item_id == 32:
            return True
        if self.__test_bit(13):
            return True
        return False

    @property
    def is_container(self):
        return self.__test_bit(14)

    @property
    def is_closed(self):
        return self.is_closable and self.state != 0

    @property
    def owner(self):
        if self.carry_flag in (self.CARRY_0, self.IN_CONTAINER):
            return None
        return Player(self.location)

    # ObjSys
    @classmethod
    def __find(
        cls,
        item_name,
        destroyed=False,
        available=None,  # 1
        owner=None,  # 2, 3
        location=None,  # 4
        container=None,  # 5
    ):
        if item_name is None:
            return None

        item_name = item_name.lower()
        if item_name == "red":
            # word = next(parser)
            return 4
        if item_name == "blue":
            # word = next(parser)
            return 5
        if item_name == "green":
            # word = next(parser)
            return 6

        items = [item for item in cls.items() if item.name.lower == item_name]
        # wd_it = item_name

        if available:
            # Patch for shields
            # if item.item_id == 112 and cls(113).iscarrby(user):
            #     return 113
            # if item.item_id == 112 and cls(114).iscarrby(user):
            #     return 114
            # if user.item_is_available(item):
            #     return item
            items = [item for item in items]
        elif owner is not None:
            items = [item for item in items if item.is_carried_by(owner)]
        elif location is not None:
            items = [item for item in items if item.is_in_locaton(location)]
        elif container is not None:
            items = [item for item in items if item.is_contained_in(container)]

        if not destroyed:
            return [item for item in items if not item.is_destroyed]

        return items

    @classmethod
    def __find_at(cls, location, carry_flag, destroyed=False):
        """
        Carried Loc !

        :param location:
        :param carry_flag:
        :param destroyed:
        :return:
        """
        if carry_flag == cls.CARRIED:
            items = [item for item in cls.items() if item.is_carried_by(location)]
        elif carry_flag == cls.IN_CONTAINER:
            items = [item for item in cls.items() if item.is_contained_in(location)]
        else:
            items = []

        return [item for item in items if destroyed or not item.is_destroyed]

    @classmethod
    def list_items_at(cls, location, carry_flag, debug=False, destroyed=False):
        """
        Carried Loc !
        """
        items = [item for item in cls.__find_at(location, carry_flag, destroyed)]
        if len(items) <= 0:
            yield "Nothing\n"
            return

        for item in items:
            text = item.name
            if debug:
                text = "{}{}".format(text, item.item_id)
            if item.is_destroyed:
                text = "({})".format(text)
            if item.iswornby(location):
                text += "<worn> "
            text += " "
            yield text
        yield "\n"

    # Unknown
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
        name = item.name

        return next(
            cls.__find(
                name,
                destroyed=destroyed,
            ),
            None
        )

    def iswornby(self, *args):
        raise NotImplementedError()

    def is_carried_by(self, owner):
        # if is_wizard
        if self.carry_flag not in [self.CARRIED, self.WEARING]:
            return False
        return self.location == owner.location_id

    def is_contained_in(self, container):
        # if is_wizard
        if self.carry_flag != self.IN_CONTAINER:
            return False
        return self.location == container.item_id

    def is_in_locaton(self, location):
        if self.carry_flag == self.CARRIED:
            return False
        return self.location == location.location_id

    def contain(self, destroyed=False):
        items = [item for item in self.items() if item.is_contained_in(self)]
        return [item for item in items if destroyed or not item.is_destroyed]

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

    def oplong(self, debug=False):
        if debug:
            return "{{{}}} {}".format(self.item_id, self.description)
        return self.description

    # Support
    def create(self):
        self.__clear_bit(0)

    def __set_bit(self, bit_id):
        self.__data[2][bit_id] = True

    def __clear_bit(self, bit_id):
        self.__data[2][bit_id] = False

    def __test_bit(self, bit_id):
        return self.__data[2][bit_id]

    def __set_byte(self, byte_id, value):
        self.__data[2][byte_id] = value

    def __get_byte(self, byte_id):
        return self.__data[2][byte_id]

    def test_mask(self, mask):
        return all(self.__test_bit(bit_id) for bit_id, value in enumerate(mask) if value)

    # Events
    def on_dig(self, actor):
        return None

    def on_dig_here(self, actor):
        return None

    def on_drop(self, actor):
        return None

    def on_give(self, actor):
        return None

    def on_owner_flee(self, owner):
        return None

    def on_take(self, actor, container):
        return self

    def on_taken(self, actor):
        if self.__test_bit(12):
            self.state = 0


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


class MagicSword(Item):
    def __init__(self):
        super().__init__(32)

    def on_drop(self, actor):
        if not actor.is_wizard:
            raise CommandError("You can't let go of it!\n")

    def on_give(self, actor):
        if not actor.is_wizard:
            raise CommandError("It doesn't wish to be given away.....\n")

    def on_owner_flee(self, owner):
        raise CommandError("The sword won't let you!!!!\n")

    def on_take(self, actor, container):
        if self.state == 1 and actor.helper is None:
            raise CommandError("Its too well embedded to shift alone.\n")


class Item75(Item):
    def __init__(self):
        super().__init__(75)

    def eat(self, actor):
        yield "very refreshing\n"


class Shield89(Item):
    def __init__(self):
        super().__init__(89)


class Item101(Item):
    def __init__(self):
        super().__init__(101)


class Item102(Item):
    def __init__(self):
        super().__init__(102)


class Item103(Item):
    def __init__(self):
        super().__init__(103)


class Shields(Item):
    def __init__(self):
        super().__init__(112)

    def on_take(self, actor, container):
        if container is None:
            return self

        if Item(113).is_destroyed:
            return Item113().on_take(actor, container)
        elif Item(114).is_destroyed:
            return Item114().on_take(actor, container)
        else:
            raise CommandError("The shields are all to firmly secured to the walls\n")


class Shield(Item):
    def on_take(self, actor, container):
        self.__clear_bit(0)
        return self


class Shield113(Shield):
    def __init__(self):
        super().__init__(113)


class Shield114(Shield):
    def __init__(self):
        super().__init__(114)


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
    MagicSword,  # 32
    Item75(),
    Shield89(),
    Item101(),
    Item102(),
    Item103(),
    Shields(),  # 112
    Shield113(),
    Shield114(),
    Item122(),
    Item123(),
    Item175(),
    Item176(),
    Item186(),
]