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

    @property
    def is_container(self):
        # 14    container
        raise NotImplementedError()

    @property
    def is_weapon(self):
        # 15    weapon
        raise NotImplementedError()

    # Flag setters
    def create(self):
        raise NotImplementedError()

    def destroy(self):
        raise NotImplementedError()

    def extinguish(self, actor):
        raise NotImplementedError()

    def light(self, actor):
        raise NotImplementedError()

    def on_taken(self, actor):
        raise NotImplementedError()

    # Bytes
    def get_byte(self, byte_id):
        raise NotImplementedError()

    def set_byte(self, byte_id, value):
        raise NotImplementedError()

    # Locations
    @property
    def room(self):
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

    # States
    @property
    def is_open(self):
        raise NotImplementedError()

    @property
    def is_locked(self):
        raise NotImplementedError()

    # Pair
    @property
    def pair(self):
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
        return location.equal(self.room)
