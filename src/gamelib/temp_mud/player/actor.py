from ..direction import DIRECTIONS
from ..errors import CommandError, CrapupError, LooseError, ServiceError
from ..item.item import Item, Door, Shield89, Shield113, Shield114, ITEMS
from ..location import Location
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


def randperc():
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


def not_dumb_action(f):
    def wrapped(self, *args):
        self.Disease.dumb.check()
        return f(self, *args)
    return wrapped


class Actor(Sender, Reader):
    # Modules
    @property
    def Blood(self):
        raise NotImplementedError()

    @property
    def Disease(self):
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

    def on_flee(self, *args):
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

    # Other
    @property
    def is_fighting(self):
        return self.Blood.in_fight > 0

    def __fade_system(self, actions):
        self.fade()
        self.save_position()
        World.save()

        yield from actions

        self.check_kicked()
        yield from self.read_messages()

    def list_items(self):
        return Item.list_items_at(self, Item.CARRIED, self.debug, self.is_wizard)

    def __silly_sound(self, message):
        self.send_silly("\001P{user.name}\001\001d " + message + "\n\001")

    def __silly_visual(self, message):
        self.send_silly("\001s{user.name}\001{user.name} " + message + "\n\001")

    # 1 - 10
    def go(self, direction):
        # Parse
        # 1 - 7
        if direction is None:
            raise CommandError("That's not a valid direction\n")
        if self.is_fighting:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")
        yield from map(lambda mobile: mobile.on_actor_leave(self, direction), MOBILES)
        self.Disease.crippled.check()

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

    def quit_game(self):
        # Parse
        if self.Disease.is_force:
            raise CommandError("You can't be forced to do that\n")

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

        if self.dragget():
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
            if self.Disease.blind:
                self.Disease.blind.cure()
            if self.is_wizard:
                yield "<DEATH ROOM>\n"
            else:
                raise LooseError("bye bye.....\n")

        if self.Disease.blind:
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

        if not self.Disease.blind:
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
        target.get_lightning()
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

        roll = randperc()
        chance = (10 + self.level - target.level) * 5
        if roll >= chance:
            raise CommandError("Your attempt fails\n")
        item.set_location(self, item.CARRIED)
        if roll & 1:
            self.send_personal(target, "\001p{}\001 steals the {} from you !\n".format(self.name, item.name))
            target.on_steal()

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
    def delete_player(self):
        raise NotImplementedError()

    def password(self):
        raise NotImplementedError()

    def summon(self):
        raise NotImplementedError()

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
        pose_id = randperc() % 5

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

    def go_to(self):
        raise NotImplementedError()

    # 100
    def wear(self):
        raise NotImplementedError()

    # 101 - 110
    def remove_clothes(self):
        raise NotImplementedError()

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

    def become_invisible(self):
        raise NotImplementedError()

    def become_visible(self):
        raise NotImplementedError()

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
    def change(self):
        raise NotImplementedError()

    def missile(self):
        raise NotImplementedError()

    def shock(self):
        raise NotImplementedError()

    def fireball(self):
        raise NotImplementedError()

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

    def kiss(self):
        raise NotImplementedError()

    def hug(self):
        raise NotImplementedError()

    def slap(self):
        raise NotImplementedError()

    # 131 - 140
    def tickle(self):
        raise NotImplementedError()

    @not_dumb_action
    def scream(self):
        # New1
        self.__silly_sound("screams loudly")
        yield "ARRRGGGGHHHHHHHHHHHH!!!!!!\n"

    def bounce(self):
        # New1
        self.__silly_visual("bounces around")
        yield "B O I N G !!!!\n"

    def wiz(self):
        raise NotImplementedError()

    def stare(self):
        raise NotImplementedError()

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

    def crash(self):
        raise NotImplementedError()

    def sing(self):
        raise NotImplementedError()

    def grope(self):
        raise NotImplementedError()

    def spray(self):
        raise NotImplementedError()

    # 141 - 150
    def groan(self):
        # Weather
        self.__silly_sound("groans loudly")
        yield "You groan\n"

    def moan(self):
        # Weather
        self.__silly_sound("starts making moaning noises")
        yield "You start to moan\n"

    def directory(self):
        raise NotImplementedError()

    def yawn(self):
        # Weather
        self.__silly_sound("yawns")

    def wizlist(self):
        raise NotImplementedError()

    def in_command(self):
        raise NotImplementedError()

    def smoke(self):
        raise NotImplementedError()

    def deafen(self):
        raise NotImplementedError()

    def ressurect(self):
        raise NotImplementedError()

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

    def squeeze(self):
        raise NotImplementedError()

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

        # keysetback()
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

    def cuddle(self):
        raise NotImplementedError()

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
        return self.debug2()

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

    def pn(self):
        raise NotImplementedError()

    def blind(self):
        raise NotImplementedError()

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

    def frobnicate(self):
        raise NotImplementedError()

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
