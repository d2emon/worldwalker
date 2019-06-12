from ..errors import CommandError, NotFoundError
from ..item import Item
from ..player import Player
from ..weather import Weather
from ..weather_data import WEATHER_SUN, WEATHER_RAIN, WEATHER_STORM, WEATHER_SNOW, WEATHER_BLIZZARD
from .action import Action


class __WeatherAction(Action):
    weather_id = None
    wizard_only = "What ?\n"

    @classmethod
    def action(cls, command, parser):
        Weather().weather_id = cls.weather_id


class Storm(__WeatherAction):
    # 62
    commands = "storm",
    weather_id = WEATHER_STORM


class Rain(__WeatherAction):
    # 63
    commands = "rain",
    weather_id = WEATHER_RAIN


class Sun(__WeatherAction):
    # 64
    commands = "sun",
    weather_id = WEATHER_SUN


class Snow(__WeatherAction):
    # 65
    commands = "snow",
    weather_id = WEATHER_SNOW


class Blizzard(__WeatherAction):
    # 104
    commands = "blizzard",
    weather_id = WEATHER_BLIZZARD


# Silly Section
class Silly(Action):
    not_dumb = False

    sound = None
    visual = None
    message = ""
    result = ""

    @classmethod
    def validate(cls, command, parser):
        super().validate(command, parser)
        if cls.not_dumb:
            parser.user.diseases.dumb.check()

    @classmethod
    def action(cls, command, parser):
        message = cls.message
        if cls.sound is not None:
            message += "\001P{user.name}\001\001d " + cls.sound + "\n\001"
        if cls.visual is not None:
            message += "\001s{user.name}\001{user.name} " + cls.visual + "\n\001"
        parser.user.silly(message)
        yield cls.result


class Laugh(Silly):
    # 50
    commands = "laugh",
    not_dumb = True
    sound = "falls over laughing"
    result = "You start to laugh\n"


class Cry(Silly):
    # 51
    commands = "cry",
    not_dumb = True
    visual = "bursts into tears"
    result = "You burst into tears\n"


class Burp(Silly):
    # 52
    commands = "burp",
    not_dumb = True
    sound = "burps loudly"
    result = "You burp rudely\n"


class Fart(Silly):
    # 53
    commands = "fart",
    sound = "lets off a real rip roarer"
    result = "Fine...\n"

    @classmethod
    def action(cls, command, parser):
        parser.user.has_farted = True
        super().action(command, parser)


class Hiccup(Silly):
    # 54
    commands = "hiccup",
    not_dumb = True
    sound = "\001d hiccups"
    result = "You hiccup\n"


class Grin(Silly):
    # 55
    commands = "grin",
    visual = "grins evilly"
    result = "You grin evilly\n"


class Smile(Silly):
    # 56
    commands = "smile",
    visual = "smiles happily"
    result = "You smile happily\n"


class Wink(Silly):
    # 57
    commands = "wink",
    # At person later maybe ?
    visual = "winks suggestively"
    result = "You wink\n"


class Snigger(Silly):
    # 58
    commands = "snigger",
    not_dumb = True
    sound = "sniggers"
    result = "You snigger\n"


class Pose(Silly):
    # 59
    commands = "pose",
    wizard_only = "You are just not up to this yet\n"

    @classmethod
    def action(cls, command, parser):
        pose_id = randperc() % 5

        yield "POSE :{}\n".format(pose_id)

        if pose_id == 0:
            pass
        elif pose_id == 1:
            parser.user.silly("\001s{user.name}\001{user.name} throws out one arm and sends a huge bolt of fire high\n"
                              "into the sky\n\001")
            parser.user.broadcast("\001cA massive ball of fire explodes high up in the sky\n\001")
        elif pose_id == 2:
            parser.user.silly("\001s{user.name}\001{user.name} turns casually into a hamster before resuming normal "
                              "shape\n\001")
        elif pose_id == 3:
            parser.user.silly("\001s{user.name}\001{user.name} starts sizzling with magical energy\n\001")
        elif pose_id == 4:
            parser.user.silly("\001s{user.name}\001{user.name} begins to crackle with magical fire\n\001")


class SetValue(Action):
    # 60
    commands = "set",
    wizard_only = "Sorry, wizards only\n"

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
    def action(cls, command, parser):
        item_name = parser.require_next("set what\n")
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


class Pray(Silly):
    # 61
    commands = "pray",
    visual = "falls down and grovels in the dirt"
    result = "Ok\n"


class Groan(Silly):
    # 141
    commands = "goan",
    sound = "groans loudly"
    result = "You groan\n"


class Moan(Silly):
    # 142
    commands = "moan",
    sound = "starts making moaning noises"
    result = "You start to moan\n"


class Yawn(Silly):
    # 144
    commands = "yawn",
    sound = "yawns"


class Purr(Silly):
    # 165
    commands = "purr",
    not_dumb = True
    sound = "starts purring"
    result = "MMMMEMEEEEEEEOOOOOOOWWWWWWW!!\n"


class Sulk(Silly):
    # 167
    commands = "sulk",
    visual = "sulks"
    result = "You sulk....\n"


class SetPFlags(Action):
    # 181
    commands = "pflags",
    @classmethod
    def validate(cls, command, parser):
        if not parser.user.test_bit(2):
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


class Emote(Silly):
    # 187
    commands = "emote",
    """
    (C) Jim Finnis
    """
    god_only = "Your emotions are strictly limited!\n"

    @classmethod
    def action(cls, command, parser):
        parser.user.silly("\001P{user.name}\001 " + parser.full() + "\n")
