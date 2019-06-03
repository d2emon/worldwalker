from .errors import CrapupError
from .location import Location
from .message import Message
from .player import Player
from .weather import autochange_weather


class User:
    wd_there = ""

    class NewUaf:
        my_lev = 0

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
        self.__player_id = 0

        self.__location_id = 0

        self.__message_id = None
        self.__putmeon()

        try:
            openworld()
        except FileNotFoundError:
            raise CrapupError("Sorry AberMUD is currently unavailable")
        if self.__player_id >= maxu:
            raise Exception("\nSorry AberMUD is full at the moment\n")
        self.__name = name
        self.read_messages()
        closeworld()

        self.__message_id = None

    @property
    def name(self):
        return self.__name

    @property
    def is_wizard(self):
        return self.NewUaf.my_lev > 9

    @property
    def is_god(self):
        return self.NewUaf.my_lev > 9999

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
            sysctrl(message_data, self.__name.lower())
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
            loseme()
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
        revise(message_data[0])
