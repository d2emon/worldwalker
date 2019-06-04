"""
The next part of the universe...
"""
from ..action import Action
from ..errors import CommandError, NotFoundError
from ..item import Item
from ..message import Message, MSG_WEATHER, MSG_GLOBAL
from ..player import Player
from ..weather_data import WEATHER_SUN, WEATHER_RAIN, WEATHER_STORM, WEATHER_SNOW, WEATHER_BLIZZARD, WEATHER_START

"""
Weather Routines
 
Current weather defined by state of object 47
 
states are
 
0   Sunny
1   Rain
2   Stormy
3   Snowing
"""


def adjust_weather(user, new_weather):
    weather = Item(0)
    old_weather = weather.state
    if new_weather != old_weather:
        weather.state = new_weather
        Message.send(
            user,
            user,
            MSG_WEATHER,
            None,
            new_weather,
        )


def autochange_weather(user):
    chance = randperc()
    if chance < 50:
        return adjust_weather(user, 1)
    elif chance > 90:
        return adjust_weather(user, 2)
    else:
        return adjust_weather(user, 0)


def receive_weather(user, weather_id):
    if not user.location.outdoors():
        return

    weather_id = user.location.validate_weather_id(weather_id)
    yield WEATHER_START.get(weather_id, "")


class __Weather(Action):
    weather_id = None
    wizard_only = "What ?\n"

    @classmethod
    def action(cls, parser, user):
        adjust_weather(user, cls.weather_id)


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
    message = ""
    result = ""

    @classmethod
    def silly(cls, user, message):
        Message.send(
            user,
            user,
            MSG_GLOBAL,
            user.channel_id,
            message.format(user=user),
        )

    @classmethod
    def validate(cls, user):
        super().validate(user)
        if cls.not_dumb:
            user.diseases.dumb.check()

    @classmethod
    def action(cls, parser, user):
        cls.silly(user, cls.message)
        yield cls.result


class Laugh(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d falls over laughing\n\001"
    result = "You start to laugh\n"


class Purr(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d starts purring\n\001"
    result = "MMMMEMEEEEEEEOOOOOOOWWWWWWW!!\n"


class Cry(Silly):
    not_dumb = True
    message = "\001s{user.name}\001{user.name} bursts into tears\n\001"
    result = "You burst into tears\n"


class Sulk(Silly):
    message = "\001s{user.name}\001{user.name} sulks\n\001"
    result = "You sulk....\n"


class Burp(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d burps loudly\n\001"
    result = "You burp rudely\n"


class Hiccup(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d hiccups\n\001"
    result = "You hiccup\n"


class Fart(Silly):
    message = "\001P{user.name}\001\001d lets off a real rip roarer\n\001"
    result = "Fine...\n"

    @classmethod
    def action(cls, parser, user):
        user.has_farted = True
        super().action(parser, user)


class Grin(Silly):
    message = "\001s{user.name}\001{user.name} grins evilly\n\001"
    result = "You grin evilly\n"


class Smile(Silly):
    message = "\001s{user.name}\001{user.name} smiles happily\n\001"
    result = "You smile happily\n"


class Wink(Silly):
    # At person later maybe ?
    message = "\001s{user.name}\001{user.name} winks suggestively\n\001"
    result = "You wink\n"


class Snigger(Silly):
    not_dumb = True
    message = "\001P{user.name}\001\001d sniggers\n\001"
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
            cls.silly(user, "\001s{user.name}\001{user.name} throws out one arm and sends a huge bolt of fire high\n"
                            "into the sky\n\001")
            user.broad("\001cA massive ball of fire explodes high up in the sky\n\001")
        elif pose_id == 2:
            cls.silly(user, "\001s{user.name}\001{user.name} turns casually into a hamster before resuming normal "
                            "shape\n\001")
        elif pose_id == 3:
            cls.silly(user, "\001s{user.name}\001{user.name} starts sizzling with magical energy\n\001")
        elif pose_id == 4:
            cls.silly(user, "\001s{user.name}\001{user.name} begins to crackle with magical fire\n\001")


class Emote(Silly):
    """
    (C) Jim Finnis
    """
    god_only = "Your emotions are strictly limited!\n"

    @classmethod
    def action(cls, parser, user):
        cls.silly(user, "\001P{}\001 " + parser.getreinput() + "\n")


class Pray(Silly):
    message = "\001s{user.name}\001{user.name} falls down and grovels in the dirt\n\001"
    result = "Ok\n"


class Yawn(Silly):
    message = "\001P{user.name}\001\001d yawns\n\001"


class Groan(Silly):
    message = "\001P{user.name}\001\001d groans loudly\n\001"
    result = "You groan\n"


class Moan(Silly):
    message = "\001P{user.name}\001\001d starts making moaning noises\n\001"
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
            yield "Current Value is : {}\n".format(item.byte(byte_id))
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
