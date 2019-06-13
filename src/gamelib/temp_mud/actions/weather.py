from ..item import Item
from ..player.player import Player
from ..weather_data import WEATHER_SUN, WEATHER_RAIN, WEATHER_STORM, WEATHER_SNOW, WEATHER_BLIZZARD
from .action import Action


# Silly Section
class Laugh(Action):
    # 50
    commands = "laugh",

    @classmethod
    def action(cls, command, parser):
        return parser.user.laugh()


class Cry(Action):
    # 51
    commands = "cry",

    @classmethod
    def action(cls, command, parser):
        return parser.user.cry()


class Burp(Action):
    # 52
    commands = "burp",

    @classmethod
    def action(cls, command, parser):
        return parser.user.burp()


class Fart(Action):
    # 53
    commands = "fart",

    @classmethod
    def action(cls, command, parser):
        return parser.user.fart()


class Hiccup(Action):
    # 54
    commands = "hiccup",

    @classmethod
    def action(cls, command, parser):
        return parser.user.hiccup()


class Grin(Action):
    # 55
    commands = "grin",

    @classmethod
    def action(cls, command, parser):
        return parser.user.grin()


class Smile(Action):
    # 56
    commands = "smile",

    @classmethod
    def action(cls, command, parser):
        return parser.user.smile()


class Wink(Action):
    # 57
    commands = "wink",
    # At person later maybe ?

    @classmethod
    def action(cls, command, parser):
        return parser.user.wink()


class Snigger(Action):
    # 58
    commands = "snigger",

    @classmethod
    def action(cls, command, parser):
        return parser.user.snigger()


class Pose(Action):
    # 59
    commands = "pose",

    @classmethod
    def action(cls, command, parser):
        return parser.user.pose()


class SetValue(Action):
    # 60
    commands = "set",

    @classmethod
    def action(cls, command, parser):
        name = parser.require_next("set what\n")
        item = Item.fobna(name)
        if item is None:
            player = Player.fpbn(name)
            value = parser.require_next("To what value ?\n")
            return parser.user.set_player_strength(player, int(value))

        value = parser.require_next("Set to what value ?\n")
        if value == "bit":
            bit_id = int(parser.require_next("Which bit ?\n"))
            value = next(parser)
            return parser.user.set_item_bit(item, bit_id, value)
        elif value == "byte":
            byte_id = int(parser.require_next("Which byte ?\n"))
            value = next(parser)
            return parser.user.set_item_byte(item, byte_id, value)
        else:
            return parser.user.set_item_state(item, int(value))


class Pray(Action):
    # 61
    commands = "pray",

    @classmethod
    def action(cls, command, parser):
        return parser.user.pray()


class __WeatherAction(Action):
    weather_id = None

    @classmethod
    def action(cls, command, parser):
        parser.user.set_weather(cls.weather_id)


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


class Groan(Action):
    # 141
    commands = "goan",

    @classmethod
    def action(cls, command, parser):
        return parser.user.groan()


class Moan(Action):
    # 142
    commands = "moan",

    @classmethod
    def action(cls, command, parser):
        return parser.user.moan()


class Yawn(Action):
    # 144
    commands = "yawn",

    @classmethod
    def action(cls, command, parser):
        return parser.user.yawn()


class Purr(Action):
    # 165
    commands = "purr",

    @classmethod
    def action(cls, command, parser):
        return parser.user.purr()


class Sulk(Action):
    # 167
    commands = "sulk",

    @classmethod
    def action(cls, command, parser):
        return parser.user.sulk()


class SetPFlags(Action):
    # 181
    commands = "pflags",

    @classmethod
    def action(cls, parser, user):
        player = Player.fpbn(parser.require_next("Whose PFlags ?\n"))
        flag_id = parser.require_next("Flag number ?\n")
        parser.user.set_player_flags(player, flag_id, next(parser))


class Emote(Action):
    # 187
    commands = "emote",
    """
    (C) Jim Finnis
    """

    @classmethod
    def action(cls, command, parser):
        parser.user.emote(parser.full())
