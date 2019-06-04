from .errors import CrapupError, ServiceError
from .item import Item
from .location import Location
from .message import Message, MSG_GLOBAL, MSG_WIZARD, MSG_BROADCAST
from .player import Player
from .weather import autochange_weather
from .world import World


class User:
    wd_there = ""

    class NewUaf:
        level = 0
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

        self.__message_id = None
        self.__put_on()
        try:
            World.load()
            self.__name = name
            self.read_messages()
            World.save()
        except ServiceError:
            raise CrapupError("Sorry AberMUD is currently unavailable")
        self.__message_id = None

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
        if not self.is_wizard:
            return None
        if self.player.level < 0:
            return None
        return self.player.level + 5

    @property
    def player(self):
        return Player(self.__player_id)

    def set_wd_there(self, zone, location_id):
        self.wd_there = zone + " " + location_id

    def output_message(self, message_data):
        """
        Print appropriate stuff from data block

        :param user:
        :param message_data:
        :return:
        """
        code = message_data[1]
        text = message_data[2]
        if self.debug_mode:
            bprintf("\n<{}>".format(code))
        if code < -3:
            gamrcv(message_data, self.__name.lower())
        else:
            bprintf(text)

    @property
    def enemy(self):
        return Player(self.Blood.fighting)

    def check_fight(self):
        if self.Blood.fighting is not None:
            if self.enemy.is_alive:
                self.Blood.stop_fight()
            if self.enemy.location != self.__location_id:
                self.Blood.stop_fight()

        if self.Blood.in_fight:
            self.Blood.in_fight -= 1

    def send2(self, message):
        try:
            World.load()

            message_id = message.save()
            if message_id >= 199:
                for message in World.cleanup():
                    self.broad(message)
                autochange_weather(self)
        except ServiceError:
            self.loose()
            raise CrapupError("\nAberMUD: FILE_ACCESS : Access failed\n")

    def broad(self, message):
        self.rd_qd = True
        self.send2(Message(
            None,
            None,
            MSG_BROADCAST,
            None,
            message,
        ))

    def read_messages(self, to_read=True):
        if not to_read:
            to_read = self.rd_qd
            self.rd_qd = False

        if not to_read:
            return

        try:
            World.load()
            for message in Message.messages(self.__message_id):
                self.output_message(message)
                self.__message_id = message.message_id

            self.update()
            eorte()
            rdes = 0
            tdes = 0
            vdes = 0
        except ServiceError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

    def start_game(self):
        self.__location_id = -5
        self.initme()
        World.load()
        visible = 0 if not self.is_god else 10000
        self.player.start(self.NewUaf.strength, self.NewUaf.level, visible, self.NewUaf.sex)
        Message.send(
            self,
            self,
            MSG_WIZARD,
            self.__location_id,
            "\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self),
        )
        self.read_messages()
        if randperc() > 50:
            self.__location_id = -5
        else:
            self.__location_id = -183
        self.go_to_channel(self.__location_id)
        Message.send(
            self,
            self,
            MSG_GLOBAL,
            self.__location_id,
            "\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self),
        )

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
            Message.send(
                self,
                self,
                MSG_WIZARD,
                0,
                "{} has departed from AberMUDII\n".format(self.name)
            )
        self.player.remove()
        World.save()

        if not self.__zapped:
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

    def is_available(self, item):
        if self.is_here(item):
            return True
        return item.is_carried_by(self.player)

    def has_any(self, mask):
        items = Item.items()
        items = (item for item in items if item.is_carried_by(self.__player_id) or self.is_here(self.__player_id))
        return any(item for item in items if item.test_mask(mask))
