from ..direction import DIRECTIONS
from ..errors import CommandError, CrapupError, LooseError, ServiceError
from ..item import Item, Door
from ..location import Location
from ..message import message_codes
from ..parser import Parser
from ..syslog import syslog
from ..world import World
from .mobile import MOBILES
from .player import Player


EXE = None
EXE2 = None
CREDITS = None


def execl(*args):
    raise NotImplementedError()


def randperc():
    raise NotImplementedError()


def is_door(location_id):
    return 999 < location_id < 2000


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


class Actor:
    @property
    def Blood(self):
        raise NotImplementedError()

    @property
    def Disease(self):
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
    def is_editor(self):
        raise NotImplementedError()

    @property
    def is_wizard(self):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()

    @property
    def location_id(self):
        raise NotImplementedError()

    @location_id.setter
    def location_id(self, value):
        # if value == 0:
        #     self.__location_id = 0
        raise NotImplementedError()

    @property
    def name(self):
        raise NotImplementedError()

    @property
    def strength(self):
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

    @property
    def out_ms(self):
        raise NotImplementedError()

    @property
    def overweight(self):
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

    @property
    def __uid(self):
        raise NotImplementedError()

    @property
    def __is_valid_uid(self):
        return self.__uid == self.__euid

    def debug2(self, *args):
        raise NotImplementedError()

    def die(self, *args):
        raise NotImplementedError()

    def disle3(self, *args):
        raise NotImplementedError()

    def dumpitems(self, *args):
        raise NotImplementedError()

    def fade(self, *args):
        raise NotImplementedError()

    def item_is_available(self, *args):
        raise NotImplementedError()

    def loose(self, *args):
        raise NotImplementedError()

    def on_flee(self, *args):
        raise NotImplementedError()

    def on_look(self, *args):
        raise NotImplementedError()

    def read_messages(self, *args):
        raise NotImplementedError()

    def remove(self, *args):
        raise NotImplementedError()

    def reset_position(self, *args):
        raise NotImplementedError()

    def save_player(self, *args):
        raise NotImplementedError()

    def save_position(self, *args):
        raise NotImplementedError()

    def send_message(self, *args):
        raise NotImplementedError()

    def update(self, *args):
        raise NotImplementedError()

    @property
    def has_shield(self):
        shields = Item(113), Item(114), Item(89)
        return any(item.iswornby(self) for item in shields)

    @property
    def in_fight(self):
        return self.Blood.in_fight > 0

    @property
    def location(self):
        return Location(self.location_id)

    def check_kicked(self):
        self.reset_position()
        World.load()
        if Player.fpbns(self.name) is None:
            raise LooseError("You have been kicked off")

    def __fade_system(self, actions):
        self.fade()
        self.save_position()
        World.save()

        yield from actions

        self.check_kicked()
        yield from self.read_messages()

    # Messages
    def broadcast(self, *args):
        raise NotImplementedError()

    def communicate(self, code, message, target=None):
        target = target or self
        self.send_message(
            target,
            code,
            self.location_id,
            message,
        )

    def __send_exorcise(self, target):
        self.send_message(
            target,
            message_codes.EXORCISE,
            self.location_id,
            None,
        )

    def send_flee(self):
        self.send_message(
            self,
            message_codes.FLEE,
            self.location_id,
            None,
        )

    def send_global(self, message):
        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location_id,
            message,
        )

    def __send_lightning(self, target):
        self.send_message(
            target,
            message_codes.LIGHTNING,
            target.location_id,
            None,
        )

    def send_personal(self, target, message):
        self.send_message(
            target,
            message_codes.PERSONAL,
            self.location_id,
            message,
        )

    def send_wizard(self, message):
        self.send_message(
            self,
            message_codes.WIZARD,
            0,
            message,
        )

    # 1 - 10
    def go(self, direction_id):
        # Parse
        # 1 - 7
        direction = DIRECTIONS.get(direction_id)
        if direction is None:
            raise CommandError("Thats not a valid direction\n")
        if self.in_fight > 0:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")
        location_id = self.location.exits[direction_id]
        yield from map(lambda mobile: mobile.on_actor_leave(self, direction_id), MOBILES)
        self.Disease.crippled.check()
        if is_door(location_id):
            location_id = Door(location_id).go_through(self)
        yield from Location(location_id).on_enter(self)
        yield from map(lambda mobile: mobile.on_actor_enter(self, direction_id, location_id), MOBILES)
        if location_id >= 0:
            raise CommandError("You can't go that way\n")

        self.send_global(
            "\001s{actor.data.name}\001{actor.name} has gone {direction} {message}.\n\001".format(
                actor=self,
                direction=direction,
                message=self.out_ms
            ),
        )
        self.location_id = location_id
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

        if self.in_fight:
            raise CommandError("Not in the middle of a fight!\n")

        yield "Ok"

        World.load()
        self.send_global("{} has left the game\n".format(self.name))
        self.send_wizard("[ Quitting Game : {} ]\n".format(self.name))
        self.dumpitems()
        self.die()
        self.remove()
        World.save()

        self.location_id = 0
        self.show_players = False
        self.save_player()
        raise CrapupError("Goodbye")

    def take(self):
        raise NotImplementedError()

    def drop(self):
        raise NotImplementedError()

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
            return

        yield self.location.short

        if long or not self.brief or self.location.no_brief:
            yield "\n".join(self.location.description)

        World.load()

        if not self.Disease.blind:
            self.location.lisobs()
            if self.show_players:
                self.location.lispeople()
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
        yield from item.aobjsat(3)

    def inventory(self):
        raise NotImplementedError()

    def who(self):
        raise NotImplementedError()

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
        self.__send_lightning(target)
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

    def shout(self, message):
        # Parse
        self.Disease.dumb.check()
        self.communicate(-10104 if self.is_wizard else message_codes.SHOUT, message)
        yield "Ok!"

    def say(self, message):
        # Parse
        self.Disease.dumb.check()
        self.communicate(message_codes.SAY, message)
        yield "You say '{}'\n".format(message)

    def tell(self, target, message):
        # Parse
        self.Disease.dumb.check()
        if target is None:
            raise CommandError("No one with that name is playing\n")
        self.communicate(message_codes.TELL, message, target)

    # 21 - 30
    def save(self):
        raise NotImplementedError()

    def show_score(self):
        # Parse
        if self.level == 1:
            yield "Your strength is {}\n".format(self.strength)
            return

        yield "Your strength is {}(from {}),Your score is {}\nThis ranks you as %s ".format(
            self.strength,
            50 + 8 * self.level,
            self.score,
            self.name,
        )
        yield self.disle3(self.level, self.sex)

    @wizard_action("No chance....\n")
    def exorcise(self, target):
        # Parse
        if target is None:
            raise CommandError("They aren't playing\n")

        target.exorcised()
        syslog("{} exorcised {}".format(self.name, target.name))
        self.__send_exorcise(target)

    def give(self, item, target):
        # Parse
        if item is None:
            raise CommandError("You aren't carrying that\n")
        if target is None:
            raise CommandError("I don't know who it is\n")

        if not self.is_wizard and target.location_id != self.location_id:
            raise CommandError("They are not here\n")
        if not item.iscarrby(self):
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

        if not self.is_wizard and target.location_id != self.location_id:
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
    def laugh(self):
        raise NotImplementedError()

    # 51 - 60
    def cry(self):
        raise NotImplementedError()

    def burp(self):
        raise NotImplementedError()

    def fart(self):
        raise NotImplementedError()

    def hiccup(self):
        raise NotImplementedError()

    def grin(self):
        raise NotImplementedError()

    def smile(self):
        raise NotImplementedError()

    def wink(self):
        raise NotImplementedError()

    def snigger(self):
        raise NotImplementedError()

    def pose(self):
        raise NotImplementedError()

    def set(self):
        raise NotImplementedError()

    # 61 - 66
    def pray(self):
        raise NotImplementedError()

    def storm(self):
        raise NotImplementedError()

    def rain(self):
        raise NotImplementedError()

    def sun(self):
        raise NotImplementedError()

    def snow(self):
        raise NotImplementedError()

    def go_to(self):
        raise NotImplementedError()

    # 100
    def wear(self):
        raise NotImplementedError()

    # 101 - 110
    def remove_clothes(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()

    def wave(self):
        raise NotImplementedError()

    def blizzard(self):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def lock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()

    def force(self):
        raise NotImplementedError()

    def light(self):
        raise NotImplementedError()

    # 111 - 120
    def extinguish(self):
        raise NotImplementedError()

    def where(self):
        raise NotImplementedError()

    # 113

    def invisible(self):
        raise NotImplementedError()

    def visible(self):
        raise NotImplementedError()

    # 116

    def push(self):
        raise NotImplementedError()

    def cripple(self):
        raise NotImplementedError()

    def cure(self):
        raise NotImplementedError()

    def dumb(self):
        raise NotImplementedError()

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

    def blow(self):
        raise NotImplementedError()

    def sigh(self):
        raise NotImplementedError()

    def kiss(self):
        raise NotImplementedError()

    def hug(self):
        raise NotImplementedError()

    def slap(self):
        raise NotImplementedError()

    # 131 - 140
    def tickle(self):
        raise NotImplementedError()

    def scream(self):
        raise NotImplementedError()

    def bounce(self):
        raise NotImplementedError()

    def wiz(self):
        raise NotImplementedError()

    def stare(self):
        raise NotImplementedError()

    def exits(self):
        raise NotImplementedError()

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
        raise NotImplementedError()

    def moan(self):
        raise NotImplementedError()

    def directory(self):
        raise NotImplementedError()

    def yawn(self):
        raise NotImplementedError()

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
        if not self.is_editor:
            raise CommandError("Dum de dum.....\n")

        self.send_wizard("\001s{name}\001{name} fades out of reality\n\001".format(name=self.name))
        self.__fade_system(World.remote_editor())
        self.send_wizard("\001s{name}\001{name} re-enters the normal universe\n\001".format(name=self.name))

    def loc(self):
        raise NotImplementedError()

    def squeeze(self):
        raise NotImplementedError()

    def users(self):
        raise NotImplementedError()

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
        yield "Item Number is {}\n".format(item)

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

    def purr(self):
        raise NotImplementedError()

    def cuddle(self):
        raise NotImplementedError()

    def sulk(self):
        raise NotImplementedError()

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
        if not self.Blood.in_fight:
            return self.go(direction_id)

        if Item(32).iscarrby(self):
            raise CommandError("The sword won't let you!!!!\n")

        self.send_global("\001c{}\001 drops everything in a frantic attempt to escape\n".format(self.name))
        self.send_flee()

        self.score -= self.score / 33  # loose 3%
        yield from self.update()

        self.Blood.in_fight = None
        self.on_flee()

        return self.go(direction_id)

    def bug(self):
        raise NotImplementedError()

    def typo(self):
        raise NotImplementedError()

    def pn(self):
        raise NotImplementedError()

    def blind(self):
        raise NotImplementedError()

    def patch(self):
        raise NotImplementedError()

    def debugmode(self):
        raise NotImplementedError()

    # 181 - 189
    def pflags(self):
        raise NotImplementedError()

    def frobnicate(self):
        raise NotImplementedError()

    def setin(self):
        raise NotImplementedError()

    def setout(self):
        raise NotImplementedError()

    def setmin(self):
        raise NotImplementedError()

    def setmout(self):
        raise NotImplementedError()

    def emote(self):
        raise NotImplementedError()

    def dig(self):
        raise NotImplementedError()

    def empty(self):
        raise NotImplementedError()
