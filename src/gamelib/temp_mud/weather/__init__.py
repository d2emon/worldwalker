"""
The next part of the universe...
"""
from ..action import Action
from ..errors import CommandError, NotFoundError
from ..item import Item
from ..message import MSG_WEATHER
from ..player import Player
from ..weather_data import WEATHER_SUN, WEATHER_RAIN, WEATHER_STORM, WEATHER_SNOW, WEATHER_BLIZZARD, WEATHER_START, \
    WEATHER_TEXT

"""
Weather Routines
 
Current weather defined by state of object 47
 
states are
 
0   Sunny
1   Rain
2   Stormy
3   Snowing
"""


class Climate:
    @classmethod
    def get_weather_description(cls, weather_id):
        return WEATHER_TEXT.get(weather_id, ""),

    @classmethod
    def get_weather_id(cls, weather_id):
        return weather_id

    @classmethod
    def show_weather_start(cls, weather_id):
        yield WEATHER_START.get(cls.get_weather_id(weather_id))

    @classmethod
    def show_weather(cls, weather_id):
        yield from cls.get_weather_description(cls.get_weather_id(weather_id))


class ClimateWarm(Climate):
    @classmethod
    def get_weather_description(cls, weather_id):
        if weather_id == WEATHER_RAIN:
            return (
                "It is raining, a gentle mist of rain, which sticks to everything around\n",
                "you making it glisten and shine. High in the skies above you is a rainbow\n",
            )
        return super().get_weather_description(weather_id),

    @classmethod
    def get_weather_id(cls, weather_id):
        return weather_id % 2


class ClimateCold(Climate):
    @classmethod
    def get_weather_id(cls, weather_id):
        if weather_id in (1, 2):
            return weather_id + 2
        return weather_id


class Indoors(Climate):
    @classmethod
    def show_weather_start(cls, weather_id):
        return None

    @classmethod
    def show_weather(cls, weather_id):
        return None


class Weather:
    __weather = None

    @property
    def weather(self):
        if self.__weather is None:
            self.__weather = Item(0)
        return self.__weather

    def send_weather(self, user, new_weather):
        if self.weather.state == new_weather:
            return

        self.weather.state = new_weather
        user.send_message(user, MSG_WEATHER, None, new_weather)

    def autochange(self, user):
        chance = randperc()
        if chance < 50:
            return self.send_weather(user, 1)
        elif chance > 90:
            return self.send_weather(user, 2)
        else:
            return self.send_weather(user, 0)

    @classmethod
    def receive(cls, user, weather_id):
        if not user.location.outdoors():
            return

        yield from user.location.climate.show_weather_start(weather_id)


class __Weather(Action):
    weather_id = None
    wizard_only = "What ?\n"

    @classmethod
    def action(cls, parser, user):
        user.location.weather.send_weather(user, cls.weather_id)


class Sun(__Weather):
    weather_id = WEATHER_SUN


class Rain(__Weather):
    weather_id = WEATHER_RAIN


class Storm(__Weather):
    weather_id = WEATHER_STORM


class Snow(__Weather):
    weather_id = WEATHER_SNOW


class Blizzard(__Weather):
    weather_id = WEATHER_BLIZZARD


# Silly Section
class Silly(Action):
    not_dumb = False

    sound = None
    visual = None
    message = ""
    result = ""

    @classmethod
    def validate(cls, user):
        super().validate(user)
        if cls.not_dumb:
            user.diseases.dumb.check()

    @classmethod
    def action(cls, parser, user):
        message = cls.message
        if cls.sound is not None:
            message += "\001P{user.name}\001\001d " + cls.sound + "\n\001"
        if cls.visual is not None:
            message += "\001s{user.name}\001{user.name} " + cls.visual + "\n\001"
        user.silly(message)
        yield cls.result


class Laugh(Silly):
    not_dumb = True
    sound = "falls over laughing"
    result = "You start to laugh\n"


class Purr(Silly):
    not_dumb = True
    sound = "starts purring"
    result = "MMMMEMEEEEEEEOOOOOOOWWWWWWW!!\n"


class Cry(Silly):
    not_dumb = True
    visual = "bursts into tears"
    result = "You burst into tears\n"


class Sulk(Silly):
    visual = "sulks"
    result = "You sulk....\n"


class Burp(Silly):
    not_dumb = True
    sound = "burps loudly"
    result = "You burp rudely\n"


class Hiccup(Silly):
    not_dumb = True
    sound = "\001d hiccups"
    result = "You hiccup\n"


class Fart(Silly):
    sound = "lets off a real rip roarer"
    result = "Fine...\n"

    @classmethod
    def action(cls, parser, user):
        user.has_farted = True
        super().action(parser, user)


class Grin(Silly):
    visual = "grins evilly"
    result = "You grin evilly\n"


class Smile(Silly):
    visual = "smiles happily"
    result = "You smile happily\n"


class Wink(Silly):
    # At person later maybe ?
    visual = "winks suggestively"
    result = "You wink\n"


class Snigger(Silly):
    not_dumb = True
    sound = "sniggers"
    result = "You snigger\n"


class Pose(Silly):
    wizard_only = "You are just not up to this yet\n"

    @classmethod
    def action(cls, parser, user):
        pose_id = randperc() % 5

        yield "POSE :{}\n".format(pose_id)

        if pose_id == 0:
            pass
        elif pose_id == 1:
            user.silly("\001s{user.name}\001{user.name} throws out one arm and sends a huge bolt of fire high\n"
                       "into the sky\n\001")
            user.broadcast("\001cA massive ball of fire explodes high up in the sky\n\001")
        elif pose_id == 2:
            user.silly("\001s{user.name}\001{user.name} turns casually into a hamster before resuming normal "
                       "shape\n\001")
        elif pose_id == 3:
            user.silly("\001s{user.name}\001{user.name} starts sizzling with magical energy\n\001")
        elif pose_id == 4:
            user.silly("\001s{user.name}\001{user.name} begins to crackle with magical fire\n\001")


class Emote(Silly):
    """
    (C) Jim Finnis
    """
    god_only = "Your emotions are strictly limited!\n"

    @classmethod
    def action(cls, parser, user):
        user.silly("\001P{user.name}\001 " + parser.getreinput() + "\n")


class Pray(Silly):
    visual = "falls down and grovels in the dirt"
    result = "Ok\n"


class Yawn(Silly):
    sound = "yawns"


class Groan(Silly):
    sound = "groans loudly"
    result = "You groan\n"


class Moan(Silly):
    sound = "starts making moaning noises"
    result = "You start to moan\n"


class SetValue(Action):
    @classmethod
    def __set_bit(cls, parser, item):
        bit_id = int(parser.require_next("Which bit ?\n"))

        value = next(parser)
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

    @classmethod
    def __set_byte(cls, parser, item):
        byte_id = int(parser.require_next("Which byte ?\n"))

        value = next(parser)
        if value is None:
            yield "Current Value is : {}\n".format(item.get_byte(byte_id))
            return
        else:
            value = int(value)

        if value not in range(256) or byte_id not in range(2):
            raise CommandError("Number out of range\n")

        item.set_byte(byte_id, value)

    @classmethod
    def __set_mobile(cls, parser, mobile):
        try:
            player = Player.fpbn(mobile)
        except NotFoundError:
            raise CommandError("Set what ?\n")

        if not player.is_mobile:
            raise CommandError("Mobiles only\n")

        player.strength = int(parser.require_next("To what value ?\n"))

    @classmethod
    def __set_state(cls, item, state):
        if state < 0:
            raise CommandError("States start at 0\n")
        if state > item.max_state:
            raise CommandError("Sorry max state for that is {}\n".format(item.max_state))
        item.state = state

    @classmethod
    def action(cls, parser, user):
        item_name = parser.require_next("set what\n")
        if not user.is_wizard:
            raise CommandError("Sorry, wizards only\n")

        item = Item.fobna(item_name)
        if item is None:
            return cls.__set_mobile(parser, item_name)

        value = parser.require_next("Set to what value ?\n")
        if value == "bit":
            return cls.__set_bit(parser, item)
        elif value == "byte":
            return cls.__set_byte(parser, item)
        else:
            return cls.__set_state(item, int(value))


class SetPFlags(Action):
    @classmethod
    def validate(cls, user):
        if not user.player.test_bit(2):
            raise CommandError("You can't do that\n")

    @classmethod
    def action(cls, parser, user):
        try:
            player = Player.fpbn(parser.require_next("Whose PFlags ?\n"))
        except NotFoundError:
            raise CommandError("Who is that ?\n")

        flag_id = parser.require_next("Flag number ?\n")

        value = next(parser)
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
