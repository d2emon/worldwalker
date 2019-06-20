from datetime import datetime
from ..errors import CrapupError, LooseError
from ..item import Item, Door
from ..location import Location
from ..syslog import syslog
from ..world import World
from .actor import Actor
from .base_player import BasePlayer
from .player import Player
from .user_data import UserData


GWIZ = None


def randperc():
    raise NotImplementedError()


class User(UserData, BasePlayer, Actor):
    def __init__(self, name):
        super().__init__()

        self.player_id = 0
        self.name = name
        self.__data = None

        # Property fields
        self.__location = None

        # Events
        self.before_message = lambda message: None
        self.get_new_player = lambda: {}

        # Other fields
        self.__in_setup = False
        self.__position_saved = 0

        # Parse
        self.__brief = False
        self.show_players = False

        self.__in_ms = "has arrived."
        self.__out_ms = ""
        self.__mout_ms = "vanishes in a puff of smoke."
        self.__min_ms = "appears with an ear-splitting bang."
        self.__here_ms = "is here"

        self.__is_summoned = 0  # tdes
        self.__summoned_location = 0  # ades
        self.__vdes = 0
        self.__rdes = 0
        self.zapped = False

        self.__last_interrupt = 0

        self.__invisibility_counter = 0
        self.__drunk_counter = 0
        self.__to_update = False

        # Weather
        self.has_farted = False

        # Unknown
        self.__interrupt = None
        self.__wpnheld = None

        self.NewUaf = None

        # makebfr()
        self.reset_position()
        self.add()

    # Player properties
    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        World.load()
        self.__location = value
        # self.__data.location = value
        self.look()

    @property
    def visible(self):
        raise NotImplementedError()

    @visible.setter
    def visible(self, value):
        raise NotImplementedError()

    @property
    def flags(self):
        raise NotImplementedError()

    @property
    def weapon(self):
        raise NotImplementedError()

    @weapon.setter
    def weapon(self, value):
        raise NotImplementedError()

    @property
    def helping(self):
        raise NotImplementedError()

    # Other properties
    @property
    def is_mobile(self):
        raise NotImplementedError()

    @property
    def __player(self):
        return Player(self.player_id)

    # Weather
    @property
    def items(self):
        # return [item for item in ITEMS if item.is_carried_by(self)]
        return [item for item in Item.items() if not item.is_destroyed and item.is_carried_by(self)]

    @property
    def __available_items(self):
        return [item for item in Item.items() if self.item_is_available(item)]

    @property
    def overweight(self):
        if self.capacity is None:
            return False
        return len(self.items) >= self.capacity

    @property
    def in_dark(self):
        if self.is_wizard:
            return False
        if not self.location.is_dark:
            return False
        for item in (item for item in Item.items() if item.is_light):
            if self.item_is_here(item):
                return False
            if item.owner is not None and item.owner.location.location_id == self.location.location_id:
                return False
        return True

    # Parse
    @property
    def summoned_location(self):
        return self.__summoned_location

    @summoned_location.setter
    def summoned_location(self, value):
        self.__summoned_location = value
        if not self.is_wizard:
            self.__is_summoned = True

    # Tk
    @classmethod
    def start_location(cls):
        return Location(-5 if randperc() > 50 else -183)

    # New1
    def get_damage(self, damage):
        if self.is_wizard:
            return

        self.strength -= damage
        self.__to_update = True

        if not self.is_dead:
            return

        World.save()

        syslog("{} slain magically".format(self.name))
        self.remove()
        self.zapped = True

        World.load()
        self.dump_items()
        self.loose()
        self.send_global("{} has just died\n".format(self.name))
        self.send_wizard("[ {} has just died ]\n".format(self.name))
        raise CrapupError("Oh dear you just died\n")

    # Not Implemented
    def chksnp(self, *args):
        raise NotImplementedError()

    def on_look(self, *args):
        raise NotImplementedError()

    # ObjSys
    def item_is_here(self, item):
        if not self.is_wizard and item.is_destroyed:
            return False
        return item.is_in_location(self.location)

    def find(self, player_name, not_found_error=None):
        player = Player.find(player_name)
        if player is None:
            return player
        if not self.seeplayer(player):
            return None
        return player

    # Support
    def item_is_available(self, item):
        return self.item_is_here(item) or item.is_carried_by(self)

    # Tk
    def add(self):
        World.load()
        if Player.find(self.name) is not None:
            raise CrapupError("You are already on the system - you may only be on once at a time")

        self.player_id = Player.new_player_id()
        if self.player_id is None:
            raise CrapupError("\nSorry AberMUD is full at the moment\n")

        # self.data.name = self.name
        # self.data.location = self.location.location_id
        # self.data.position = self.position
        self.level = 1
        self.visible = 0
        self.strength = -1
        self.weapon = None
        self.sex = 0
        self.__data = self

    def check_fight(self):
        self.Blood.check_fight()
        if self.Blood.fighting and self.Blood.get_enemy().location.location_id != self.location.location_id:
            self.Blood.stop_fight()

        if self.Blood.in_fight:
            self.Blood.in_fight -= 1

    # Unknown
    def check_kicked(self):
        self.reset_position()
        World.load()
        if self.find(self.name) is None:
            raise LooseError("You have been kicked off")

    # Support
    def has_any(self, mask):
        return any(item for item in self.__available_items if item.test_mask(mask))

    # Parse
    def hit_lightning(self, wizard):
        if self.is_wizard:
            yield "\001p{}\001 cast a lightning bolt at you\n".format(wizard.name)
            return

        # You are in the ....
        yield "A massive lightning bolt arcs down out of the sky to strike"
        self.send_wizard(
            "[ \001p{}\001 has just been zapped by \001p{}\001 and terminated ]\n".format(
                self.name,
                wizard.name,
            ),
        )

        yield " you between\nthe eyes\n"
        self.zapped = True
        self.delete()
        self.send_global("\001s{user}\001{user} has just died.\n\001".format(user=self.name))

        yield "You have been utterly destroyed by {}\n".format(wizard.name)
        raise LooseError("Bye Bye.... Slain By Lightning")

    # Tk
    def loose(self):
        # sig_aloff()
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.__in_setup = False

        World.load()
        self.dump_items()
        if self.visible < 10000:
            self.send_wizard("{} has departed from AberMUDII\n".format(self.name))
        self.delete()
        World.save()

        self.save()
        self.chksnp()

    # New1
    def __do_forced(self):
        if self.force_action is None:
            return

        self.is_forced = True
        gamecom(self.force_action)
        self.is_forced = False

    # Parse
    def on_messages(self):
        self.save_position()

        time = datetime.now()
        if (time - self.__last_interrupt).total_seconds() > 2:
            self.__interrupt = True
        if self.__interrupt:
            self.__last_interrupt = time

        self.__update_invisibility()

        if self.__to_update:
            yield from self.update()
            self.__to_update = False

        if self.__is_summoned:
            self.__summoned(self.summoned_location)

        self.__update_fight()

        if Item(18).iswornby(self) or randperc() < 10:
            self.strength += 1
            yield from self.update()

        self.__do_forced()

        if self.__drunk_counter > 0:
            self.__drunk_counter -= 1
            if not self.is_dumb:
                self.hiccup()

        self.__is_summoned = False
        self.__rdes = 0
        self.__vdes = 0
        self.__interrupt = False

    def save_position(self):
        if abs(self.position - self.__position_saved) < 10:
            return

        World.load()
        # self.__data = self
        self.__position_saved = self.position

    def start(self):
        location = self.start_location()
        UserData.load(self)

        World.load()
        self.visible = 0 if not self.is_god else 10000

        if self.load() is None:
            self.create(**self.get_new_player())

        self.send_wizard("\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self.name))

        yield from self.read_messages(reset_after_read=True)
        self.location = location

        self.send_global("\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self.name))

    # Parse
    def __summoned(self, location):
        self.send_global("\001s{name}\001{name} vanishes in a puff of smoke\n\001".format(name=self.name))
        self.dump_items()
        self.send_global("\001s{name}\001{name} appears in a puff of smoke\n\001".format(name=self.name))
        self.location = location

    def update(self):
        """
        Routine to correct me in user file

        :return:
        """
        if not self.__in_setup:
            return

        level = self.NewUaf.level_of(self.score)
        if level != self.level:
            self.level = level
            yield "You are now {} ".format(self.name)
            syslog("{} to level {}".format(self.name, level))
            yield self.level_name + "\n"
            self.send_wizard("\001p{}\001 is now level {}\n".format(self.name, self.level))
            if level == 10:
                yield "\001f{}\001".format(GWIZ)

        self.strength = min(self.strength, 30 + 10 * self.level)

        self.__data.level = self.level
        self.__data.strength = self.strength
        self.__data.sex = self.sex
        self.__data.weapon = self.__wpnheld

    def __update_invisibility(self):
        if self.__invisibility_counter:
            self.__invisibility_counter -= 1
        if self.__invisibility_counter == 1:
            self.visible = 0

    def __update_fight(self):
        if not self.Blood.in_fight:
            return
        enemy = self.Blood.get_enemy()
        if enemy.location.location_id != self.location.location_id:
            self.Blood.stop_fight()
        if not enemy.exists:
            self.Blood.stop_fight()
        if self.in_fight and self.__interrupt:
            self.Blood.in_fight = 0
            enemy.hitplayer(self.__wpnheld)

    def broadcast(self, message):
        self.force_read = True
        Broadcast(message).send(self)

    # Other
    @property
    def has_shield(self):
        shields = Shield113(), Shield114(), Shield89()
        return any(item.is_worn_by(self) for item in shields)
