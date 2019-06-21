from gamelib.temp_mud.errors import CommandError
from gamelib.temp_mud.player import Player
from gamelib.temp_mud.world import World
from .world_item import WorldItem


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


class Item(WorldItem):
    # ObjSys
    @classmethod
    def list_items_at(cls, location, carry_flag, debug=False, destroyed=False):
        """
        Carried Loc !
        """
        items = [item for item in cls.find_at(location, carry_flag, destroyed)]
        if len(items) <= 0:
            yield "Nothing"
        else:
            yield from (item.get_text(debug) for item in items)
        yield "\n"

    # ObjSys
    def get_item_text(self, debug=False):
        text = self.name
        if debug:
            text += self.item_id
        if self.is_destroyed:
            text = "({})".format(text)
        if self.is_worn:
            text += "<worn> "
        text += " "
        return text

    # Unknown
    def contain(self, destroyed=False):
        items = self.items()
        items = (item for item in items if item.is_contained_in(self))
        items = (item for item in items if destroyed or not item.is_destroyed)
        return list(items)

    # Actions
    def show_description(self, debug=False):
        if debug:
            return "{{{}}} {}".format(self.item_id, self.description)
        return self.description

    def eat(self, actor):
        if not self.is_food:
            raise CommandError("That's sure not the latest in health food....\n")

        self.destroy()
        yield "Ok....\n"

        actor.strength += 12
        yield from actor.update()

    def play(self, actor):
        pass

    def roll(self, actor):
        raise CommandError("You can't roll that\n")

    def open(self, actor):
        if not self.can_open:
            raise CommandError("You can't open that\n")
        elif self.is_open:
            raise CommandError("It already is\n")
        elif self.is_locked:
            raise CommandError("It's locked!\n")

        self.state = 0
        yield "Ok\n"

    def close(self, actor):
        if not self.can_open:
            raise CommandError("You can't close that\n")
        elif not self.is_open:
            raise CommandError("It is open already\n")
        else:
            self.state = 1
            yield "Ok\n"

    def lock(self, actor):
        if not self.can_lock:
            raise CommandError("You can't lock that!\n")
        elif self.is_locked:
            raise CommandError("It's already locked\n")
        else:
            self.state = 2
            yield "Ok\n"

    def unlock(self, actor):
        if not self.can_lock:
            raise CommandError("You can't unlock that\n")
        elif not self.is_locked:
            raise CommandError("Its not locked!\n")
        else:
            self.state = 1
            yield "Ok...\n"

    def wave(self, actor):
        yield "Nothing happens\n"

    def blow(self, actor):
        raise CommandError("You can't blow that\n")

    def put_in(self, item, actor):
        if self.item_id == item.item_id:
            raise CommandError("What do you think this is, the goon show ?\n")
        if not self.is_container:
            raise CommandError("You can't do that\n")
        if item.flannel:
            raise CommandError("You can't take that !\n")
        if actor.get_dragon():
            return
        item.on_put(actor, self)

        item.set_location(self, self.IN_CONTAINER)
        yield "Ok.\n"
        actor.send_global("\001D{}\001\001c puts the {} in the {}.\n\001".format(actor.name, item.name, self.name))

        if item.__test_bit(12):
            item.state = 0

        actor.location.on_put(actor, item, self)

    def light(self, actor):
        if not self.can_light:
            raise CommandError("You can't light that!\n")
        if self.state == 0:
            raise CommandError("It is lit\n")

        super().light(actor)
        yield "Ok\n"

    def extinguish(self, actor):
        if not self.can_extinguish:
            raise CommandError("You can't extinguish that!\n")
        if not self.is_light:
            raise CommandError("That isn't lit\n")

        super().extinguish(actor)
        yield "Ok\n"

    def push(self, actor):
        # ELSE RUN INTO DEFAULT
        if self.can_turn:
            self.state = 0
            yield self.show_description(actor.debug_mode)
        elif self.can_toggle:
            self.state = 1 - self.state
            yield self.show_description(actor.debug_mode)
        else:
            yield "Nothing happens\n"

    def spray(self, actor, target):
        raise CommandError("You can't do that\n")

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

    def on_put(self, actor, container):
        return None

    def on_take(self, actor, container):
        return self

    def on_taken(self, actor):
        super().on_taken(actor)

    def on_wear(self, actor):
        pass

    def on_look(self, actor):
        pass


class Door(Item):
    def __init__(self, door_id):
        super().__init__(door_id - 1000)

    @property
    def can_open(self):
        return True

    @property
    def is_invisible(self):
        return self.name != "door" or not self.description

    def go_through(self, actor):
        new_location = self.pair.location if self.is_open else Location(0)
        if new_location is not None and new_location.location_id > 0:
            return new_location

        if actor.in_dark or self.is_invisible:
            # Invis doors
            return None
        else:
            raise CommandError("The door is not open\n")


class Shield(Item):
    def on_wear(self, actor):
        shields = [Shield89(), Shield113(), Shield114()]
        if any(shield.is_worn_by(actor) for shield in shields):
            raise CommandError("You can't use TWO shields at once...\n")


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


class Item10(Item):
    def __init__(self):
        super().__init__(10)

    def put_in(self, item, actor):
        if item.item_id < 4 or item.item_id > 6:
            raise CommandError("You can't do that\n")
        if self.state != 2:
            raise CommandError("There is already a candle in it!\n")

        yield "The candle fixes firmly into the candlestick\n"
        actor.score += 50
        item.destroy()
        self.__set_byte(1, item.item_id)
        self.__set_bit(9)
        self.__set_bit(10)
        if item.__test_bit(13):
            self.__set_bit(13)
            self.state = 0
        else:
            self.__clear_bit(13)
            self.state = 1


class Item11(Item):
    def __init__(self):
        super().__init__(11)

    def eat(self, actor):
        yield "You feel funny, and then pass out\n"
        yield "You wake up elsewhere....\n"
        actor.teleport(-1076)


class Item20(Item):
    def __init__(self):
        super().__init__(20)

    def open(self, actor):
        raise CommandError("You can't shift the door from this side!!!!\n")


class Item21(Item):
    def __init__(self):
        super().__init__(21)

    def open(self, actor):
        if self.state == 0:
            raise CommandError("It is\n")
        else:
            raise CommandError("It seems to be magically closed\n")


class Item23(Item):
    def __init__(self):
        super().__init__(23)

    def put_in(self, item, actor):
        if item.item_id == 19 and Item21.state == 1:
            yield "The door clicks open!\n"
            Item20.state = 0
            return

        yield "Nothing happens\n"


class Item24(Item):
    def __init__(self):
        super().__init__(24)

    def push(self, actor):
        if SecretDoor().state == 1:
            SecretDoor().state = 0
            yield "A secret door slides quietly open in the south wall!!!\n"
        else:
            yield "It moves but nothing seems to happen\n"


class SecretDoor(Item):
    def __init__(self):
        super().__init__(26)


class PortcullisFront(Item):
    def __init__(self):
        super().__init__(28)


class PortcullisBack(Item):
    def __init__(self):
        super().__init__(29)


class Item30(Item):
    def __init__(self):
        super().__init__(30)

    def push(self, actor):
        PortcullisFront().state = 1 - PortcullisFront().state
        if PortcullisFront().state:
            actor.send_global("\001cThe portcullis falls\n\001", PortcullisFront().location)
            actor.send_global("\001cThe portcullis falls\n\001", PortcullisBack().location)
        else:
            actor.send_global("\001cThe portcullis rises\n\001", PortcullisFront().location)
            actor.send_global("\001cThe portcullis rises\n\001", PortcullisBack().location)


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

        if randperc() < 9 * actor.level:
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


class Shield89(Shield):
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


ITEMS = [
    Umbrella(),  # 1

    Item10(),
    Item11(),

    Item20(),
    Item21(),

    Item23(),
    Item24(),

    SecretDoor(),

    PortcullisFront(),  # 28
    PortcullisBack(),  # 29
    Item30(),

    MagicSword,  # 32

    Bell(),

    Item75(),

    Shield89(),

    Item101(),
    Item102(),
    Item103(),
    Item104(),

    Shields(),  # 112
    Shield113(),
    Shield114(),

    Item122(),
    Item123(),

    Item126(),

    Item130(),
    Item131(),
    Item132(),

    Item134(),

    Item136(),
    Item137(),
    Item138(),

    Item146(),
    Item147(),

    Item149(),
    DrawbridgeFront(),  # 150
    DrawbridgeBack(),  # 151

    Item158(),

    Item162(),

    Item175(),
    Item176(),

    Item186(),

    ChuteTop(),  # 192
    ChuteBottom(),  # 193
]