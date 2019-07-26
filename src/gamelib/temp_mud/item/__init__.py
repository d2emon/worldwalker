from ..errors import CommandError
from ..magic import random_percent
from ..weather import Weather
from .world_item import Item


# Base classes
class Door(Item):
    def __init__(self, door_id):
        super().__init__(door_id - 1000)

    @property
    def can_open(self):
        return True

    @property
    def is_visible(self):
        return self.name == "door" and len(self.description) > 0

    def go_through(self, actor):
        new_location = self.pair.location if self.is_open else None
        if new_location is not None and new_location.location_id > 0:
            return new_location

        if actor.can_see_door(self):
            raise CommandError("The door is not open\n")

        # Invisible doors
        return None


class Shield(Item):
    def on_wear(self, actor):
        shields = [Shield89(), Shield113(), Shield114()]
        if any(shield.is_worn_by(actor) for shield in shields):
            raise CommandError("You can't use TWO shields at once...\n")


class Candle(Item):
    candle_id = 0
    color = ""

    def __init__(self):
        super().__init__(self.candle_id + 3)


# Items
class Umbrella(Item):
    def __init__(self):
        super().__init__(1)

    def open(self, actor):
        if self.state == 1:
            raise CommandError("It is\n")
        else:
            self.state = 1
            yield "The Umbrella Opens\n"

    def close(self, actor):
        if self.state == 0:
            raise CommandError("It is closed, silly!\n")
        else:
            self.state = 0
            yield "Ok\n"


class RedCandle(Candle):
    candle_id = 1
    color = "red"


class BlueCandle(Candle):
    candle_id = 2
    color = "blue"


class GreenCandle(Candle):
    candle_id = 3
    color = "green"


class CrystalBall(Item):
    __candles = RedCandle(), BlueCandle(), GreenCandle(),

    def __init__(self):
        super().__init__(7)

    @property
    def candle(self):
        if self.state <= 0:
            return None
        return self.__candles[self.state - 1]

    def on_examine(self, actor):
        self.state = random_percent() % 3 + 1
        yield "It glows {}\n".format(self.candle.color)


class Scroll(Item):
    crystal_ball = CrystalBall()

    def __init__(self):
        super().__init__(8)

    def __success(self, actor):
        candle = self.crystal_ball.candle
        if candle is None:
            return False
        if not candle.is_carried_by(actor):
            return False
        if not candle.is_light:
            return False
        return True

    def examine(self, actor):
        if self.__success(actor):
            yield "Everything shimmers and then solidifies into a different view!\n"
            self.destroy()
            return actor.teleport(-1074)
        return super().examine(actor)


class Candlestick(Item):
    def __init__(self):
        super().__init__(10)

    @property
    def can_extinguish(self):
        if not self.has_candle:
            return super().can_extinguish
        return True

    @property
    def can_light(self):
        if not self.has_candle:
            return super().can_light
        return True

    @property
    def is_light(self):
        if not self.has_candle:
            return super().is_light
        return self.state == 0

    @property
    def has_candle(self):
        return self.state != 2

    @property
    def candle(self):
        if not self.has_candle:
            return None

        return Item(self.get_byte(1))

    @candle.setter
    def candle(self, value):
        if not isinstance(value, Candle):
            raise CommandError("You can't do that\n")
        if self.has_candle:
            raise CommandError("There is already a candle in it!\n")

        value.destroy()
        self.set_byte(1, value.item_id)
        self.state = value.is_light

    def put_in(self, item, actor):
        self.candle = item
        yield "The candle fixes firmly into the candlestick\n"
        actor.score += 50


class Cauldron(Item):
    def __init__(self):
        super().__init__(11)

    def eat(self, actor):
        yield "You feel funny, and then pass out\n"
        yield "You wake up elsewhere....\n"
        actor.teleport(-1076)


class Door20Side0(Door):
    def __init__(self):
        super().__init__(20)

    def open(self, actor):
        raise CommandError("You can't shift the door from this side!!!!\n")


class Door20Side1(Door):
    def __init__(self):
        super().__init__(21)

    def open(self, actor):
        if self.state == 0:
            raise CommandError("It is\n")
        else:
            raise CommandError("It seems to be magically closed\n")


class Hole(Item):
    __door = Door20Side0()

    def __init__(self):
        super().__init__(23)

    def put_in(self, item, actor):
        if item.item_id == 19 and self.__door.state == 1:
            yield "The door clicks open!\n"
            self.__door.state = 0
            return

        yield "Nothing happens\n"


class Torch(Item):
    def __init__(self):
        super().__init__(24)

    @property
    def __door(self):
        return SecretDoorSide0()

    def push(self, actor):
        if self.__door.state == 1:
            self.__door.state = 0
            yield "A secret door slides quietly open in the south wall!!!\n"
        else:
            yield "It moves but nothing seems to happen\n"


class SecretDoorSide0(Door):
    def __init__(self):
        super().__init__(26)


class PortcullisSide0(Door):
    def __init__(self):
        super().__init__(28)


class PortcullisSide1(Door):
    def __init__(self):
        super().__init__(29)


class Lever(Item):
    __door = PortcullisSide0()

    def __init__(self):
        super().__init__(30)

    def push(self, actor):
        self.__door.state = 1 - self.__door.state
        if self.__door.state:
            actor.send_global("\001cThe portcullis falls\n\001", self.__door.location)
            actor.send_global("\001cThe portcullis falls\n\001", self.__door.pair.location)
        else:
            actor.send_global("\001cThe portcullis rises\n\001", self.__door.location)
            actor.send_global("\001cThe portcullis rises\n\001", self.__door.pair.location)


class MagicSword(Item):
    def __init__(self):
        super().__init__(32)

    @property
    def is_light(self):
        return True

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

    def on_put(self, actor, container):
        raise CommandError("You can't let go of it!\n")

    def on_look(self, actor):
        if actor.Blood.in_fight:
            return
        players = (Player(player_id) for player_id in range(32) if player_id != actor.player_id)
        players = (player for player in players if player.exists)
        players = (player for player in players if not player.is_wizard)
        players = (player for player in players if player.location.location_id == actor.location.location_id)
        player = next(players, None)
        if player is None:
            return

        if random_percent() < 9 * actor.level:
            return
        if Player.find(player.name) is None:
            return

        yield "The runesword twists in your hands lashing out savagely\n"

        actor.hit_player(player, self)


class Bell(Item):
    def __init__(self):
        super().__init__(49)

    def push(self, actor):
        actor.broadcast("\001dChurch bells ring out around you\n\001")


class Item75(Item):
    def __init__(self):
        super().__init__(75)

    def eat(self, actor):
        yield "very refreshing\n"


class Item85(Item):
    def __init__(self):
        super().__init__(85)

    def examine(self, actor):
        item = Item(83)
        if item.__get_byte(0):
            return super().examine(actor)

        yield "Aha. under the bed you find a loaf and a rabbit pie\n"
        item.create()
        item.__set_byte(0, 1)
        Item(84).create()


class Shield89(Shield):
    def __init__(self):
        super().__init__(89)


class Item91(Item):
    def __init__(self):
        super().__init__(91)

    def examine(self, actor):
        item = Item(90)
        if item.__get_byte(0):
            return super().examine(actor)

        yield "You pull an amulet from the bedding\n"
        item.create()
        item.__set_byte(0, 1)


class Item101(Item):
    def __init__(self):
        super().__init__(101)

    def examine(self, actor):
        if self.__get_byte(0) != 0:
            return super().examine(actor)

        yield "You take a key from one pocket\n"
        self.__set_byte(0, 1)
        key = Item(107)
        key.create()
        key.set_location(actor, self.CARRIED)


class Item102(Item):
    def __init__(self):
        super().__init__(102)


class Item103(Item):
    def __init__(self):
        super().__init__(103)


class Item104(Item):
    def __init__(self):
        super().__init__(104)

    def push(self, actor):
        if actor.helper is None:
            raise CommandError("You can't shift it alone, maybe you need help\n")
        actor.broadcast("\001dChurch bells ring out around you\n\001")


class Shields(Item):
    def __init__(self):
        super().__init__(112)

    def on_take(self, actor, container):
        if container is None:
            return self

        shields = [Shield113(), Shield114()]
        shield = next((shield.is_destroyed for shield in shields), None)
        if shield is None:
            raise CommandError("The shields are all to firmly secured to the walls\n")

        return shield.create()


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


class Item126(Item):
    def __init__(self):
        super().__init__(126)

    def push(self, actor):
        yield "The tripwire moves and a huge stone crashes down from above!\n"
        actor.broadcast("\001dYou hear a thud and a squelch in the distance.\n\001")
        actor.loose()
        raise CrapupError("             S   P    L      A         T           !")


class Item130(Item):
    def __init__(self):
        super().__init__(130)

    def push(self, actor):
        if Item132().state == 1:
            Item132().state = 0
            yield "A secret panel opens in the east wall!\n"
        else:
            yield "Nothing happens\n"


class Item131(Item):
    def __init__(self):
        super().__init__(131)

    def push(self, actor):
        if Item134().state == 1:
            yield "Uncovering a hole behind it.\n"
            Item134().state = 0


class Item132(Item):
    def __init__(self):
        super().__init__(132)


class Item134(Item):
    def __init__(self):
        super().__init__(134)


class Item136(Item):
    def __init__(self):
        super().__init__(136)

    def wave(self, actor):
        door = DrawbridgeBack()
        if door.state != 1 or door.location.location_id == actor.location.location_id:
            return
        DrawbridgeFront().state = 0
        yield "The drawbridge is lowered!\n"


class Item137(Item):
    def __init__(self):
        super().__init__(137)

    def put_in(self, item, actor):
        if self.state == 0:
            item.set_location(Location(-162), self.IN_LOCATION)
            yield "ok\n"
            return

        item.destroy()
        yield "It dissappears with a fizzle into the slime\n"

        if item.item_id == 108:
            yield "The soap dissolves the slime away!\n"
            self.state = 0


class Item138(Item):
    def __init__(self):
        super().__init__(138)

    def push(self, actor):
        if Item137().state == 0:
            yield "Ok...\n"
        else:
            yield "You hear a gurgling noise and then silence.\n"
            Item137().state = 0


class Item144(Item):
    def __init__(self):
        super().__init__(144)

    def examine(self, actor):
        if self.__get_byte(0) != 0:
            return super().examine(actor)
        self.__set_byte(0, 1)
        yield "You take a scroll from the tube.\n"

        scroll = Scroll()
        scroll.create()
        scroll.set_location(actor, self.CARRIED)


class Scroll(Item):
    def __init__(self):
        super().__init__(145)

    def examine(self, actor):
        yield "As you read the scroll you are teleported!\n"
        self.destroy()
        actor.location_id = -114


class Item146(Item):
    def __init__(self, item_id=146):
        super().__init__(item_id)

    def push(self, actor):
        Item146().state = 1 - Item146().state
        yield "Ok...\n"


class Item147(Item146):
    def __init__(self):
        super().__init__(147)


class Item149(Item):
    def __init__(self):
        super().__init__(149)

    def push(self, actor):
        DrawbridgeFront().state = 1 - DrawbridgeFront().state
        if DrawbridgeFront().state:
            actor.send_global("\001cThe drawbridge rises\n\001", DrawbridgeFront().location)
            actor.send_global("\001cThe drawbridge rises\n\001", DrawbridgeBack().location)
        else:
            actor.send_global("\001cThe drawbridge is lowered\n\001", DrawbridgeFront().location)
            actor.send_global("\001cThe drawbridge is lowered\n\001", DrawbridgeBack().location)


class DrawbridgeFront(Item):
    def __init__(self):
        super().__init__(150)


class DrawbridgeBack(Item):
    def __init__(self):
        super().__init__(151)


class Item158(Item):
    def __init__(self):
        super().__init__(158)

    def wave(self, actor):
        yield "You are teleported!\n"
        actor.teleport(Location(-114))


class Item162(Item):
    def __init__(self):
        super().__init__(162)

    def push(self, actor):
        yield "A trapdoor opens at your feet and you plumment downwards!\n"
        actor.location_id = -140


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


class ChuteTop(Item):
    def __init__(self):
        super().__init__(192)

    def put_in(self, item, actor):
        if item.item_id == 32:
            raise CommandError("You can't let go of it!\n")
        yield "It vanishes down the chute....\n"
        actor.send_global("The {} comes out of the chute!\n".format(item.name), ChuteBottom.location)
        item.set_location(ChuteBottom.location, self.IN_LOCATION)


class ChuteBottom(Item):
    def __init__(self):
        super().__init__(193)

    def put_in(self, item, actor):
        raise CommandError("You can't do that, the chute leads up from here!\n")


__CANDLES = {
    "red": RedCandle(),
    "blue": BlueCandle(),
    "green": GreenCandle(),
}

__SHIELD = Shields()
__SHIELDS = Shield113(), Shield114()

ITEMS = [
    Weather(),
    Umbrella(),  # 1
    # Item2(),
    # Item3(),
    __CANDLES["red"],  # 4
    __CANDLES["blue"],  # 5
    __CANDLES["green"],  # 6
    CrystalBall(),  # 7
    Scroll(),  # 8
    # Item9(),

    Candlestick(),  # 10
    Cauldron(),
    # Item12(),
    # Item13(),
    # Item14(),
    # Item15(),
    # Item16(),
    # Item17(),
    # Item18(),
    # Item19(),

    Door20Side0,  # 20
    Door20Side1,  # 21
    # Item22(),
    Hole(),  # 23
    Torch(),  # 24
    # Item25(),
    SecretDoorSide0(),  # 26
    # SecretDoorSide1(),  # 27
    PortcullisSide0(),  # 28
    PortcullisSide1(),  # 29

    Lever(),
    # Item31(),
    MagicSword,  # 32
    # Item33(),
    # Item34(),
    # Item35(),
    # Item36(),
    # Item37(),
    # Item38(),
    # Item39(),

    # Item40(),
    # Item41(),
    # Item42(),
    # Item43(),
    # Item44(),
    # Item45(),
    # Item46(),
    # Item47(),
    # Item48(),
    Bell(),  # 49

    # Item50(),
    # Item51(),
    # Item52(),
    # Item53(),
    # Item54(),
    # Item55(),
    # Item56(),
    # Item57(),
    # Item58(),
    # Item59(),

    # Item60(),
    # Item61(),
    # Item62(),
    # Item63(),
    # Item64(),
    # Item65(),
    # Item66(),
    # Item67(),
    # Item68(),
    # Item69(),

    # Item70(),
    # Item71(),
    # Item72(),
    # Item73(),
    # Item74(),
    Item75(),
    # Item76(),
    # Item77(),
    # Item78(),
    # Item79(),

    # Item80(),
    # Item81(),
    # Item82(),
    # Item83(),
    # Item84(),
    Item85(),
    # Item86(),
    # Item87(),
    # Item88(),
    Shield89(),

    # Item90(),
    Item91(),
    # Item92(),
    # Item93(),
    # Item94(),
    # Item95(),
    # Item96(),
    # Item97(),
    # Item98(),
    # Item99(),

    # Item100(),
    Item101(),
    Item102(),
    Item103(),
    Item104(),
    # Item105(),
    # Item106(),
    # Item107(),
    # Item108(),
    # Item109(),

    # Item110(),
    # Item111(),
    __SHIELD,  # 112
    __SHIELDS[0],  # 113
    __SHIELDS[1],  # 114
    # Item115(),
    # Item116(),
    # Item117(),
    # Item118(),
    # Item119(),

    # Item120(),
    # Item121(),
    Item122(),
    Item123(),
    # Item124(),
    # Item125(),
    Item126(),
    # Item127(),
    # Item128(),
    # Item129(),

    Item130(),
    Item131(),
    Item132(),
    # Item133(),
    Item134(),
    # Item135(),
    Item136(),
    Item137(),
    Item138(),
    # Item139(),

    # Item140(),
    # Item141(),
    # Item142(),
    # Item143(),
    Item144(),
    Scroll(),  # 145
    Item146(),
    Item147(),
    # Item148(),
    Item149(),

    DrawbridgeFront(),  # 150
    DrawbridgeBack(),  # 151
    # Item152(),
    # Item153(),
    # Item154(),
    # Item155(),
    # Item156(),
    # Item157(),
    Item158(),
    # Item159(),

    # Item160(),
    # Item161(),
    Item162(),
    # Item163(),
    # Item164(),
    # Item165(),
    # Item166(),
    # Item167(),
    # Item168(),
    # Item169(),

    # Item170(),
    # Item171(),
    # Item172(),
    # Item173(),
    # Item174(),
    Item175(),
    Item176(),
    # Item177(),
    # Item178(),
    # Item179(),

    # Item180(),
    # Item181(),
    # Item182(),
    # Item183(),
    # Item184(),
    # Item185(),
    Item186(),
    # Item187(),
    # Item188(),
    # Item189(),

    # Item190(),
    # Item191(),
    ChuteTop(),  # 192
    ChuteBottom(),  # 193
    # Item194(),
    # Item195(),
]


# ObjSys
# Patches
def __patch_colored(name):
    item = {
        "red": ITEMS[4],
        "blue": ITEMS[5],
        "green": ITEMS[6],
    }.get(name)
    if item is not None:
        # word = next(parser)
        pass
    return item


def __patch_shields(item, owner):
    # Patch for shields
    if not __SHIELD.equal(item):
        return item
    return next((shield for shield in __SHIELDS if shield.is_carried_by(owner)), item)


def __filter_by(**kwargs):
    def f(item):
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
            item = __patch_shields(item, available)
            if not any(available.items_available.filter(item=item).all):
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
    return f


def __find(**kwargs):
    name = kwargs.get("name")
    if name is None:
        return ()

    name = name.lower()
    kwargs["name"] = name

    colored = __patch_colored(name)
    if colored is not None:
        return colored,
    return (item for item in map(__filter_by(**kwargs), ITEMS) if item is not None)


def __by_name(name):
    return (item for item in ITEMS if item.name.lower() == name)


def find_item(**kwargs):
    item = next(__find(**kwargs))
    if item is None:
        return None
    elif kwargs.get("mode_0", False):
        return next(__find(
            name=item.name,
            destroyed=kwargs.get("destroyed", False),
        ))
    else:
        return item


def find_items(**kwargs):
    return (item for item in map(__filter_by(**kwargs), ITEMS) if item is not None)
