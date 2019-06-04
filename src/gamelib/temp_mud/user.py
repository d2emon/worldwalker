from .errors import CrapupError
from .location import Location
from .message import Message, MSG_GLOBAL, MSG_WIZARD
from .player import Player
from .weather import autochange_weather


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

        self.__message_id = None
        self.__put_on()

        try:
            openworld()
        except FileNotFoundError:
            raise CrapupError("Sorry AberMUD is currently unavailable")
        self.__name = name
        self.read_messages()
        closeworld()

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
        items_count = sum(not item.is_destroyed and item.is_carried_by(self.player) for item in ITEMS)
        return items_count < max_items

    @property
    def is_dark(self):
        if self.is_wizard:
            return False
        if not self.location.is_dark:
            return False
        for item in filter(lambda i: i.is_light, ITEMS):
            if is_here(item):
                return False
            owner = item.owner
            if owner is not None and owner.location == self.__location_id:
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
            world = openworld()
        except FileNotFoundError:
            self.loose()
            raise CrapupError("\nAberMUD: FILE_ACCESS : Access failed\n")

        message_id = message.send2(world)

        if message_id >= 199:
            cleanup(message.get_message_data(world))

        if message_id >= 199:
            autochange_weather(self)

    def read_messages(self):
        try:
            world = openworld()
        except FileNotFoundError:
            raise CrapupError("AberMUD: FILE_ACCESS : Access failed\n")

        for message in Message.read_all(world, self.__message_id):
            self.output_message(message)
            self.__message_id = message.message_id

        self.update()
        eorte()
        rdes = 0
        tdes = 0
        vdes = 0

    def cleanup(self, message_data):
        world = openworld()
        for i in range(100):
            world[i] = world[100 + i + 1]
        message_data[0] += 100
        self.revise(message_data[0])

    def start_game(self):
        self.__location_id = -5
        self.initme()
        world = openworld()
        visible = 0 if not self.is_god else 10000
        self.player.start(self.NewUaf.strength, self.NewUaf.level, visible, self.NewUaf.sex)
        Message.send(
            self,
            self,
            MSG_WIZARD,
            self.__location_id,
            "\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self),
        )
        user.read_messages()
        if randperc() > 50:
            trapch(-5)
        else:
            self.__location_id = -183
            trapch(-183)
        Message.send(
            self,
            self,
            MSG_GLOBAL,
            self.__location_id,
            "\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self),
        )

    def go_to_channel(self, channel_id):
        openworld()
        self.player.location = channel_id
        self.look_in(self.location)

    def __put_on(self):
        self.__is_on = False
        world = openworld()
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
        world = openworld()
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
        closeworld()
        if not self.__zapped:
            saveme()
        chksnp()

    def update(self):
        if abs(self.__message_id - self.__updated) < 10:
            return

        openworld()
        self.player.position = self.__message_id
        self.__updated = self.__message_id

    def revise(self, timeout):
        openworld()
        for player in PLAYERS[:16]:
            if not player.is_alive:
                continue
            if player.position == -2:
                continue
            if player.position >= timeout / 2:
                continue
            self.broad("{} has been timed out\n".format(player.name))
            dumpstuff(player, player.location)
            player.remove()

    def look_in(self, location):
        closeworld()
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
                openworld()
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

        openworld()
        if not self.__ail_blind:
            lisobs()
            if self.mode == 1:
                lispeople()
        yield "\n"
        on_look()
