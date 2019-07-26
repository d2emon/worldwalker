import re
from .. import debug
from ..database import ItemsData, PlayerData
from ..errors import CrapupError, LooseError, ServiceError
# from ..item import Item, Door
# from ..location import Location
from ..magic import random_percent
from ..services.log import LogService
from ..services.players import PlayersService
from ..world import World
from .actor import Actor
from .world_player import WorldPlayer, Level
from .player import Player
from .user_data import UserData


GWIZ = None


class User(WorldPlayer, UserData, Actor):
    def __init__(
        self,
        name,

        # Events
        before_message=lambda message: None,
        on_new_user=lambda: {},
    ):
        try:
            player_data = PlayersService.get_new_player(name=name)
        except ServiceError as e:
            raise CrapupError(e)

        super().__init__(player_data[0])

        # Player properties
        self.__name = player_data[1]
        self.__location = player_data[4]
        self.__message_id = player_data[5]
        # 6 UNKNOWN
        self.__strength = player_data[7]  # Not reimplemented
        self.__visible = player_data[8]
        self.__sex = player_data[9]  # flags
        self.__level = player_data[10]
        self.__weapon = player_data[11]  # Not reimplemented
        # 12 UNKNOWN
        # 13 Not reimplemented

        # Events
        self.before_message = before_message
        self.on_new_user = on_new_user

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

        self.__summoned_location = None  # tdes, ades
        self.__vdes = 0
        self.__rdes = 0

        self.__is_zapped = False

        self.__invisibility_counter = 0
        self.__drunk_counter = 0
        self.__to_update = False

        # Weather
        self.__has_farted = False

        # Unknown
        self.__wpnheld = None

        # self.buffer = Buffer()

    # From WorldPlayer

    # Player properties:

    # WorldPlayer, UserData, Actor
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        super(WorldPlayer).name = value

    # WorldPlayer, Actor
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

    # WorldPlayer, Actor
    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value

    # WorldPlayer, UserData, Actor
    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    # Flags:

    # 0
    # WorldPlayer, UserData, Actor
    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, value):
        self.__sex = value

    # Other properties:

    # WorldPlayer, UserData, Actor
    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value

    # Methods:

    # WorldData, Actor
    def check_kicked(self):
        # Unknown
        self.reset_position()
        World.load()
        if not any(PlayerData().filter(name=self.name).items):
            raise LooseError("You have been kicked off")

    def get_damage(self, enemy, damage):
        # New1
        if self.is_wizard:
            return

        self.strength -= damage
        self.__to_update = True

        if not self.is_dead:
            return

        World.save()

        self.remove()
        self.__is_zapped = True
        self.loose()

        # Send messages
        LogService.post_system(message="{} slain magically".format(self.name))
        self.send_global("{} has just died\n".format(self.name))
        self.send_wizard("[ {} has just died ]\n".format(self.name))

        raise CrapupError("Oh dear you just died\n")

    def look(self):
        super(Actor).look()

    def start(self):
        # Parse
        self.reload()

        self.show_players = True
        self.visible = 0 if not self.is_god else 10000
        debug.show_user(self)

        if self.load() is None:
            self.create(**self.on_new_user())
        debug.show_user(self)

        self.send_wizard("\001s{user.name}\001[ {user.name}  has entered the game ]\n\001".format(user=self))

        # yield from self.read_messages(reset_after_read=True)
        # self.location = location

        self.send_global("\001s{user.name}\001{user.name}  has entered the game\n\001".format(user=self))
        yield ""

    def woundmn(self, *args):
        pass

    # From UserData

    # Methods

    # UserData, Actor
    def update(self):
        """
        Routine to correct me in user file

        :return:
        """
        # Parse
        if not self.__in_setup:
            return

        level = Level.by_score(self)
        if level.level != self.level:
            self.level = level.level
            LogService.post_system(message="{} to level {}".format(self.name, level.level))
            yield "You are now {} {}\n".format(self.name, level.name)
            self.send_wizard("\001p{}\001 is now level {}\n".format(self.name, self.level))
            if self.level == 10:
                yield "\001f{}\001".format(GWIZ)

        self.strength = min(self.strength, 30 + 10 * self.level)

        self.__data.level = self.level
        self.__data.strength = self.strength
        self.__data.sex = self.sex
        self.__data.weapon = self.__wpnheld

    # ------------------------------------------------

    # From Actor

    # Not Implemented

    @property
    def available_items(self):
        # Weather
        return ItemsData().filter(available=self)

    @property
    def has_farted(self):
        return self.__has_farted

    @has_farted.setter
    def has_farted(self, value):
        self.__has_farted = value

    @property
    def in_light(self):
        # Weather
        return any((
            self.is_wizard,
            not self.location.is_dark,
            any(self.items_visible.filter(is_light=True).items),
        ))

    @property
    def items(self):
        return super(WorldPlayer).items

    @property
    def level_name(self):
        return super(WorldPlayer).level_name

    @property
    def show_players(self):
        return self.__show_players

    @show_players.setter
    def show_players(self, value):
        self.__show_players = value

    @property
    def overweight(self):
        return super(WorldPlayer).overweight

    @property
    def player_id(self):
        return super(WorldPlayer).player_id

    @property
    def items_available(self):
        # Support
        return self.items_here.or_filter(self.items_carried)

    def loose(self):
        # Tk
        self.on_loose()
        self.__in_setup = False

        World.load()
        self.dump_items()
        if self.visible < 10000:
            self.send_wizard("{} has departed from AberMUDII\n".format(self.name))
        self.delete()
        World.save()

        if not self.__is_zapped:
            self.save()
        self.send_snoop(self.snoop_target, False)

    def on_look(self):
        print("On Look")
        undead = not ItemsData().filter(item_id=45).first().is_carried_by(self)
        enemies = (
            undead and "wraith",
            "shazareth",
            "bomber",
            "owin",
            "glowin",

            "smythe",
            "dio",
            # ["The Dragon", -326, 500, 0, -2],
            undead and "zombie",
            # ["The Golem", -1056, 90, 0, -2],
            # ["The Haggis", -341, 50, 0, -2],
            # ["The Piper", -630, 50, 0, -2],
            "rat",
            "ghoul",
            # ["The Figure", -130, 90, 0, -2],

            "ogre",
            "riatha",
            "yeti",
            "guardian",
            # ["Prave", -201, 60, 0, -400],
            # undead and Player.find("wraith"),
            # ["Bath", -1, 70, 0, -401],
            # ["Ronnie", -809, 40, 0, -402],
            # ["The Mary", -1, 50, 0, -403],
            # ["The Cookie", -126, 70, 0, -404],

            # ["MSDOS", -1, 50, 0, -405],
            # ["The Devil", -1, 70, 0, -2],
            # ["The Copper", -1, 40, 0, -2],
        )

        enemies = (PlayerData().filter(name=enemy).first for enemy in enemies if enemy)
        yield from (enemy.on_look(self) for enemy in enemies if enemy)  # No such being

        items = ItemsData().filter(carried_by=self).items
        yield from (item.on_look(self) for item in items)

        if self.helping is not None:
            yield from self.check_help()

    def remove(self):
        return super(WorldPlayer).remove()

    def save_position(self):
        # Parse
        if abs(self.message_id - self.__position_saved) < 10:
            return

        self.reload()
        # self.__data = self
        self.__position_saved = self.message_id

    # Base Player properties

    @property
    def can_debug(self):
        return super(WorldPlayer).can_debug

    @property
    def can_edit(self):
        return super(WorldPlayer).can_edit

    @property
    def can_modify_messages(self):
        return super(WorldPlayer).can_modify_messages

    @property
    def can_set_flags(self):
        return super(WorldPlayer).can_set_flags

    @property
    def is_god(self):
        return super(WorldPlayer).is_god

    @property
    def is_wizard(self):
        return super(WorldPlayer).is_wizard

    @property
    def strength(self):
        return super(WorldPlayer).strength

    @strength.setter
    def strength(self, value):
        super(WorldPlayer).strength = value

    def die(self):
        return super(WorldPlayer).die()

    def dump_items(self):
        return super(WorldPlayer).dump_items()

    # Other
    def can_see_door(self, door):
        return self.in_light and door.visible

    @property
    def is_fighting(self):
        return self.Blood.in_fight > 0

    def add_force(self, action):
        if self.force_action is not None:
            yield "The compulsion to {} is overridden\n".format(action)
        self.force_action = action

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

    def show_item_description(self, item):
        if self.debug:
            return "{{{}}} {}".format(item.item_id, item.description)
        return item.description

    def on_flee(self):
        # New1
        for item in ItemsData().filter(carried_by=self, not_worn_by=self).items:
            item.set_location(self, item.IN_LOCATION)

    # Abstract

    # Modules

    @property
    def Blood(self):
        # TODO: Remove it
        return None

    # Not Implemented

    @property
    def brief(self):
        # TODO: Remove it
        return None

    @property
    def conversation_mode(self):
        # TODO: Remove it
        return None

    @property
    def debug_mode(self):
        # TODO: Remove it
        return None

    @property
    def force_action(self):
        # TODO: Remove it
        return None

    @force_action.setter
    def force_action(self, value):
        # TODO: Remove it
        print(value)

    @property
    def is_forced(self):
        # TODO: Remove it
        return None

    @is_forced.setter
    def is_forced(self, value):
        # TODO: Remove it
        print(value)

    @property
    def log_service(self):
        # TODO: Remove it
        return None

    @log_service.setter
    def log_service(self, value):
        # TODO: Remove it
        print(value)

    @property
    def in_ms(self):
        # TODO: Remove it
        return None

    @in_ms.setter
    def in_ms(self, value):
        # TODO: Remove it
        print(value)

    @property
    def out_ms(self):
        # TODO: Remove it
        return None

    @out_ms.setter
    def out_ms(self, value):
        # TODO: Remove it
        print(value)

    @property
    def min_ms(self):
        # TODO: Remove it
        return None

    @min_ms.setter
    def min_ms(self, value):
        # TODO: Remove it
        print(value)

    @property
    def mout_ms(self):
        # TODO: Remove it
        return None

    @mout_ms.setter
    def mout_ms(self, value):
        # TODO: Remove it
        print(value)

    def debug2(self, *args):
        # TODO: Remove it
        pass

    def show_buffer(self, *args):
        # TODO: Remove it
        pass

    # Disease
    @property
    def is_dumb(self):
        # TODO: Remove it
        return None

    @property
    def is_crippled(self):
        # TODO: Remove it
        return None

    @property
    def is_blind(self):
        # TODO: Remove it
        return None

    @property
    def is_deaf(self):
        # TODO: Remove it
        return None

    # Actions
    def wield(self):
        # TODO: Remove it
        pass

    def kill(self):
        # TODO: Remove it
        pass

    def translocate(self):
        # TODO: Remove it
        pass

    # ------------------------------------------------

    # In User
    # Parse
    @property
    def summoned_location(self):
        return self.__summoned_location if not self.is_wizard else None

    @summoned_location.setter
    def summoned_location(self, value):
        if self.is_wizard:
            self.__summoned_location = None
            return
        self.__summoned_location = value

    # ObjSys
    @property
    def items_here(self):
        return ItemsData().filter(user=self, location=self.location)

    @property
    def items_visible(self):
        return self.items_here.or_filter(ItemsData().filter(carried_in=self.location))

    @property
    def items_carried(self):
        return ItemsData().filter(carried_by=self)

    # Support
    @property
    def players_visible(self):
        return PlayerData().filter(visible=self.level, location=self.location).or_filter(self.myself)

    @property
    def myself(self):
        return PlayerData().filter(player=self)

    # ObjSys
    def find(self, name):
        player = self.players_visible.filter(name=name).first
        return player if self.can_see_player(player) or None

    # Support
    def check_fight(self):
        self.Blood.check_fight()
        if self.Blood.fighting and self.Blood.get_enemy().location.location_id != self.location.location_id:
            self.Blood.stop_fight()

        if self.Blood.in_fight:
            self.Blood.in_fight -= 1

    # Support
    def has_any(self, mask):
        return self.items_available.filter(mask=mask)

    # Parse
    def hit_lightning(self, wizard):
        if self.is_wizard:
            yield "\001p{}\001 cast a lightning bolt at you\n".format(wizard.name)
            return

        # You are in the ....
        yield "A massive lightning bolt arcs down out of the sky to strike you between\nthe eyes\n"

        self.__is_zapped = True
        self.delete()

        self.send_wizard(
            "[ \001p{}\001 has just been zapped by \001p{}\001 and terminated ]\n".format(
                self.name,
                wizard.name,
            ),
        )
        self.send_global("\001s{user}\001{user} has just died.\n\001".format(user=self.name))

        yield "You have been utterly destroyed by {}\n".format(wizard.name)
        raise LooseError("Bye Bye.... Slain By Lightning")

    # New1
    def __do_forced(self):
        if self.force_action is None:
            return

        self.is_forced = True
        gamecom(self.force_action)
        self.is_forced = False

    # Parse
    def on_message(self, message):
        yield from self.before_message(message)
        yield from super().on_message(message)

    def on_messages(self, **kwargs):
        interrupt = kwargs.get('interrupt', False)

        self.save_position()

        self.__update_invisibility()

        if self.__to_update:
            yield from self.update()
            self.__to_update = False

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

    # Parse
    def __summoned(self, location):
        self.__rdes = 0
        self.__vdes = 0
        if self.summoned_location is None:
            return

        self.send_global("\001s{name}\001{name} vanishes in a puff of smoke\n\001".format(name=self.name))
        self.dump_items()
        self.send_global("\001s{name}\001{name} appears in a puff of smoke\n\001".format(name=self.name))
        self.location = location
        self.summoned_location = None

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

    @property
    def can_see(self):
        return not self.is_blind and self.in_light

    def can_hear_player(self, player):
        return not self.is_deaf and player is not None

    def can_see_player(self, player):
        if not player or self.equal(player):
            return True
        if not self.can_see:
            return False
        if self.level < player.visible:
            return False
        if not self.location.equal(player.location):
            return False

        self.set_name(player)
        return True

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
            return message if self.find(name) else ""
        return f

    def __see_player(self):
        def f(match):
            name = match.group(0)
            return name if self.find(name) else "Someone"
        return f

    def __not_dark(self):
        def f(match):
            return match.group(0) if not self.in_light or self.is_blind else ""
        return f

    def __can_hear_player(self):
        def f(match):
            name = match.group(0)
            player = self.find(name)
            return name if self.can_hear_player(player) else "Someone"

        return f

    def __can_see_player(self):
        def f(match):
            name = match.group(0)
            player = Player.find(name)
            return name if not self.is_blind and self.find(player) else "Someone"

        return f

    @classmethod
    def __not_keyboard(cls, from_keyboard):
        def f(match):
            return match.group(0) if not from_keyboard else ""
        return f

    def on_loose(self):
        # Signals.active = False
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        pass
