from datetime import datetime
from ..direction import DIRECTIONS
from ..errors import CrapupError, LooseError, CommandError, ServiceError
from ..item import Item, Door
from ..location import Location
from ..message import message_codes
from ..message.message import Message, Broadcast, Silly
from ..message.process import handle
from ..syslog import syslog
from ..world import World
from .base_player import BasePlayer
from .player import Player


class User(BasePlayer):
    def __init__(self, name):
        self.player_id = 0
        self.__name = name
        self.__data = None

        self.before_message = lambda message: None

        self.__in_setup = False
        self.__position = -1
        self.__location_id = 0
        self.__force_read = False
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

        # Unknown
        self.has_farted = False

        # makebfr()
        self.reset_position()
        self.add()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def location_id(self):
        return self.__location_id

    @location_id.setter
    def location_id(self, value):
        self.__location_id = value
        World.load()
        self.__player.location = value
        self.look()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def strength(self):
        raise NotImplementedError()

    @strength.setter
    def strength(self, value):
        raise NotImplementedError()

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
    def level(self):
        raise NotImplementedError()

    @level.setter
    def level(self, value):
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

    @property
    def sex(self):
        raise NotImplementedError()

    @sex.setter
    def sex(self, value):
        raise NotImplementedError()

    @property
    def is_mobile(self):
        raise NotImplementedError()

    @property
    def __location(self):
        return Location(self.location_id)

    @property
    def __player(self):
        return Player(self.player_id)

    # Weather
    @property
    def __items(self):
        return [item for item in Item.items() if not item.is_destroyed and item.is_carried_by(self)]

    @property
    def __available_items(self):
        return [item for item in Item.items() if item.is_carried_by(self) or item.is_here(self)]

    @property
    def overweight(self):
        if self.capacity is None:
            return False
        return len(self.__items) >= self.capacity

    @property
    def in_dark(self):
        if self.is_wizard:
            return False
        if not self.__location.is_dark:
            return False
        for item in (item for item in Item.items() if item.is_light):
            if self.is_here(item):
                return False
            if item.owner is not None and item.owner.location_id == self.location_id:
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
    def start_location_id(cls):
        return -5 if randperc() > 50 else -183

    # Unknown
    def chksnp(self, *args):
        raise NotImplementedError()

    def initme(self, *args):
        raise NotImplementedError()

    def is_here(self, *args):
        raise NotImplementedError()

    def delpers(self, *args):
        raise NotImplementedError()

    def disle3(self, *args):
        raise NotImplementedError()

    def dumpitems(self, *args):
        raise NotImplementedError()

    def dumpstuff(self, *args):
        raise NotImplementedError()

    def lisobs(self, *args):
        raise NotImplementedError()

    def lispeople(self, *args):
        raise NotImplementedError()

    def on_look(self, *args):
        raise NotImplementedError()

    def save(self, *args):
        raise NotImplementedError()

    # Support
    def item_is_available(self, item):
        if self.is_here(item):
            return True
        return item.is_carried_by(self)

    # Tk
    def add(self):
        World.load()
        if Player.fpbn(self.name) is not None:
            raise CrapupError("You are already on the system - you may only be on once at a time")

        self.player_id = Player.new_player_id()
        if self.player_id is None:
            raise CrapupError("\nSorry AberMUD is full at the moment\n")

        # self.data.name = self.name
        # self.data.location_id = self.location
        # self.data.position = self.position
        self.level = 1
        self.visible = 0
        self.strength = -1
        self.weapon = None
        self.sex = 0
        self.__data = self

    def check_fight(self):
        self.Blood.check_fight()
        if self.Blood.fighting and  self.Blood.get_enemy().location != self.location_id:
            self.Blood.stop_fight()

        if self.Blood.in_fight:
            self.Blood.in_fight -= 1

    # Parse
    def __check_kick(self):
        self.reset_position()
        World.load()
        if Player.fpbns(self.name) is None:
            raise LooseError("You have been kicked off")

    # Tk
    def fade_system(self, message, actions):
        self.send_message(
            self,
            message_codes.WIZARD,
            0,
            message,
        )
        self.fade()
        self.save_position()
        World.save()

        yield from actions

        self.__check_kick()
        yield from self.read_messages()

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
        self.send_message(
            self,
            message_codes.WIZARD,
            self.location_id,
            "[ \001p{}\001 has just been zapped by \001p{}\001 and terminated ]\n".format(
                self.name,
                wizard.name,
            ),
        )

        yield " you between\nthe eyes\n"
        self.zapped = True
        self.delpers()
        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location_id,
            "\001s{user}\001{user} has just died.\n\001".format(user=self.name),
        )

        yield "You have been utterly destroyed by {}\n".format(wizard.name)
        raise LooseError("Bye Bye.... Slain By Lightning")

    # Tk
    def look(self, full=False):
        World.save()

        if self.Disease.blind:
            yield "You are blind... you can't see a thing!\n"

        self.__location.reload()

        if self.is_wizard:
            yield self.__location.get_name(self)

        if self.in_dark:
            yield "It is dark\n"
            return

        if self.__location.death_room:
            if self.Disease.blind:
                self.Disease.blind.cure()
            if self.is_wizard:
                yield "<DEATH ROOM>\n"
            else:
                raise LooseError("bye bye.....\n")

        yield self.__location.short

        brief = self.__brief and not full and not self.__location.no_brief
        if not self.Disease.blind and not brief:
            yield "\n".join(self.__location.description)

        World.load()

        if not self.Disease.blind:
            self.lisobs()
            if self.show_players:
                self.lispeople()
        yield "\n"

        self.on_look()

    def loose(self):
        # sig_aloff()
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.__in_setup = False

        World.load()
        self.dumpitems()
        if self.visible < 10000:
            self.send_message(
                self,
                message_codes.WIZARD,
                0,
                "{} has departed from AberMUDII\n".format(self.name)
            )
        self.remove()
        World.save()

        if not self.zapped:
            self.save()
        self.chksnp()

    # Parse
    def on_messages(self):
        time = datetime.now()
        if (time - self.__last_interrupt).total_seconds() > 2:
            self.interrupt = True
        if self.interrupt:
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

        self.Disease.force.check()

        if self.__drunk_counter > 0:
            self.__drunk_counter -= 1
            if not self.Disease.dumb:
                gamecom("hiccup")

        self.__is_summoned = False
        self.__rdes = 0
        self.__vdes = 0
        self.interrupt = False

    def save_position(self):
        if abs(self.position - self.__position_saved) < 10:
            return

        World.load()
        # self.__data = self
        self.__position_saved = self.position

    def start(self):
        location_id = self.start_location_id()
        self.initme()

        World.load()
        self.visible = 0 if not self.is_god else 10000
        super().start()

        self.send_message(
            self,
            message_codes.WIZARD,
            location_id,
            "\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self.name),
        )

        yield from self.read_messages(reset_after_read=True)
        self.location_id = location_id

        self.send_message(
            self,
            message_codes.GLOBAL,
            location_id,
            "\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self.name),
        )

    # Parse
    def __summoned(self, location):
        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location_id,
            "\001s{name}\001{name} vanishes in a puff of smoke\n\001".format(name=self.name),
        )
        self.dumpitems()
        self.send_message(
            self,
            message_codes.GLOBAL,
            location,
            "\001s{name}\001{name} appears in a puff of smoke\n\001".format(name=self.name),
        )
        self.location_id = location

    def switch_brief(self):
        self.__brief = not self.__brief

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
            self.disle3(level, self.sex)
            self.send_message(
                self,
                message_codes.WIZARD,
                self.location_id,
                "\001p{}\001 is now level {}\n".format(self.name, self.level),
            )
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
        if enemy.location != self.location_id:
            self.Blood.stop_fight()
        if not enemy.exists:
            self.Blood.stop_fight()
        if self.Blood.in_fight and self.interrupt:
            self.Blood.in_fight = 0
            hitplayer(enemy, self.__wpnheld)

    # Messages
    # Tk
    def send_message(self, to_user, code, channel_id, message):
        Message(to_user, self, code, channel_id, message).send(self)

    def broadcast(self, message):
        self.__force_read = True
        Broadcast(message).send(self)

    # Weather
    def silly(self, message):
        Silly(self, message).send(self)

    # Tk
    def __get_messages(self):
        try:
            World.load()
            return Message.messages(self.position)
        except ServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def read_messages(self, unique=False, reset_after_read=False):
        if unique and self.__force_read:
            return

        for message in self.__get_messages():
            yield from self.before_message(message)
            yield from handle(self, message)
        self.save_position()

        yield from self.on_messages()

        if reset_after_read:
            self.reset_position()
        if unique:
            self.__force_read = False

    # For actions
    # Parse
    def go(self, direction_id):
        if self.Blood.in_fight > 0:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")

        treasure = Item(32)
        golem = Player(25)
        if golem.exists and golem.location == self.location_id and treasure.iscarrby(self):
            raise CommandError("\001cThe Golem\001 bars the doorway!\n")

        self.Disease.crippled.check()

        new_location = self.location.exits[direction_id]

        if 999 < new_location < 2000:
            door = Door(new_location)
            new_location = door.go_through()
            if new_location >= 0:
                if self.in_dark or door.invisible:
                    raise CommandError("You can't go that way\n")  # Invis doors
                else:
                    raise CommandError("The door is not open\n")

        if new_location == -139:
            shields = Item(113), Item(114), Item(89)
            if any(item.iswornby(self) for item in shields):
                yield "The shield protects you from the worst of the lava stream's heat\n"
            else:
                raise CommandError("The intense heat drives you back\n")

        # Direction::on_go
        if direction_id == 2:
            sorcerors = Item(101), Item(102), Item(103)
            figure = Player.fpbns("figure")
            if figure is not None and figure != self and figure.location == self.location_id:
                if any(item.iswornby(self) for item in sorcerors):
                    raise CommandError("\001pThe Figure\001 holds you back\n"
                                       "\001pThe Figure\001 says 'Only true sorcerors may pass'\n")

        if new_location >= 0:
            raise CommandError("You can't go that way\n")

        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location_id,
            "\001s{user.player.name}\001{user.name} has gone {direction} {message}.\n\001".format(
                user=self,
                direction=DIRECTIONS[direction_id],
                message=self.__out_ms
            ),
        )
        self.send_message(
            self,
            message_codes.GLOBAL,
            new_location,
            "\001s{user.name}\001{user.name}{message}.\n\001".format(
                user=self,
                direction=DIRECTIONS[direction_id],
                message=self.__out_ms
            ),
        )
        self.location_id = new_location

    def quit_game(self):
        if self.Disease.is_force:
            raise CommandError("You can't be forced to do that\n")

        yield from self.read_messages()

        if self.Blood.in_fight:
            raise CommandError("Not in the middle of a fight!\n")

        yield "Ok"

        World.load()
        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location_id,
            "{} has left the game\n".format(self.name)
        )
        self.send_message(
            self,
            message_codes.WIZARD,
            0,
            "[ Quitting Game : {} ]\n".format(self.name)
        )
        self.dumpitems()
        self.die()
        self.remove()
        World.save()

        self.__location_id = 0
        self.show_players = False

    def lightning(self, victim):
        if victim is None:
            raise CommandError("There is no one on with that name\n")
        self.send_message(victim.name, -10001, victim.location, "")
        syslog("{} zapped {}".format(self.name, victim.name))

        if victim.is_mobile:
            woundmn(victim, 10000)
            # DIE

        self.broadcast("\001dYou hear an ominous clap of thunder in the distance\n\001")

    def eat(self, item):
        if item is None:
            raise CommandError("There isn't one of those here\n")
        elif item.item_id == 11:
            yield "You feel funny, and then pass out\n"
            yield "You wake up elsewhere....\n"
            self.teleport(-1076)
        elif item.item_id == 75:
            yield "very refreshing\n"
        elif item.item_id == 175:
            if self.level < 3:
                self.score += 40
                yield "You feel a wave of energy sweeping through you.\n"
            else:
                yield "Faintly magical by the taste.\n"
                if self.strength < 40:
                    self.strength += 2
            yield from self.update()
        else:
            if item.is_edible:
                item.destroy()
                yield "Ok....\n"
                self.strength += 12
                yield from self.update()
            else:
                yield "Thats sure not the latest in health food....\n"

    def play(self, item):
        if item is None:
            raise CommandError("That isn't here\n")
        if not self.item_is_available(item):
            raise CommandError("That isn't here\n")

    def shout(self, text):
        self.Disease.dumb.check()
        self.send_message(
            self,
            -10104 if self.is_wizard else -10002,
            self.location_id,
            text,
        )
        yield "Ok!"

    def say(self, text):
        self.Disease.dumb.check()
        self.send_message(
            self,
            -10003,
            self.location_id,
            text,
        )
        yield "You say '{}'\n".format(text)

    def tell(self, player, text):
        self.Disease.dumb.check()
        if player is None:
            raise CommandError("No one with that name is playing\n")
        self.send_message(player, -10004, self.location_id, text)

    def show_score(self):
        if self.level == 1:
            yield "Your strength is {}\n".format(self.strength)
            return

        yield "Your strength is {}(from {}),Your score is {}\nThis ranks you as %s ".format(
            self.strength,
            50 + 8 * self.level,
            self.score,
            self.name,
        )
        yield disle3(self.level, self.sex)

    def exorcise(self, player):
        if player is None:
            raise CommandError("They aren't playing\n")
        if player.tstflg(1):
            raise CommandError("You can't exorcise them, they dont want to be exorcised\n")
        syslog("{} exorcised {}".format(self.name, player.name))
        self.dumpstuff(player, player.location)
        self.send_message(
            player,
            -10010,
            self.location_id,
            ""
        )
        player.remove()

    def give(self, item, player):
        if item is None:
            raise CommandError("You aren't carrying that\n")
        if player is None:
            raise CommandError("I don't know who it is\n")

        if not self.is_wizard and player.location_id != self.location_id:
            raise CommandError("They are not here\n")
        if not item.iscarrby(self):
            raise CommandError("You are not carrying that\n")
        if player.overweight:
            raise CommandError("They can't carry that\n")
        if not self.is_wizard and item.item_id == 32:
            raise CommandError("It doesn't wish to be given away.....\n")
        item.set_location(player, 1)
        self.send_message(
            player,
            -10011,
            self.location_id,
            "\001p{}\001 gives you the {}\n".format(self.name, item.name),
        )

    def steal(self, item, player):
        if item is None:
            raise CommandError("They are not carrying that\n")
        if player is None:
            raise CommandError("Who is that ?\n")

        if not self.is_wizard and player.location_id != self.location_id:
            raise CommandError("But they aren't here\n")
        if item.carry_flag == 2:
            raise CommandError("They are wearing that\n")
        if player.weapon == item:
            raise CommandError("They have that firmly to hand .. for KILLING people with\n")
        if self.overweight:
            raise CommandError("You can't carry any more\n")

        roll = randperc()
        chance = (10 + self.level - player.level) * 5
        if roll >= chance:
            raise CommandError("Your attempt fails\n")
        if roll & 1:
            self.send_message(
                player,
                -10011,
                self.location_id,
                "\001p{}\001 steals the {} from you !\n".format(self.name, item.name),
            )
            if player.is_mobile:
                woundmn(player, 0)
        item.setoloc(self, 1)

    def on_after_editor(self):
        self.send_message(
            self,
            message_codes.WIZARD,
            0,
            "\001s{name}\001{name} re-enters the normal universe\n\001".format(name=self.name),
        )

    def on_after_system(self):
        World.load()
        self.send_message(
            self,
            message_codes.WIZARD,
            0,
            "\001s{name}\001{name} has returned to AberMud\n\001".format(name=user.name),
        )
