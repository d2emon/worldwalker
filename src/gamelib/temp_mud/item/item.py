from gamelib.temp_mud.errors import CommandError
from gamelib.temp_mud.player import Player
from gamelib.temp_mud.world import World
from ..services.descriptions import DescriptionService
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

    def examine(self, actor):
        self.on_examine(actor)
        try:
            yield DescriptionService.get(item_id=self.item_id)
        except ServiceError:
            yield "You see nothing special.\n"

    # Events
    def on_dig(self, actor):
        return None

    def on_dig_here(self, actor):
        return None

    def on_drop(self, actor):
        return None

    def on_examine(self, actor):
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
