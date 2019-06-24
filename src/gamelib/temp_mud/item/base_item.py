from ..errors import CommandError


class BaseItemData:
    @property
    def name(self):
        raise NotImplementedError()

    @property
    def descriptions(self):
        raise NotImplementedError()

    @property
    def max_state(self):
        raise NotImplementedError()

    @property
    def flannel(self):
        raise NotImplementedError()

    @property
    def base_value(self):
        raise NotImplementedError()

    @property
    def state(self):
        raise NotImplementedError()

    @property
    def description(self):
        return self.descriptions[self.state]


class BaseItem:
    # Locations
    @property
    def location(self):
        raise NotImplementedError()

    @property
    def owner(self):
        raise NotImplementedError()

    @property
    def wearer(self):
        raise NotImplementedError()

    @property
    def container(self):
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
    def has_pair(self):
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

    @is_light.setter
    def is_light(self, value):
        raise NotImplementedError()

    @property
    def is_container(self):
        # 14    container
        raise NotImplementedError()

    @property
    def is_weapon(self):
        # 15    weapon
        raise NotImplementedError()

    # States
    @property
    def is_open(self):
        raise NotImplementedError()

    @is_open.setter
    def is_open(self, value):
        raise NotImplementedError()

    @property
    def is_locked(self):
        raise NotImplementedError()

    @is_locked.setter
    def is_locked(self, value):
        raise NotImplementedError()

    # Pair
    @property
    def pair(self):
        raise NotImplementedError()

    @property
    def where(self):
        if self.location is not None:
            return self.location
        elif self.owner is not None:
            return self.owner
        elif self.container is not None:
            return self.container
        return None

    @property
    def location_text(self):
        if self.location is not None:
            return self.location.item_location
        elif self.container is not None:
            return "In the {}\n".format(self.container.name)
        elif self.owner is not None:
            return "Carried by \001c{}\001\n".format(self.owner.name)

    @property
    def text(self):
        return "You see nothing special.\n"

    # Flag setters
    def create(self):
        raise NotImplementedError()

    def destroy(self):
        raise NotImplementedError()

    # Bytes
    def __get_byte(self, byte_id):
        raise NotImplementedError()

    def __set_byte(self, byte_id, value):
        raise NotImplementedError()

    # Equals
    def equal(self, item):
        raise NotImplementedError()

    # Compare location
    def is_worn_by(self, wearer):
        return wearer.equal(self.wearer)

    def is_carried_by(self, owner):
        # if is_wizard
        return owner.equal(self.owner)

    def is_contained_in(self, container):
        # if is_wizard
        return container.equal(self.container)

    def is_located_in(self, location):
        return location.equal(self.location)

    # Actions
    # Paired actions
    def open(self, actor):
        self.is_open = True
        actor.get_message("Ok\n")
        return self

    def close(self, actor):
        self.is_open = False
        actor.get_message("Ok\n")
        return self

    def extinguish(self, actor):
        self.is_light = False
        actor.get_message("Ok\n")
        return self

    def light(self, actor):
        self.is_light = True
        actor.get_message("Ok\n")
        return self

    def lock(self, actor):
        self.is_locked = True
        actor.get_message("Ok\n")
        return self

    def unlock(self, actor):
        self.is_locked = False
        actor.get_message("Ok\n")
        return self

    # Other actions
    def blow(self, actor):
        raise CommandError("You can't blow that\n")

    def eat(self, actor):
        if not self.is_food:
            raise CommandError("That's sure not the latest in health food....\n")

        self.destroy()
        actor.get_message("Ok....\n")
        actor.strength += 12
        return self

    def examine(self, actor):
        self.on_examine(actor)
        actor.get_message(self.text)
        return self

    def play(self, actor):
        return self

    def push(self, actor):
        raise NotImplementedError

    def put_in(self, item, actor):
        if self.equal(item):
            raise CommandError("What do you think this is, the goon show ?\n")
        if not self.is_container:
            raise CommandError("You can't do that\n")
        if item.flannel:
            raise CommandError("You can't take that !\n")
        return self

    def roll(self, actor):
        raise CommandError("You can't roll that\n")

    def spray(self, actor, target):
        raise CommandError("You can't do that\n")

    def wave(self, actor):
        actor.get_message("Nothing happens\n")

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

    def on_look(self, actor):
        return None

    def on_owner_flee(self, owner):
        return None

    def on_put(self, actor, container):
        return None

    def on_take(self, actor, container):
        return None

    def on_taken(self, actor):
        return None

    def on_wear(self, actor):
        return None
