from .errors import CrapupError, ServiceError, CommandError, LooseError
from .item import Item, Door
from .location import Location
from .message import Broadcast, Message, Silly
from .player import Player
from .world import World


DIRECTIONS = [
    "north",
    "east",
    "south",
    "west",
    "up",
    "down",
]


class User:
    wd_there = ""

    class NewUaf:
        level = 0
        score = 0
        sex = 0
        strength = 0

    class Blood:
        fighting = None
        in_fight = 0

        @classmethod
        def stop_fight(cls):
            cls.in_fight = 0
            cls.fighting = None

    def __init__(self, name):
        self.in_setup = False

        self.has_farted = False
        self.__player_id = None

        self.__location_id = 0

        self.__is_on = False

        self.__updated = 0

        self.rd_qd = False

        # Parse
        self.__in_ms = "has arrived."
        self.__out_ms = ""
        self.__mout_ms = "vanishes in a puff of smoke."
        self.__min_ms = "appears with an ear-splitting bang."
        self.__here_ms = "is here"

        self.__tdes = 0
        self.__vdes = 0
        self.__rdes = 0
        self.__ades = 0
        self.zapped = False

        self.__message_id = None
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def is_wizard(self):
        return self.NewUaf.level > 9

    @property
    def is_god(self):
        return self.NewUaf.level > 9999

    @property
    def can_carry(self):
        max_items = self.max_items
        if max_items is None:
            return True
        return sum(not item.is_destroyed and item.is_carried_by(self.player) for item in Item.items()) < max_items

    @property
    def is_dark(self):
        if self.is_wizard:
            return False
        if not self.location.is_dark:
            return False
        for item in (item for item in Item.items() if item.is_light):
            if is_here(item):
                return False
            if item.owner is not None and item.owner.location == self.__location_id:
                return False
        return True

    @property
    def location(self):
        return Location(self.__location_id)

    @property
    def max_items(self):
        if not self.player.is_wizard:
            return None
        if self.player.level < 0:
            return None
        return self.player.level + 5

    @property
    def player(self):
        return Player(self.__player_id)

    def set_wd_there(self, zone, location_id):
        self.wd_there = zone + " " + location_id

    @property
    def enemy(self):
        return Player(self.Blood.fighting)

    def check_fight(self):
        if self.Blood.fighting is not None:
            if not self.enemy.exists:
                self.Blood.stop_fight()
            if self.enemy.location != self.__location_id:
                self.Blood.stop_fight()

        if self.Blood.in_fight:
            self.Blood.in_fight -= 1

    def read_messages(self, reset_after_read=False):
        yield from self.get_messages()

        self.update()
        eorte()
        rdes = 0
        tdes = 0
        vdes = 0
        if reset_after_read:
            self.__message_id = None

    def reset_location_id(self, is_random=False):
        if is_random:
            self.__location_id = -5 if randperc() > 50 else -183
        else:
            self.__location_id = -5

    def reset_message_id(self):
        self.__message_id = None
        self.__put_on()

    def go_to_channel(self, channel_id):
        World.load()
        self.player.location = channel_id
        self.look_in(self.location)

    def __put_on(self):
        self.__is_on = False
        World.load()
        if Player.fpbn(self.name) is not None:
            raise CrapupError("You are already on the system - you may only be on once at a time")

        self.__player_id = next((player.player_id for player in PLAYERS if not player.is_alive), None)
        if self.__player_id is None:
            raise CrapupError("\nSorry AberMUD is full at the moment\n")

        self.player.put_on(self.name, self.__location_id, self.__message_id)
        self.__is_on = True

    def loose(self):
        sig_aloff()
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        self.in_setup = False

        World.load()
        dumpitems()
        if self.player.visible < 10000:
            self.send_message(
                self,
                Message.WIZARD,
                0,
                "{} has departed from AberMUDII\n".format(self.name)
            )
        self.player.remove()
        World.save()

        if not self.zapped:
            saveme()
        chksnp()

    def update(self):
        if abs(self.__message_id - self.__updated) < 10:
            return

        World.load()
        self.player.position = self.__message_id
        self.__updated = self.__message_id

    def look_in(self, location):
        World.save()

        if self.__ail_blind:
            yield "You are blind... you can't see a thing!\n"

        if self.is_wizard:
            location.show_name(self)

        try:
            un1 = openroom(location.location_id, "r")
            # xx1
            xxx = False
            location.load_exits(un1)
            if self.is_dark:
                fclose(un1)
                yield "It is dark\n"

                World.load()
                on_look()
                return

            for s in un1:
                if s == "#DIE":
                    if self.__ail_blind:
                        rewind(un1)
                        self.__ail_blind = False
                        # xx1()
                    elif self.NewUaf.level > 9:
                        yield "<DEATH ROOM>\n"
                    else:
                        self.loose()
                        raise CrapupError("bye bye.....\n")
                elif s  == "#NOBR":
                    self.brief = False
                    xxx = self.brief
                else:
                    if not self.__ail_blind and not xxx:
                        yield "{}\n".format(s)
                    xxx = self.brief
        except FileNotFoundError:
            yield "\nYou are on channel {}\n".format(location.location_id)
        fclose(un1)

        World.load()
        if not self.__ail_blind:
            lisobs()
            if self.mode == 1:
                lispeople()
        yield "\n"
        on_look()

    # Support
    def is_available(self, item):
        if self.is_here(item):
            return True
        return item.is_carried_by(self.player)

    def has_any(self, mask):
        items = Item.items()
        items = (item for item in items if item.is_carried_by(self.__player_id) or item.is_here(self.__player_id))
        return any(item for item in items if item.test_mask(mask))

    # Unknown
    # Messages
    def send_message(self, to_user, code, channel_id, message):
        Message(to_user, self, code, channel_id, message).send(self)

    def broadcast(self, message):
        self.rd_qd = True
        Broadcast(message).send(self)

    def silly(self, message):
        Silly(self, message).send(self)

    def get_messages(self):
        try:
            World.load()
            return Message.messages(self.__message_id)
        except ServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def process_messages(self, *messages):
        for message in messages:
            self.__message_id = message.message_id
            if message.code < -3:
                yield from process_message(message, self.name.lower())
            else:
                yield message.text

    # For actions
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
            Message.GLOBAL,
            self.__location_id,
            "{} has left the game\n".format(self.name)
        )
        self.send_message(
            self,
            Message.WIZARD,
            0,
            "[ Quitting Game : {} ]\n".format(self.name)
        )
        dumpitems()
        self.player.die()
        self.player.remove()
        World.save()
        self.__location_id = 0

    def flee(self):
        if not self.Blood.in_fight:
            return

        if Item(32).iscarrby(self.__player_id):
            raise CommandError("The sword won't let you!!!!\n")

        self.send_message(
            self,
            Message.GLOBAL,
            self.__location_id,
            "\001c{}\001 drops everything in a frantic attempt to escape\n".format(self.name),
        )
        self.send_message(
            self,
            Message.FLEE,
            self.__location_id,
            "",
        )

        self.NewUaf.score -= self.NewUaf.score / 33  # loose 3%
        self.calibme()
        self.Blood.in_fight = None
        self.on_flee_event()

    def go_in_direction(self, direction_id):
        if self.Blood.in_fight > 0:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")

        golem = Player(25)
        if Item(32).iscarrby(self.player) and golem.exists and golem.location == self.__location_id:
            raise CommandError("\001cThe Golem\001 bars the doorway!\n")

        self.Disease.crippled.check()

        new_location = self.location.exits[direction_id]
        if 999 < new_location < 2000:
            door = Door(new_location)
            new_location = door.go_through()
            if new_location >= 0:
                if self.is_dark or door.invisible:
                    raise CommandError("You can't go that way\n")  # Invis doors
                else:
                    raise CommandError("The door is not open\n")
        if new_location == -139:
            shields = Item(113), Item(114), Item(89)
            if any(item.iswornby(self.player) for item in shields):
                yield "The shield protects you from the worst of the lava stream's heat\n"
            else:
                raise CommandError("The intense heat drives you back\n")
        if direction_id == 2:
            sorcerors = Item(101), Item(102), Item(103)
            figure = Player.fpbns("figure")
            if figure is not None and figure.player_id != self.__player_id and figure.location == self.__location_id:
                if any(item.iswornby(self.player) for item in sorcerors):
                    raise CommandError("\001pThe Figure\001 holds you back\n"
                                       "\001pThe Figure\001 says 'Only true sorcerors may pass'\n")
        if new_location >= 0:
            raise CommandError("You can't go that way\n")

        self.send_message(
            self,
            Message.GLOBAL,
            self.__location_id,
            "\001s{user.player.name}\001{user.name} has gone {direction} {user.out_ms}.\n\001".format(
                user=self,
                direction=DIRECTIONS[direction_id],
            ),
        )
        self.__location_id = new_location
        self.send_message(
            self,
            Message.GLOBAL,
            self.__location_id,
            "\001s{user.name}\001{user.name}{user.in_ms}.\n\001".format(
                user=self,
                direction=DIRECTIONS[direction_id],
            ),
        )
        self.go_to_channel(self.__location_id)

    # Receive
    def process_message(self, message):
        is_me = message.is_my(self.name.lower())
        name1 = message.user_to
        name2 = message.user_from
        text = message.message

        if message.code == Message.FLEE and Player.fpbn(message.user_to) == self.Blood.fighting:
            self.Blood.stop_fight()
        if message.code < -10099:
            return new1rcv(
                is_me,
                message.channel_id,
                message.user_to,
                message.user_from,
                message.code,
                message.message,
            )

        if message.code == Message.STOP_SNOOP:
            if not is_me:
                return
            self.snoopd = None
        if message.code == Message.START_SNOOP:
            if not is_me:
                return
            self.snoopd = Player.fpbns(message.user_from)
        elif message.code == Message.CHANGE_STATS:
            if not is_me:
                return
            self.NewUaf.level, self.NewUaf.score, self.NewUaf.strength = message.message
            self.calibme()
        elif message.code == Message.TOO_EVIL:
            yield "Something Very Evil Has Just Happened...\n"
            raise LooseError("Bye Bye Cruel World....")
        elif message.code == -750:
            if not is_me:
                return
            if Player.fpbns(message.user_from) is not None:
                self.loose()
            World.save()
            print("***HALT\n")
            raise SystemExit(0)
        elif message.code == -9900:
            Player(message.message[0]).visible = message.message[1]
        elif message.code == Message.GLOBAL:
            if is_me:
                return
            if message.channel_id != self.__location_id:
                return
            yield message.message
        elif message.code == -10001:
            if not is_me:
                if message.channel_id == self.__location_id:
                    yield "\001cA massive lightning bolt strikes \001\001D{}\001\001c\n\001".format(message.user_to)
                return
            if self.is_wizard:
                yield "\001p{}\001 cast a lightning bolt at you\n".format(message.user_from)
                return
            # You are in the ....
            yield "A massive lightning bolt arcs down out of the sky to strike"
            self.send_message(
                self,
                Message.WIZARD,
                self.__location_id,
                "[ \001p{}\001 has just been zapped by \001p{}\001 and terminated ]\n".format(
                    self.name,
                    message.user_from,
                ),
            )
            yield " you between\nthe eyes\n"
            self.zapped = True
            delpers(self)
            self.send_message(
                self,
                Message.GLOBAL,
                self.__location_id,
                "\001s{user}\001{user} has just died.\n\001".format(user=self.name),
            )
            yield "You have been utterly destroyed by {}\n".format(message.user_from)
            raise LooseError("Bye Bye.... Slain By Lightning")
        elif message.code == -10002:
            if is_me:
                return
            if self.__location_id == message.channel_id or self.is_wizard:
                yield "\001P{}\001\001d shouts '{}'\n\001".format(message.user_from, message.message)
            else:
                yield "\001dA voice shouts '{}'\n\001".format(message.message)
        elif message.code == -10003:
            if is_me:
                return
            if message.channel_id != self.__location_id:
                return
            yield "\001P{}\001\001d says '{}'\n\001".format(message.user_from, message.message)
        elif message.code == -10004:
            if not is_me:
                return
            yield "\001P{}\001\001d tells you '{}'\n\001".format(message.user_from, message.message)
        elif message.code == -10010:
            if is_me:
                raise LooseError("You have been kicked off")
            yield "{} has been kicked off\n".format(message.user_to)
        elif message.code == -10011:
            yield message.message
        elif message.code == -10020:
            if not is_me:
                return
            yield "\001P{}\001\001d tells you '{}'\n\001".format(message.user_from, message.message)
        elif message.code == -10021:
            if message.channel_id != self.__location_id:
                return
            if not is_me:
                return
            self.rdes = 1
            self.vdes = message.message[0]
            bloodrcv(message.message, is_me)
        elif message.code == Message.WEATHER:
            wthrrcv(message.channel_id)
