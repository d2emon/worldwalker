from ..errors import CommandError, CrapupError, LooseError, ServiceError
from ..item.item import Item, ITEMS
from ..location import Location
from ..magic import random_percent
from ..message import message_codes
from ..parser import Parser
from ..syslog import syslog
from ..weather import Weather
from ..world import World
from ..zone import ZONES
from .mobile import MOBILES
from .player import Player
from .reader import Reader
from .sender import Sender


EXE = None
EXE2 = None
CREDITS = None


def execl(*args):
    raise NotImplementedError()


def wizard_action(message):
    def wrapper(f):
        def wrapped(self, *args):
            if not self.is_wizard:
                raise NotImplementedError(message)
            return f(self, *args)
        return wrapped
    return wrapper


def god_action(message):
    def wrapper(f):
        def wrapped(self, *args):
            if not self.is_god:
                raise NotImplementedError(message)
            return f(self, *args)
        return wrapped
    return wrapper


def message_action(f):
    def wrapped(self, *args):
        if not self.can_modify_messages:
            raise NotImplementedError("No way !\n")
        return f(self, *args)
    return wrapped


# def not_blind_action(f):
#     def wrapped(self, *args):
#         if self.is_blind:
#             raise CommandError("You are blind, you cannot see\n")
#         return f(self, *args)
#     return wrapped


def not_crippled_action(f):
    def wrapped(self, *args):
        if self.is_crippled:
            raise CommandError("You are crippled\n")
        return f(self, *args)
    return wrapped


# def not_deaf_action(f):
#     def wrapped(self, *args):
#         if self.is_blind:
#             raise CommandError()
#         return f(self, *args)
#     return wrapped


def not_dumb_action(f):
    def wrapped(self, *args):
        if self.is_dumb:
            raise CommandError("You are dumb...\n")
        return f(self, *args)
    return wrapped


def not_force_action(message):
    def wrapper(f):
        def wrapped(self, *args):
            if self.is_forced:
                raise CommandError(message)
            return f(self, *args)
        return wrapped
    return wrapper


class Actor(Sender, Reader):
    # Modules
    @property
    def Blood(self):
        raise NotImplementedError()

    # Not Implemented
    @property
    def available_items(self):
        raise NotImplementedError()

    @property
    def brief(self):
        raise NotImplementedError()

    @brief.setter
    def brief(self, value):
        raise NotImplementedError()

    @property
    def conversation_mode(self):
        raise NotImplementedError()

    @conversation_mode.setter
    def conversation_mode(self, value):
        raise NotImplementedError()

    @property
    def debug_mode(self):
        raise NotImplementedError()

    @debug_mode.setter
    def debug_mode(self, value):
        raise NotImplementedError()

    @property
    def __euid(self):
        raise NotImplementedError()

    @property
    def force_action(self):
        raise NotImplementedError()

    @force_action.setter
    def force_action(self, value):
        raise NotImplementedError()

    @property
    def is_forced(self):
        raise NotImplementedError()

    @is_forced.setter
    def is_forced(self, value):
        raise NotImplementedError()

    @property
    def has_farted(self):
        raise NotImplementedError()

    @has_farted.setter
    def has_farted(self, value):
        raise NotImplementedError()

    @property
    def in_dark(self):
        raise NotImplementedError()

    @property
    def items(self):
        raise NotImplementedError()

    @property
    def level_name(self):
        raise NotImplementedError()

    @property
    def show_players(self):
        raise NotImplementedError()

    @show_players.setter
    def show_players(self, value):
        # if not value:
        #     parser.mode = parser.MODE_SPECIAL
        raise NotImplementedError()

    @property
    def in_ms(self):
        raise NotImplementedError()

    @in_ms.setter
    def in_ms(self, value):
        raise NotImplementedError()

    @property
    def out_ms(self):
        raise NotImplementedError()

    @out_ms.setter
    def out_ms(self, value):
        raise NotImplementedError()

    @property
    def min_ms(self):
        raise NotImplementedError()

    @min_ms.setter
    def min_ms(self, value):
        raise NotImplementedError()

    @property
    def mout_ms(self):
        raise NotImplementedError()

    @mout_ms.setter
    def mout_ms(self, value):
        raise NotImplementedError()

    @property
    def overweight(self):
        raise NotImplementedError()

    @property
    def player_id(self):
        raise NotImplementedError()

    @property
    def visible(self):
        raise NotImplementedError()

    @visible.setter
    def visible(self, value):
        raise NotImplementedError()

    @property
    def __uid(self):
        raise NotImplementedError()

    @property
    def __is_valid_uid(self):
        return self.__uid == self.__euid

    def check_kicked(self, *args):
        raise NotImplementedError()

    def debug2(self, *args):
        raise NotImplementedError()

    def item_is_available(self, *args):
        raise NotImplementedError()

    def loose(self, *args):
        raise NotImplementedError()

    def on_look(self, *args):
        raise NotImplementedError()

    def remove(self, *args):
        raise NotImplementedError()

    def reset_position(self, *args):
        raise NotImplementedError()

    def save_position(self, *args):
        raise NotImplementedError()

    def show_buffer(self, *args):
        raise NotImplementedError()

    def update(self, *args):
        raise NotImplementedError()

    # Base Player properties
    @property
    def can_debug(self):
        raise NotImplementedError()

    @property
    def can_edit(self):
        raise NotImplementedError()

    @property
    def can_modify_messages(self):
        raise NotImplementedError()

    @property
    def can_set_flags(self):
        raise NotImplementedError()

    @property
    def is_god(self):
        raise NotImplementedError()

    @property
    def is_wizard(self):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()

    @property
    def location(self):
        raise NotImplementedError()

    @location.setter
    def location(self, value):
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def strength(self):
        raise NotImplementedError()

    @property
    def sex(self):
        raise NotImplementedError()

    @property
    def score(self):
        raise NotImplementedError()

    @score.setter
    def score(self, value):
        raise NotImplementedError()

    def die(self, *args):
        raise NotImplementedError()

    def dump_items(self, *args):
        raise NotImplementedError()

    def fade(self, *args):
        raise NotImplementedError()

    # Disease
    @property
    def is_dumb(self):
        raise NotImplementedError()

    @property
    def is_crippled(self):
        raise NotImplementedError()

    @property
    def is_blind(self):
        raise NotImplementedError()

    @property
    def is_deaf(self):
        raise NotImplementedError()

    # Other
    @property
    def is_fighting(self):
        return self.Blood.in_fight > 0

    def add_force(self, action):
        if self.force_action is not None:
            yield "The compulsion to {} is overridden\n".format(action)
        self.force_action = action

    def __fade_system(self, actions):
        self.fade()
        self.save_position()
        World.save()

        yield from actions

        self.check_kicked()
        yield from self.read_messages()

    def get_dragon(self):
        # Mobile
        if self.is_wizard:
            return False
        dragon = Player.find("dragon")
        if dragon is None:
            return False
        if dragon.location.location_id == self.location.location_id:
            return False
        return True

    def list_items(self):
        return Item.list_items_at(self, Item.CARRIED, self.debug, self.is_wizard)

    def on_flee(self):
        # New1
        items = [item for item in ITEMS if item.is_carried_by(self) and not item.is_worn_by(self)]
        map(lambda item: item.set_location(self, item.IN_LOCATION), items)

    def __silly_sound(self, message):
        self.send_silly("\001P{user.name}\001\001d " + message + "\n\001")

    def __silly_visual(self, message):
        self.send_silly("\001s{user.name}\001{user.name} " + message + "\n\001")

    # 1 - 10
    @not_crippled_action
    def go(self, direction):
        # Parse
        # 1 - 7
        if direction is None:
            raise CommandError("That's not a valid direction\n")
        if self.is_fighting:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")
        yield from map(lambda mobile: mobile.on_actor_leave(self, direction), MOBILES)

        location = self.location.go_to(direction, self)

        yield from location.on_enter(self)
        yield from map(lambda mobile: mobile.on_actor_enter(self, direction, location), MOBILES)

        self.send_global(
            "\001s{actor.data.name}\001{actor.name} has gone {direction} {message}.\n\001".format(
                actor=self,
                direction=direction.title,
                message=self.out_ms
            ),
        )
        self.location = location
        self.send_global(
            "\001s{actor.name}\001{actor.name}{message}.\n\001".format(
                actor=self,
                # direction=direction,
                message=self.in_ms
            ),
        )

    @not_force_action("You can't be forced to do that\n")
    def quit_game(self):
        # Parse
        yield from self.read_messages()

        if self.is_fighting:
            raise CommandError("Not in the middle of a fight!\n")

        yield "Ok"

        World.load()
        self.send_global("{} has left the game\n".format(self.name))
        self.send_wizard("[ Quitting Game : {} ]\n".format(self.name))
        self.dump_items()
        self.die()
        self.remove()
        World.save()

        self.location = Location(0)
        self.show_players = False
        self.save()
        raise CrapupError("Goodbye")

    def take(self, item, container=None):
        # ObjSys
        if item is None:
            raise CommandError("That is not here.\n")

        item = item.on_take(self, container)

        if item.flannel == 1:
            raise CommandError("You can't take that!\n")

        if self.get_dragon():
            return

        if self.overweight:
            raise CommandError("You can't carry any more\n")

        item.set_location(self, 1)
        yield "Ok...\n"

        self.send_global("\001D{}\001\001c takes the {}\n\001".format(self.name, item.name))

        item.on_taken(self)
        self.location.on_take_item(self, item)

    def drop(self, item):
        # ObjSys
        if item is None:
            raise CommandError("You are not carrying that.\n")

        yield from item.on_drop(self)

        item.set_location(self.location, 0)
        yield "OK..\n"
        self.send_global("\001D{}\001\001c drops the {}.\n\n\001".format(self.name, item.name))

        yield from self.location.on_drop(self, item)

    # 11 - 20
    def look(self, long=False):
        # Tk
        World.save()

        self.location.reload()

        if self.is_wizard:
            yield self.location.get_name(self)

        if self.location.death_room:
            if self.is_blind:
                self.Disease.blind.cure()
            if self.is_wizard:
                yield "<DEATH ROOM>\n"
            else:
                raise LooseError("bye bye.....\n")

        if self.is_blind:
            yield "You are blind... you can't see a thing!\n"
            return

        if self.in_dark:
            yield "It is dark\n"
            World.load()
            self.on_look()
            return

        yield self.location.short

        if long or not self.brief or self.location.no_brief:
            yield "\n".join(self.location.description)

        World.load()

        if not self.is_blind:
            yield from self.location.list_items()
            if self.show_players:
                self.location.list_people()
        yield "\n"

        self.on_look()

    def look_in(self, item):
        # Parse
        if item is None:
            raise CommandError("What ?\n")
        if not item.is_container:
            raise CommandError("That isn't a container\n")
        if item.is_closed:
            raise CommandError("It's closed!\n")
        yield "The {} contains:\n".format(item.name)
        yield from Item.list_items_at(self, Item.IN_CONTAINER, self.debug, self.is_wizard)

    def inventory(self):
        # ObjSys
        yield "You are carrying\n"
        yield from self.list_items()

    def who(self, users=False):
        # ObjSys
        # 13 + 155
        if not self.is_wizard:
            users = True

        if not users:
            yield "Players\n"
            players = PLAYERS
        else:
            players = PLAYERS[:16]

        for player in (player for player in players if player.visible <= self.level):
            if player.player_id == 16:
                yield "----------\nMobiles\n"
            if player.exists:
                yield player.show(self)

        yield "\n"

    @wizard_action("What ?\n")
    def reset_world(self):
        # Parse
        self.broadcast("Reset in progress....\nReset Completed....\n")
        return World.reset()

    @wizard_action("Your spell fails.....\n")
    def lightning(self, target):
        # Parse
        if target is None:
            raise CommandError("There is no one on with that name\n")
        self.send_magic(target, message_codes.LIGHTNING)
        syslog("{} zapped {}".format(self.name, target.name))
        target.get_lightning(self)
        self.broadcast("\001dYou hear an ominous clap of thunder in the distance\n\001")

    def eat(self, item):
        # Parse
        if item is None:
            raise CommandError("There isn't one of those here\n")
        item.eat(self)

    def play(self, item):
        # Parse
        if item is None:
            raise CommandError("That isn't here\n")
        if not self.item_is_available(item):
            raise CommandError("That isn't here\n")
        item.play(self)

    @not_dumb_action
    def shout(self, message):
        # Parse
        self.communicate(-10104 if self.is_wizard else message_codes.SHOUT, message)
        yield "Ok!"

    @not_dumb_action
    def say(self, message):
        # Parse
        self.communicate(message_codes.SAY, message)
        yield "You say '{}'\n".format(message)

    @not_dumb_action
    def tell(self, target, message):
        # Parse
        if target is None:
            raise CommandError("No one with that name is playing\n")
        self.communicate(message_codes.TELL, message, target)

    # 21 - 30
    def save(self):
        # NewUaf
        if self.zapped:
            return
        # self.name = user.name
        # self.score = user.score
        # self.strength = user.strength
        # self.sex = user.sex
        # self.level = user.level
        yield "\nSaving {}\n".format(self.name)
        super().save()

    def show_score(self):
        # Parse
        if self.level == 1:
            yield "Your strength is {}\n".format(self.strength)
            return

        yield "Your strength is {}(from {}),Your score is {}\nThis ranks you as {} ".format(
            self.strength,
            50 + 8 * self.level,
            self.score,
            self.name,
        )
        yield self.level_name
        yield "\n"

    @wizard_action("No chance....\n")
    def exorcise(self, target):
        # Parse
        if target is None:
            raise CommandError("They aren't playing\n")

        target.exorcised()
        syslog("{} exorcised {}".format(self.name, target.name))
        self.send_exorcise(target)

    def give(self, item, target):
        # Parse
        if item is None:
            raise CommandError("You aren't carrying that\n")
        if target is None:
            raise CommandError("I don't know who it is\n")

        if not self.is_wizard and target.location.location_id != self.location.location_id:
            raise CommandError("They are not here\n")
        if not item.is_carried_by(self):
            raise CommandError("You are not carrying that\n")
        if target.overweight:
            raise CommandError("They can't carry that\n")

        item.on_give(self)
        item.set_location(target, item.CARRIED)
        self.send_personal(target, "\001p{}\001 gives you the {}\n".format(self.name, item.name))

    def steal(self, item, target):
        # Parse
        if item is None:
            raise CommandError("They are not carrying that\n")
        if target is None:
            raise CommandError("Who is that ?\n")

        if not self.is_wizard and target.location.location_id != self.location.location_id:
            raise CommandError("But they aren't here\n")
        if item.carry_flag == item.WEARING:
            raise CommandError("They are wearing that\n")
        if target.weapon == item:
            raise CommandError("They have that firmly to hand .. for KILLING people with\n")
        if self.overweight:
            raise CommandError("You can't carry any more\n")

        roll = random_percent()
        chance = (10 + self.level - target.level) * 5
        if roll >= chance:
            raise CommandError("Your attempt fails\n")
        item.set_location(self, item.CARRIED)
        if roll & 1:
            self.send_personal(target, "\001p{}\001 steals the {} from you !\n".format(self.name, item.name))
            target.on_steal(self)

    def levels(self):
        raise NotImplementedError()

    def help(self):
        raise NotImplementedError()

    def value(self):
        raise NotImplementedError()

    def stats(self):
        raise NotImplementedError()

    def examine(self):
        raise NotImplementedError()

    # 31 - 35
    @wizard_action("What ?\n")
    def delete_player(self, target):
        # Magic
        yield "Selection from main menu only\n"
        yield "failed\n"

    def password(self):
        # Magic
        yield "To change your password select option 2 from the main menu\n"

    @wizard_action("You can only summon people\n")
    def summon_item(self, item):
        # Magic
        self.send_global("\001p{}\001 has summoned the {}\n".format(self.name, item.name))
        yield "The {} flies into your hand ,was ".format(item.name)
        desrm(item.location, item.carry_flag)
        item.set_location(self, item.CARRIED)

    def summon_player(self, target):
        # Magic
        if self.strength < 10:
            raise CommandError("You are too weak\n")
        if not self.is_wizard:
            self.strength -= 2

        if self.is_wizard:
            chance = 101
        else:
            chance = self.level * 2

        if Item111.is_carried_by(self):
            chance += self.level
        if Item121.is_carried_by(self):
            chance += self.level
        if Item163.is_carried_by(self):
            chance += self.level

        roll = random_percent()
        if not self.is_wizard:
            if Item90.is_worn_by(target) or chance < roll:
                raise CommandError("The spell fails....\n")
            items = (MagicSword, Item159, Item174)
            if target.player_id == self.find("wraith") or any(item.is_worn_by(target) for item in items):
                raise CommandError("Something stops your summoning from succeeding\n")
            if target.player_id == self.player_id:
                raise CommandError("Seems a waste of effort to me....\n")
            if self.location.anti_summon:
                raise CommandError("Something about this place makes you fumble the magic\n")

        yield "You cast the summoning......\n"
        if not target.is_mobile:
            return self.send_summon(target)
        if target.player_id in (17, 23):
            return
        target.dump_items()
        self.send_global("\001s{name}\001{name} has arrived\n\001".format(name=target.name))
        target.location = self.location

    def wield(self):
        raise NotImplementedError()

    def kill(self):
        raise NotImplementedError()

    # 50
    @not_dumb_action
    def laugh(self):
        # Weather
        self.__silly_sound("falls over laughing")
        yield "You start to laugh\n"

    # 51 - 60
    @not_dumb_action
    def cry(self):
        # Weather
        self.__silly_visual("bursts into tears")
        yield "You burst into tears\n"

    @not_dumb_action
    def burp(self):
        # Weather
        self.__silly_sound("burps loudly")
        yield "You burp rudely\n"

    def fart(self):
        # Weather
        self.__silly_sound("lets off a real rip roarer")
        yield "Fine...\n"
        self.has_farted = True

    @not_dumb_action
    def hiccup(self):
        # Weather
        self.__silly_sound(" hiccups")
        yield "You hiccup\n"

    def grin(self):
        # Weather
        self.__silly_visual("grins evilly")
        yield "You grin evilly\n"

    def smile(self):
        # Weather
        self.__silly_visual("smiles happily")
        yield "You smile happily\n"

    def wink(self):
        # Weather
        self.__silly_visual("winks suggestively")
        yield "You wink\n"

    @not_dumb_action
    def snigger(self):
        # Weather
        self.__silly_sound("sniggers")
        yield "You snigger\n"

    @wizard_action("You are just not up to this yet\n")
    def pose(self):
        # Weather
        pose_id = random_percent() % 5

        yield "POSE :{}\n".format(pose_id)

        if pose_id == 0:
            pass
        elif pose_id == 1:
            self.__silly_visual("throws out one arm and sends a huge bolt of fire high\ninto the sky")
            self.broadcast("\001cA massive ball of fire explodes high up in the sky\n\001")
        elif pose_id == 2:
            self.__silly_visual("turns casually into a hamster before resuming normal shape")
        elif pose_id == 3:
            self.__silly_visual("starts sizzling with magical energy")
        elif pose_id == 4:
            self.__silly_visual("begins to crackle with magical fire")

    @wizard_action("Sorry, wizards only\n")
    def set_item_bit(self, item, bit_id, value):
        # Weather
        if value is None:
            yield "The bit is {}\n".format("TRUE" if item.test_bit(bit_id) else "FALSE")
            return
        else:
            value = int(value)

        if value not in range(2) or bit_id not in range(16):
            raise CommandError("Number out of range\n")

        if not value:
            item.clear_bit(bit_id)
        else:
            item.set_bit(bit_id)

    @wizard_action("Sorry, wizards only\n")
    def set_item_byte(self, item, byte_id, value):
        # Weather
        if value is None:
            yield "Current Value is : {}\n".format(item.get_byte(byte_id))
            return
        else:
            value = int(value)

        if value not in range(256) or byte_id not in range(2):
            raise CommandError("Number out of range\n")

        item.set_byte(byte_id, value)

    @wizard_action("Sorry, wizards only\n")
    def set_item_state(self, item, value):
        # Weather
        if value < 0:
            raise CommandError("States start at 0\n")
        if value > item.max_state:
            raise CommandError("Sorry max state for that is {}\n".format(item.max_state))
        item.state = value

    @wizard_action("Sorry, wizards only\n")
    def set_player_strength(self, player, value):
        # Weather
        if player is None:
            raise CommandError("Set what ?\n")

        if not player.is_mobile:
            raise CommandError("Mobiles only\n")

        player.strength = value

    # 61 - 66
    def pray(self):
        # Weather
        self.__silly_visual("falls down and grovels in the dirt")
        yield "Ok\n"

    @wizard_action("What ?\n")
    def set_weather(self, weather_id):
        # Weather
        # 62-65, 104
        Weather().weather_id = weather_id

    @wizard_action("huh ?\n")
    def go_to_location(self, zone, location_id):
        # Magic
        location = Location.find(self, zone, location_id)
        try:
            if location.location_id >= 0:
                raise ServiceError()
            service = location.load("r")
            service.disconnect()
        except ServiceError:
            raise CommandError("Unknown Room\n")

        self.__silly_visual(self.mout_ms)
        self.location = location
        self.__silly_visual(self.min_ms)

    # 100
    def wear(self, item):
        # New1
        if not item.is_carried_by(self):
            raise CommandError("You are not carrying this\n")
        if item.is_worn_by(self):
            raise CommandError("You are wearing this\n")

        item.on_wear(self)
        if not item.can_wear:
            raise CommandError("Is this a new fashion ?\n")

        item.carry_flag = 2
        yield "OK\n"

    # 101 - 110
    def remove_clothes(self, item):
        # New1
        if item.is_worn_by(self):
            raise CommandError("You are not wearing this\n")
        item.carry_flag = item.CARRIED

    def put(self, item, container):
        # New1
        if container is None:
            raise CommandError("There isn't one of those here.\n")
        container.put_in(item, self)

    def wave(self, item):
        # New1
        item.wave(self)

    # 104 -> set_weather

    def open(self, item):
        # New1
        item.open(self)

    def close(self, item):
        # New1
        item.close(self)

    def lock(self, item):
        # New1
        if not any(item.is_key for item in self.available_items):
            raise CommandError("You haven't got a key\n")
        item.lock(self)

    def unlock(self, item):
        # New1
        if not any(item.is_key for item in self.available_items):
            raise CommandError("You have no keys\n")
        item.unlock(self)

    def force(self, target, action):
        # New1
        self.send_magic(target, message_codes.FORCE, action)

    def light(self, item):
        # New1
        if not any(item.is_light for item in self.available_items):
            raise CommandError("You have nothing to light things from\n")
        item.light(self)

    # 111 - 120
    def extinguish(self, item):
        # New1
        item.extinguish(self)

    def where(self):
        raise NotImplementedError()

    # 113

    @wizard_action("You can't just turn invisible like that!\n")
    def become_invisible(self, value=None):
        # Magic
        if self.level == 10033 and value is not None:
            pass
        elif self.is_god:
            value = 10000
        else:
            value = 10

        if self.visible == value:
            raise CommandError("You are already invisible\n")
        self.visible = value

        self.send_visible()
        yield "Ok\n"
        self.send_silly("\001c{user.name} vanishes!\n\001")

    @wizard_action("You can't just do that sort of thing at will you know.\n")
    def become_visible(self):
        # Magic
        if not self.visible:
            raise CommandError("You already are visible\n")

        self.visible = 0
        self.send_visible()
        yield "Ok\n"
        self.__silly_visual("suddenely appears in a puff of smoke")

    # 116

    def push(self, item):
        # New1
        if item is None:
            raise CommandError("That is not here\n")
        item.push(self)

    def cripple(self, target):
        # New1
        self.send_magic(target, message_codes.CRIPPLE)

    def cure(self, target):
        # New1
        self.send_magic(target, message_codes.CURE)

    def dumb(self, target):
        # New1
        self.send_magic(target, message_codes.DUMB)

    # 121 - 130
    def change(self, target):
        # New1
        self.send_change_sex(target)
        if target.is_mobile:
            return
        target.sex = 1 - target.sex

    def missile(self, target):
        # New1
        power = self.level * 2
        self.send_magic_missile(target, message_codes.BOLT, power)
        if target.strength < power:
            yield "Your last spell did the trick\n"
            if not target.is_dead:
                # Bonus ?
                self.score += target.value
                target.die()  # MARK ALREADY DEAD
            self.Blood.in_fight = 0
            self.Blood.fighting = -1
        if target.is_mobile:
            target.get_damage(self, power)

    def shock(self, target):
        # New1
        if self.player_id == target.player_id:
            raise CommandError("You are supposed to be killing other people not yourself\n")

        power = self.level * 2
        if target.strength < power:
            yield "Your last spell did the trick\n"
            if not target.is_dead:
                # Bonus ?
                self.score += target.value
                target.die()  # MARK ALREADY DEAD
            self.Blood.in_fight = 0
            self.Blood.fighting = -1
        self.send_magic_missile(target, message_codes.SHOCK, power)
        if target.is_mobile:
            target.get_damage(self, power)

    def fireball(self, target):
        # New1
        if self.player_id == target.player_id:
            raise CommandError("Seems rather dangerous to me....\n")

        damage = 6 if target.player_id == Player.find('yeti').player_id else 2
        power = self.level * damage

        if target.strength < power:
            yield "Your last spell did the trick\n"
            if not target.is_dead:
                # Bonus ?
                self.score += target.value
                target.die()  # MARK ALREADY DEAD
            self.Blood.in_fight = 0
            self.Blood.fighting = -1
        self.send_magic_missile(target, message_codes.FIREBALL, power)
        if target.is_mobile:
            target.get_damage(self, power)

    def translocate(self):
        raise NotImplementedError()

    def blow(self, item):
        # New1
        item.blow(self)

    @not_dumb_action
    def sigh(self):
        # New1
        self.__silly_sound("sighs loudly")
        yield "You sigh\n"

    def kiss(self, target):
        # New1
        if target.player_id == self.player_id:
            raise CommandError("Weird!\n")
        self.send_social(target, "kisses you")
        yield "Slurp!\n"

    def hug(self, target):
        # New1
        if target.player_id == self.player_id:
            raise CommandError("Ohhh flowerr!\n")
        self.send_social(target, "hugs you")

    def slap(self, target):
        # New1
        if target.player_id == self.player_id:
            raise CommandError("You slap yourself\n")
        self.send_social(target, "slaps you")

    # 131 - 140
    def tickle(self, target):
        # New1
        if target.player_id == self.player_id:
            raise CommandError("You tickle yourself\n")
        self.send_social(target, "tickles you")

    @not_dumb_action
    def scream(self):
        # New1
        self.__silly_sound("screams loudly")
        yield "ARRRGGGGHHHHHHHHHHHH!!!!!!\n"

    def bounce(self):
        # New1
        self.__silly_visual("bounces around")
        yield "B O I N G !!!!\n"

    @wizard_action("Such advanced conversation is beyond you\n")
    def wizards(self, message):
        # Magic
        self.send_wizard("\001p{}\001 : {}\n".format(self.name, message))
        self.force_read = True

    def stare(self, target):
        # New1
        if target.player_id == self.player_id:
            raise CommandError("That is pretty neat if you can do it!\n")

        self.send_social(target, "stares deep into your eyes\n")
        yield "You stare at \001p{}\001\n".format(target.name)

    def list_exits(self):
        # Zones
        yield "Obvious exits are\n"

        if not len(self.location.visible_exits):
            yield "None....\n"
            return

        for direction_id, location_id in enumerate(self.location.exits):
            if location_id >= 0:
                continue

            location = Location(location_id)
            yield location.directions[direction_id]
            if self.is_wizard:
                yield " : {}".format(location.name)
            yield "\n"

    @wizard_action("Hmmm....\nI expect it will sometime\n")
    def crash(self):
        # Mobile
        yield "Bye Bye Cruel World...\n"
        self.send_evil()
        yield from self.reset_world()

    @not_dumb_action
    def sing(self):
        # Mobile
        self.__silly_sound("sings in Gaelic")
        yield "You sing\n"

    @not_force_action("You can't be forced to do that\n")
    def grope(self, target):
        # New1
        if self.Blood.in_fight:
            raise CommandError("Not in a fight!\n")

        if target.player_id == self.player_id:
            yield "With a sudden attack of morality the machine edits your persona\n"
            self.loose()
            raise CrapupError("Bye....... LINE TERMINATED - MORALITY REASONS")
        self.send_social(target, "gropes you")
        yield "<Well what sort of noise do you want here ?>\n"

    def spray(self, item, target):
        # Mobile
        if item is None:
            raise CommandError("With what ?\n")
        return item.spray(self, target)

    # 141 - 150
    def groan(self):
        # Weather
        self.__silly_sound("groans loudly")
        yield "You groan\n"

    def moan(self):
        # Weather
        self.__silly_sound("starts making moaning noises")
        yield "You start to moan\n"

    @wizard_action("That's a wiz command\n")
    def directory(self):
        # Mobile
        for item in ITEMS:
            if item.is_carried or item.is_worn:
                d = "CARRIED"
            elif item.is_contained:
                d = "IN ITEM"
            else:
                location = item.location
                zone = Zone.find(location)
                d = "{}{}".format(zone.name, zone.in_zone(location))
            yield "{}\t{}".format(item.name, d)
            if item.item_id % 3 == 2:
                yield "\n"
            if item.item_id % 18 == 17:
                self.show_buffer()
        yield "\n"

    def yawn(self):
        # Weather
        self.__silly_sound("yawns")

    def wizlist(self):
        raise NotImplementedError()

    def in_command(self):
        raise NotImplementedError()

    def smoke(self):
        raise NotImplementedError()

    def deafen(self, target):
        # New1
        self.send_magic(target, message_codes.DEAF)

    @wizard_action("Huh ?\n")
    def resurrect(self, item):
        # Magic
        if item is None:
            raise CommandError("You can only resurrect objects\n")
        if not item.is_destroyed:
            raise CommandError("That already exists\n")

        item.create()
        item.set_location(self.location, item.IN_LOCATION)
        self.send_global("The {} suddenly appears\n".format(item.name))

    def log(self):
        raise NotImplementedError()

    # 151 - 160
    @god_action("I don't know that verb\n")
    def tss(self, command):
        # Parse
        if not self.__is_valid_uid:
            raise CommandError("Not permitted on this ID\n")
        World.tss(command)

    def remote_editor(self):
        # Parse
        if not self.can_edit:
            raise CommandError("Dum de dum.....\n")

        self.send_wizard("\001s{name}\001{name} fades out of reality\n\001".format(name=self.name))
        self.__fade_system(World.remote_editor())
        self.send_wizard("\001s{name}\001{name} re-enters the normal universe\n\001".format(name=self.name))

    @wizard_action("Oh go away, that's for wizards\n")
    def list_nodes(self):
        # Zones
        yield "\nKnown Location Nodes Are\n\n"
        for zone_id, zone in enumerate(ZONES):
            yield zone.name
            if zone_id % 4 == 3:
                yield "\n"
        yield "\n"

    def squeeze(self, target):
        # New1
        if target.player_id == self.player_id:
            yield "Ok....\n"
        self.send_social(target, "gives you a squeeze\n")
        yield "You give them a squeeze\n"

    # 155 -> 13

    @wizard_action("You'll have to leave the game first!\n")
    def honeyboard(self):
        # Parse
        self.send_wizard("\001s{name}\001{name} has dropped into BB\n\001".format(name=self.name))
        yield from self.__fade_system(World.honeyboard())

        World.load()
        self.send_wizard("\001s{name}\001{name} has returned to AberMud\n\001".format(name=self.name))

    @god_action("Huh ?\n")
    def item_number(self, item):
        # Parse
        yield "Item Number is {}\n".format(item.item_id)

    @wizard_action("Hmmm... you can't do that one\n")
    def update_system(self):
        # Parse
        self.loose()
        self.send_wizard("[ {} has updated ]\n".format(self.name))
        World.save()

        try:
            execl(EXE, "   --{----- ABERMUD -----}--   ", self.name)  # GOTOSS eek!
        except ServiceError:
            raise CommandError("Eeek! someones pinched the executable!\n")

    @wizard_action("Become what ?\n")
    def become(self, name):
        # Parse
        if not name:
            raise CommandError("To become what ?, inebriated ?\n")

        self.send_wizard("{} has quit, via BECOME\n".format(self.name))

        Keys.off()
        self.loose()
        World.save()

        try:
            execl(EXE2, "   --}----- ABERMUD ------   ", "-n{}".format(self.name))  # GOTOSS eek!
        except ServiceError:
            raise CommandError("Eek! someone's just run off with mud!!!!\n")

    def sys_stat(self):
        # Parse
        if self.level < 10000000:
            raise NotImplementedError("What do you think this is a DEC 10 ?\n")

    # 161 - 170
    def converse(self):
        # Parse
        self.conversation_mode = Parser.CONVERSATION_SAY
        yield "Type '**' on a line of its own to exit converse mode\n"

    def snoop(self):
        raise NotImplementedError()

    @god_action("There is nothing here you can shell\n")
    def shell(self):
        # Parse
        self.conversation_mode = Parser.CONVERSATION_TSS
        yield "Type ** on its own on a new line to exit shell\n"

    @god_action("I don't know that verb\n")
    def raw(self, message):
        # Parse
        if self.level == 10033 and message[0] == "!":
            self.broadcast(message[1:])
        else:
            self.broadcast("** SYSTEM : {}\n\007\007".format(message))

    @not_dumb_action
    def purr(self):
        # Weather
        self.__silly_sound("starts purring")
        yield "MMMMEMEEEEEEEOOOOOOOWWWWWWW!!\n"

    def cuddle(self, target):
        # New1
        if target.player_id == self.player_id:
            raise CommandError("You aren't that lonely are you ?\n")

        self.send_social(target, "cuddles you")

    def sulk(self):
        # Weather
        self.__silly_visual("sulks")
        yield "You sulk....\n"

    def roll(self, item):
        # Parse
        if item is None:
            raise CommandError()
        item.roll(self)

    def credits(self):
        # Parse
        yield "\001f{}\001".format(CREDITS)

    def switch_brief(self):
        # Parse
        self.brief = not self.brief

    # 171 - 180
    @god_action("I don't know that verb\n")
    def debug(self):
        # Parse
        yield "No debugger available\n"

    def jump(self):
        raise NotImplementedError()

    def map_world(self):
        # Parse
        yield "Your adventurers automatic monster detecting radar, and long range\n"
        yield "mapping kit, is, sadly, out of order.\n"

    def flee(self, direction_id):
        # Parse
        if not self.is_fighting:
            return self.go(direction_id)

        yield from map(lambda item: item.on_owner_flee(self, direction_id), self.items)

        self.send_global("\001c{}\001 drops everything in a frantic attempt to escape\n".format(self.name))
        self.send_flee()

        self.score -= self.score / 33  # loose 3%
        yield from self.update()

        self.Blood.in_fight = None
        self.on_flee()

        return self.go(direction_id)

    def bug(self, message):
        # Parse
        syslog("Bug by {} : {}".format(self.name, message))

    def typo(self, message):
        # Parse
        syslog("Typo by {} in {} : {}".format(self.name, self.location.location_id, message))

    def list_pronouns(self):
        # Parse
        yield("Current pronouns are:\n")
        yield("Me              : {}\n".format(self.name))
        yield("Myself          : {}\n".format(self.name))
        yield("It              : {}\n".format(self.pronouns['it']))
        yield("Him             : {}\n".format(self.pronouns['him']))
        yield("Her             : {}\n".format(self.pronouns['her']))
        yield("Them            : {}\n".format(self.pronouns['them']))
        if self.is_wizard:
            yield("There           : {}\n".format(self.pronouns['there']))

    def blind(self, target):
        # New1
        self.send_magic(target, message_codes.BLIND)

    def patch(self):
        raise NotImplementedError()

    def switch_debug(self):
        # Parse
        if not self.can_debug:
            raise CommandError

        self.debug_mode = not self.debug_mode

    # 181 - 189
    def set_player_flags(self, player, flag_id, value):
        # Weather
        if not self.can_set_flags:
            raise CommandError("You can't do that\n")
        if player is None:
            raise CommandError("Who is that ?\n")
        if value is None:
            yield "Value is : {}\n".format("TRUE" if player.test_flag(flag_id) else "FALSE")
            return
        else:
            value = int(value)

        if value not in range(2) or player.player_id not in range(31):
            raise CommandError("Out of range\n")

        if value:
            player.set_flag(flag_id)
        else:
            player.clear_flag(flag_id)

    @god_action("No way buster.\n")
    def frobnicate(self, target):
        # Frob
        if not target.is_mobile and self.level != 10033:
            raise CommandError("Can't frob mobiles old bean.\n")
        if target.is_god and self.level != 10033:
            raise CommandError("You can't frobnicate {}!!!!\n".format(self.name))

        stats = Keys.frobnicate()
        World.load()
        self.send_stats(target, stats)
        yield "Ok....\n"

    @message_action
    def set_in(self, message):
        # Parse
        self.in_ms = message

    @message_action
    def set_out(self, message):
        # Parse
        self.out_ms = message

    @message_action
    def set_magic_in(self, message):
        # Parse
        self.min_ms = message

    @message_action
    def set_magic_out(self, message):
        # Parse
        self.mout_ms = message

    @god_action("Your emotions are strictly limited!\n")
    def emote(self, message):
        # Weather
        self.send_silly("\001P{user.name}\001 " + message + "\n")

    def dig(self):
        # Parse
        self.location.on_dig_here(self)
        yield from map(lambda item: item.on_dig(self), ITEMS)

    def empty(self, container):
        # Parse
        if container is None:
            raise CommandError()

        for item in container.contain(destroyed=self.is_wizard):
            item.set_location(self.location, item.CARRIED)
            yield "You empty the {} from the {}\n".format(item.name, container.name)
            self.drop(item)
            self.show_buffer()
            World.load()
