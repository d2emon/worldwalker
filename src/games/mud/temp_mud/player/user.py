import re
from itertools import chain
from .. import debug
from ..database import ItemsData, PlayerData, LocationData
from ..errors import CrapupError, LooseError, ServiceError, CommandError
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


class Location:
    def __init__(self, location_id):
        self.location_id = location_id

    @property
    def items(self):
        return ItemsData().filter(location=self)

    @property
    def items_carried(self):
        return ItemsData().filter(carried_in=self)

    @property
    def players(self):
        return PlayerData().filter(location=self)


class SummonData:
    def __init__(self):
        self.location_id = None  # tdes, ades
        self.__vdes = 0
        self.__rdes = 0

    @property
    def ready(self):
        return self.location_id is not None

    def event(self, user):
        self.__rdes = 0
        self.__vdes = 0

        if not self.ready:
            return
        if not user.on_summon():
            return

        user.location_id = self.location_id
        self.location_id = None
        yield ""


class DrunkData:
    def __init__(self):
        self.__counter = 0

    @property
    def ready(self):
        return self.__counter > 0

    def event(self, user):
        if not self.ready:
            return

        self.__counter -= 1
        yield from user.on_drunk


class Decoder:
    def __init__(self):
        self.pronouns = {}

    # Specials
    def __decoder(
        self,
        pattern,
        condition=lambda match: True,
        replace=lambda match: match.group(0),
        default=lambda match: ""
    ):
        return lambda m: re.sub(pattern, lambda match: replace(match) if condition(match) else default(match), m)

    def decode(self, player, message, from_keyboard=True):
        """
        The main loop

        :param message:
        :return:
        """
        for decoder in (
            self.__decoder(
                r"\001f(.{, 128})\001",
                condition=lambda match: player.debug,
                replace=lambda match: "[FILE {} ]\n{}".format(match.group(0), f_listfl(match.group(0))),
                default=lambda match: f_listfl(match.group(0)),
            ),
            self.__decoder(
                r"\001d(.{, 256})\001",
                condition=lambda match: not player.is_deaf,
            ),
            self.__decoder(
                r"\001s(.{, 23})\001(.{, 256})\001",
                condition=lambda match: player.find(match.group(0)).count,
                replace=lambda match: match.group(1),
            ),
            self.__decoder(
                r"\001p(.{, 24})\001",
                condition=lambda match: player.find(match.group(0)).count,
                default=lambda match: "Someone",
            ),
            self.__decoder(
                r"\001c(.{, 256})\001",
                condition=lambda match: player.in_light and not player.is_blind,
            ),
            self.__decoder(
                r"\001P(.{, 24})\001",
                condition=lambda match: player.can_hear_player(player.find(match.group(0)).count),
                default=lambda match: "Someone",
            ),
            self.__decoder(
                r"\001D(.{, 24})\001",
                condition=lambda match: not player.is_blind and player.find(Player.find(match.group(0)).first).count,
                default=lambda match: "Someone",
            ),
            self.__decoder(
                r"\001l(.{, 127})\001",
                condition=lambda match: not from_keyboard,
            ),
        ):
            message = decoder(message)
        return message

    # BprintF
    def set_player(self, player):
        if player.sex == User.SEX_FEMALE:
            self.pronouns['her'] = player.name
            self.pronouns['them'] = player.name
        elif player.sex == User.SEX_MALE:
            self.pronouns['him'] = player.name
            self.pronouns['them'] = player.name
        else:
            self.pronouns['it'] = player.name
            return


class User(WorldPlayer, UserData, Actor):
    class Blood:
        # TODO: Remove it

        in_fight = 0
        fighting = None

        @classmethod
        def check_fight(cls, location=None):
            enemy = cls.get_enemy()
            if enemy is None:
                return
            if not enemy.exists:
                return cls.stop_fight()
            if location is not None and not location.equal(enemy.location):
                return cls.stop_fight()

        @classmethod
        def stop_fight(cls):
            cls.in_fight = 0
            cls.fighting = None

        @classmethod
        def get_enemy(cls):
            if cls.fighting is None:
                return None
            if not cls.in_fight:
                return None
            return cls.fighting

        @classmethod
        def next_turn(cls, location=None):
            cls.check_fight(location)
            if not cls.in_fight:
                return
            cls.in_fight -= 1

        @classmethod
        def fight(cls, player):
            cls.in_fight = 0

            enemy = cls.get_enemy()
            if enemy is None:
                return

            enemy.hitplayer(player.wpnheld)

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
        self.__location_id = player_data[4]
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

        self.__summon_data = SummonData()
        self.__drunk_data = DrunkData()

        self.__is_zapped = False

        self.__invisibility_counter = 0
        self.__to_update = False

        # Weather
        self.__has_farted = False

        # Unknown
        self.__wpnheld = None

        # self.buffer = Buffer()

        self.decoder = Decoder()

    # From WorldPlayer

    # Player properties:

    # WorldPlayer, UserData, Sender, Actor
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        super(WorldPlayer).name = value

    # WorldPlayer, Actor
    @property
    def location_id(self):
        return self.__location_id

    @location_id.setter
    def location_id(self, value):
        World.load()
        super(WorldPlayer).location_id = value

    # WorldPlayer, Reader
    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, value):
        self.__message_id = value

    # WorldPlayer, Sender, Actor
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
        if not any(PlayerData().filter(name=self.name).all):
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
        # self.location_id = location_id

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

    # From Sender

    def broadcast(self, message):
        # Parse
        self.force_read = True
        super().broadcast(message)

    # From Actor

    # Not Implemented
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
            self.location.items.not_destroyed(self)
                .or_filter(self.location.items_carried)
                .filter(is_light=True).count > 0,
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

    # Items
    @property
    def items_available(self):
        # Support, Weather
        return self.location.items.not_destroyed(self).or_filter(self.items)

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
        undead = not self.items.filter(item_id=45).first
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
        yield from (item.on_look(self) for item in self.items.all)

        if self.helping is not None:
            yield from self.__check_help()

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
        dragon = Player.find("dragon").first
        if dragon is None:
            return False
        if self.location.equal(dragon.location):
            return False
        return True

    def show_item_description(self, item):
        if self.debug:
            return "{{{}}} {}".format(item.item_id, item.description)
        return item.description

    def on_flee(self):
        # New1
        for item in self.items.filter(not_worn_by=self).all:
            item.set_location(self, item.IN_LOCATION)

    # Check

    def next_turn(self):
        self.Blood.check_fight(self.location)

    # Feel

    def can_see_player(self, player):
        if not player or self.equal(player):
            return True
        if super().can_see_player(player):
            self.decoder.set_player(player)
            return True
        else:
            return False

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

    # Summon (Parse)
    @property
    def can_be_summoned(self):
        return not self.is_wizard

    def set_summoned_to(self, location):
        if self.can_be_summoned:
            self.__summon_data.location = location
        return self.can_be_summoned

    def on_summon(self):
        if not self.can_be_summoned:
            return False

        self.send_global("\001s{name}\001{name} vanishes in a puff of smoke\n\001".format(name=self.name))
        self.dump_items()
        self.send_global("\001s{name}\001{name} appears in a puff of smoke\n\001".format(name=self.name))
        return True

    # Support
    @property
    def myself(self):
        return PlayerData().filter(player=self)

    @property
    def players_visible(self):
        if not self.can_see:
            return self.myself
        return self.location.players.filter(visible=self.level).or_filter(self.myself)

    # ObjSys
    def find(self, name):
        return self.players_visible.filter(name=name)

    # Parse
    def hit_by_lightning(self, wizard):
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

    # On turn

    def __check_invisibility(self):
        # Parse
        if not self.__invisibility_counter:
            return
        self.__invisibility_counter -= 1
        if self.__invisibility_counter == 1:
            self.visible = 0
        yield ""

    def __check_update(self):
        if not self.__to_update:
            return

        yield from self.update()
        self.__to_update = False

    def __check_fight(self, interrupt):
        # Parse
        if not self.Blood.in_fight:
            return

        self.Blood.check_fight()

        if not interrupt:
            return

        self.Blood.fight(self)
        yield ""

    def __check_score(self):
        chance = random_percent() < 10
        if not chance and ItemsData().filter(item_id=18, worn_by=self).count <= 0:
            return

        self.strength += 1
        yield from self.update()

    def __check_forced(self):
        # New1
        if self.force_action is None:
            return

        self.is_forced = True
        # gamecom(self.force_action)
        yield self.force_action
        self.is_forced = False

    def __check_help(self):
        # Mobile
        helping = self.helping
        if not self.__in_setup:
            return
        if helping.exists and self.location.equal(helping.location):
            return

        yield "You can no longer help \001c{}\001\n".format(helping.name)
        self.helping = None

    def get_item(self, name, mode_0=False, error_message=None):
        items = ItemsData().filter(
            name=name,
            available=self,
            mode_0=mode_0
        )
        if not self.is_wizard:
            items = items.filter(destroyed=False)

        item = items.first
        if error_message and item is None:
            raise CommandError(error_message)

    def decode(self, message, from_keyboard=True):
        return self.decoder.decode(message, from_keyboard)

    # Orphan

    def drop_pepper(self):
        # Mobile
        self.send_global("You start sneezing ATISCCHHOOOOOO!!!!\n")

        dragon = PlayerData().filter(player_id=32, exists=True).first
        if dragon is None or not self.location.equal(dragon.location):
            return

        # Ok dragon and pepper time

        item89 = ItemsData().filter(item_id=89, worn_by=self).first
        if item89 is not None:
            # Fried dragon
            dragon.remove()  # No dragon
            self.score += 100
            return self.update()

        # Whoops !
        yield "The dragon sneezes forth a massive ball of flame.....\n"
        yield "Unfortunately you seem to have been fried\n"
        raise LooseError("Whoops.....   Frying tonight")

    # Events

    # From Reader

    # Events

    def on_message(self, message):
        # Parse
        yield from chain(
            self.before_message(message),
            super().on_message(message),
        )

    def on_messages(self, **kwargs):
        # Parse
        interrupt = kwargs.get('interrupt', False)

        self.save_position()

        yield from chain(
            self.__check_invisibility(),
            self.__check_update(),
            self.__summon_data.event(self),
            self.__check_fight(interrupt),
            self.__check_score(),
            self.__check_forced(),
            self.__drunk_data.event(self),
        )


    # In User

    def on_loose(self):
        # TODO: Refactor it
        # Signals.active = False
        # No interruptions while you are busy dying
        # ABOUT 2 MINUTES OR SO
        pass

    def on_drunk(self):
        # Parse
        if self.is_dumb:
            return
        yield from self.hiccup()

    def on_time(self):
        # Mobile
        if random_percent() > 80:
            self.on_look()
