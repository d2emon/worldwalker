import re
from ..errors import CrapupError, LooseError, ServiceError
# from ..item import Item, Door
# from ..location import Location
from ..magic import random_percent
from ..services.players import PlayersService
from ..world import World
from .actor import Actor
from .world_player import WorldPlayer
from .player import Player
from .user_data import UserData


GWIZ = None


class User(WorldPlayer, UserData, Actor):
    def __init__(self, name):
        try:
            player_data = PlayersService.get_new_player(name=name)
        except ServiceError as e:
            raise CrapupError(e)

        super().__init__(player_data[0])

        self.__name = player_data[1]
        self.__location = player_data[4]
        self.__message_id = player_data[5]
        # 6
        self.__strength = player_data[7]
        self.__visible = player_data[8]
        self.__sex = player_data[9]
        self.__level = player_data[10]
        self.__weapon = player_data[11]
        # 12
        # 13

        # Events
        self.before_message = lambda message: None
        self.get_new_user = lambda: {}

        # Other fields
        self.__in_setup = False
        self.__position_saved = 0

        # Parse
        self.__brief = False
        self.__show_players = False

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

        self.__invisibility_counter = 0
        self.__drunk_counter = 0
        self.__to_update = False

        # Weather
        self.__has_farted = False

        # Unknown
        self.__wpnheld = None

        # self.buffer = Buffer()

    # Player properties
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        super(WorldPlayer).name = value

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, value):
        World.load()
        super(WorldPlayer).location = value

    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, value):
        self.__message_id = value

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, value):
        self.__sex = value

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    # Other properties
    @property
    def is_mobile(self):
        return False

    # Weather
    @property
    def available_items(self):
        return find_items(available=self)

    @property
    def in_dark(self):
        def is_light(item):
            if not item.is_light:
                return False
            if self.item_is_here(item):
                return True
            return item.owner is not None and self.location.equal(item.owner.location)

        return not any((
            self.is_wizard,
            not self.location.is_dark,
            any(is_light(item) for item in find_items()),
        ))

    # From Reader
    def reset_position(self):
        self.message_id = -1

    # In User
    # Parse
    @property
    def summoned_location(self):
        return self.__summoned_location

    @summoned_location.setter
    def summoned_location(self, value):
        self.__summoned_location = value
        if not self.is_wizard:
            self.__is_summoned = True

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
        Signals.active = False
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
        self.send_snoop(self.snoop_target, False)

    # New1
    def __do_forced(self):
        if self.force_action is None:
            return

        self.is_forced = True
        gamecom(self.force_action)
        self.is_forced = False

    # Parse
    def on_messages(self, **kwargs):
        interrupt = kwargs.get('interrupt', False)

        self.save_position()

        self.__update_invisibility()

        if self.__to_update:
            yield from self.update()
            self.__to_update = False

        if self.__is_summoned:
            self.__summoned(self.summoned_location)

        self.__update_fight(interrupt)

        if Item(18).iswornby(self) or random_percent() < 10:
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

    def save_position(self):
        if abs(self.position - self.__position_saved) < 10:
            return

        World.load()
        # self.__data = self
        self.__position_saved = self.position

    def start(self):
        self.show_players = True

        # World.load()
        self.visible = 0 if not self.is_god else 10000

        if self.load() is None:
            self.create(**self.get_new_user())

        # self.send_wizard("\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self))

        # yield from self.read_messages(reset_after_read=True)
        # self.location = location

        # self.send_global("\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self))
        yield ""

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

    def __update_fight(self, interrupt):
        if not self.Blood.in_fight:
            return
        enemy = self.Blood.get_enemy()
        if enemy.location.location_id != self.location.location_id:
            self.Blood.stop_fight()
        if not enemy.exists:
            self.Blood.stop_fight()
        if not self.Blood.in_fight:
            return
        if not interrupt:
            return

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

    # New1
    def teleport(self, location):
        self.send_global("\001s{name}\001{name} has left.\n\001".format(name=self.name))
        self.send_global("\001s{name}\001{name} has arrived.\n\001".format(name=self.name))
        self.location = location

    # Mobile
    def on_time(self):
        if random_percent() > 80:
            self.on_look()

    def on_look(self):
        print("On Look")
        enemies = (
            # Player.find("wraith"),
            Player.find("shazareth"),
            Player.find("bomber"),
            Player.find("owin"),
            Player.find("glowin"),

            Player.find("smythe"),
            Player.find("dio"),
            # ["The Dragon", -326, 500, 0, -2],
            # Player.find("zombie"),
            # ["The Golem", -1056, 90, 0, -2],
            # ["The Haggis", -341, 50, 0, -2],
            # ["The Piper", -630, 50, 0, -2],
            Player.find("rat"),
            Player.find("ghoul"),
            # ["The Figure", -130, 90, 0, -2],

            Player.find("ogre"),
            Player.find("riatha"),
            Player.find("yeti"),
            Player.find("guardian"),
            # ["Prave", -201, 60, 0, -400],
            # Player.find("wraith"),
            # ["Bath", -1, 70, 0, -401],
            # ["Ronnie", -809, 40, 0, -402],
            # ["The Mary", -1, 50, 0, -403],
            # ["The Cookie", -126, 70, 0, -404],

            # ["MSDOS", -1, 50, 0, -405],
            # ["The Devil", -1, 70, 0, -2],
            # ["The Copper", -1, 40, 0, -2],
        )
        if not Item45().is_carried_by(self):
            enemies = enemies + (
                Player.find("zombie"),
                Player.find("wraith"),
            )
        enemies = (enemy for enemy in enemies if enemy is not None)  # No such being
        yield from map(lambda enemy: enemy.check_fight(self),  enemies)

        items = (item for item in ITEMS if item.is_carried_by(self))
        yield from map(lambda item: item.on_look(self),  items)

        if self.helping is not None:
            yield from self.check_help()

    def drop_pepper(self):
        self.send_global("You start sneezing ATISCCHHOOOOOO!!!!\n")
        if not Player32.exists or Player32.location.location_id != self.location.location_id:
            return

        # Ok dragon and pepper time
        if Item89.is_worn_by(self):
            # Fried dragon
            Player32.remove()  # No dragon
            self.score += 100
            return self.update()

        # Whoops !
        yield "The dragon sneezes forth a massive ball of flame.....\n"
        yield "Unfortunately you seem to have been fried\n"
        raise LooseError("Whoops.....   Frying tonight")

    def check_help(self):
        helping = self.helping
        if not self.__in_setup:
            return
        if helping.exists and helping.location.location_id == self.location.location_id:
            return

        yield "You can no longer help \001c{}\001\n".format(helping.name)
        self.helping = None

    def get_item(self, name, mode_0=False, error_message=None):
        item = find_item(
            name=name,
            available=self,
            mode_0=mode_0,
            destroyed=self.is_wizard,
        )
        if item is None and error_message:
            raise CommandError(error_message)

    # BprintF
    def set_name(self, player):
        if player.sex == self.SEX_FEMALE:
            self.pronouns['her'] = player.name
        elif player.sex == self.SEX_MALE:
            self.pronouns['him'] = player.name
        else:
            self.pronouns['it'] = player.name
            return
        self.pronouns['them'] = player.name

    def see_player(self, player):
        if player is None:
            return True
        if self.equal(player):
            # me
            return True
        if self.level < player.visible:
            return False
        if self.is_blind:
            # Cant see
            return False
        if self.location.equal(player.location) and self.in_dark:
            return False
        self.set_name(player)
        return True

    def can_hear_player(self, player):
        return not self.is_deaf and self.see_player(player)

    def can_see_player(self, player):
        return not self.is_blind and self.see_player(player)

    def decode(self, message, from_keyboard=True):
        """
        The main loop

        :param message:
        :return:
        """
        message = re.sub(r"\001f(.{, 128})\001", self.__list_file(), message)
        message = re.sub(r"\001d(.{, 256})\001", self.__not_deaf(), message)
        message = re.sub(r"\001s(.{, 23})\001(.{, 256})\001", self.__can_see(), message)
        message = re.sub(r"\001p(.{, 24})\001", self.__see_player(), message)
        message = re.sub(r"\001c(.{, 256})\001", self.__not_dark(), message)
        message = re.sub(r"\001P(.{, 24})\001", self.__can_hear_player(), message)
        message = re.sub(r"\001D(.{, 24})\001", self.__can_see_player(), message)
        message = re.sub(r"\001l(.{, 127})\001", self.__not_keyboard(from_keyboard), message)
        return message

    # Specials
    def __list_file(self):
        def f(match):
            filename = match.group(0)

            result = ""
            if self.debug:
                result += "[FILE {} ]\n".format(filename)
            result += f_listfl(filename)
            return result
        return f

    def __not_deaf(self):
        def f(match):
            return match.group(0) if not self.is_deaf else ""
        return f

    def __can_see(self):
        def f(match):
            name = match.group(0)
            message = match.group(1)
            player = Player.find(name)
            return message if self.see_player(player) else ""
        return f

    def __see_player(self):
        def f(match):
            name = match.group(0)
            player = Player.find(name)
            return name if self.see_player(player) else "Someone"
        return f

    def __not_dark(self):
        def f(match):
            return match.group(0) if self.in_dark or self.is_blind else ""
        return f

    def __can_hear_player(self):
        def f(match):
            name = match.group(0)
            player = Player.find(name)
            return name if self.can_hear_player(player) else "Someone"

        return f

    def __can_see_player(self):
        def f(match):
            name = match.group(0)
            player = Player.find(name)
            return name if self.can_see_player(player) else "Someone"

        return f

    @classmethod
    def __not_keyboard(cls, from_keyboard):
        def f(match):
            return match.group(0) if not from_keyboard else ""
        return f

    # Abstract
    @property
    def exists(self):
        return None

    @property
    def is_dead(self):
        return None

    @property
    def is_faded(self):
        return None

    @property
    def is_in_start(self):
        return None

    @property
    def is_god(self):
        return None

    @property
    def is_wizard(self):
        return None

    @property
    def max_items(self):
        return None

    @property
    def value(self):
        return None

    @property
    def level_name(self):
        return None

    def equal(self, player):
        pass

    def die(self):
        pass

    def dump_items(self):
        pass

    def fade(self):
        pass

    def get_lightning(self, enemy):
        pass

    def is_helping(self, player):
        pass

    def is_timed_out(self, current_position):
        pass

    def remove(self):
        pass

    def woundmn(self, *args):
        pass

    @property
    def brief(self):
        return None

    @property
    def conversation_mode(self):
        return None

    @property
    def debug_mode(self):
        return None

    @property
    def force_action(self):
        return None

    @property
    def is_forced(self):
        return None

    @property
    def has_farted(self):
        return self.__has_farted

    @property
    def log_service(self):
        return None

    @property
    def show_players(self):
        return self.__show_players

    @show_players.setter
    def show_players(self, value):
        self.__show_players = value

    @property
    def in_ms(self):
        return None

    @property
    def out_ms(self):
        return None

    @property
    def min_ms(self):
        return None

    @property
    def mout_ms(self):
        return None

    def debug2(self, *args):
        pass

    def show_buffer(self, *args):
        pass

    @property
    def is_dumb(self):
        return None

    @property
    def is_crippled(self):
        return None

    @property
    def is_blind(self):
        return None

    @property
    def is_deaf(self):
        return None

    def wield(self):
        pass

    def kill(self):
        pass

    def translocate(self):
        pass

