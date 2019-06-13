from ..errors import LooseError
from ..player.player import Player
from ..world import World
from . import message_codes
from .weather import set_weather


# Parse
def __is_me(user, message):
    return message.is_my(user.name.lower())


def __private(f):
    def wrapped(user, message):
        if not __is_me(user, message):
            return
        return f(user, message)
    return wrapped


def __public(f):
    def wrapped(user, message):
        if __is_me(user, message):
            return
        return f(user, message)
    return wrapped


def __local(f):
    def wrapped(user, message):
        if message.channel_id != user.location_id:
            return
        return f(user, message)
    return wrapped


# > -3
def __show_message(user, message):
    yield message.message


# STOP_SNOOP
@__private
def __stop_snoop(user, message):
    user.snoopd = None


# START_SNOOP
@__private
def __start_snoop(user, message):
    user.snoopd = Player.fpbns(message.user_from)


# CHANGE_STATS
@__private
def __change_stats(user, message):
    user.level, user.score, user.strength = message.message
    yield from user.update()


# TOO_EVIL
def __too_evil(user, message):
    yield "Something Very Evil Has Just Happened...\n"
    raise LooseError("Bye Bye Cruel World....")


# -750
@__private
def __code_750(user, message):
    if Player.fpbns(message.user_from) is not None:
        user.loose()
    World.save()
    print("***HALT\n")
    raise SystemExit(0)


# VISIBLE
def __set_visible(user, message):
    Player(message.message[0]).visible = message.message[1]


# GLOBAL
@__public
@__local
def __global_message(user, message):
    yield message.message


# -10001
def __code_10001(user, message):
    if __is_me(user, message):
        return user.hit_lightning(message.user_from)

    if message.channel_id == user.location_id:
        yield "\001cA massive lightning bolt strikes \001\001D{}\001\001c\n\001".format(message.user_to)


# -10002
@__public
def __shout(user, message):
    if user.__location_id == message.channel_id or user.is_wizard:
        yield "\001P{}\001\001d shouts '{}'\n\001".format(message.user_from, message.message)
    else:
        yield "\001dA voice shouts '{}'\n\001".format(message.message)


# -10003
@__public
@__local
def __say(user, message):
    yield "\001P{}\001\001d says '{}'\n\001".format(message.user_from, message.message)


# -10004
@__public
def __tell(user, message):
    yield "\001P{}\001\001d tells you '{}'\n\001".format(message.user_from, message.message)


# -10010
def __code_10010(user, message):
    if __is_me:
        raise LooseError("You have been kicked off")
    yield "{} has been kicked off\n".format(message.user_to)


# -10011
def __code_10011(user, message):
    yield message.message


# -10020
@__private
def __code_10020(user, message):
    user.summoned_location = message.channel_id
    if user.is_wizard:
        yield "\001p{}\001 tried to summon you\n".format(message.user_from)
        return
    yield "You drop everything you have as you are summoned by \001p%s\001\n".format(message.user_from)

# -10021
@__local
@__private
def __code_10021(user, message):
    user.__rdes = 1
    user.__vdes = message.message[0]
    bloodrcv(message.message, __is_me(user, message))


MESSAGE_HANDLERS = {
    message_codes.STOP_SNOOP: __stop_snoop,
    message_codes.START_SNOOP: __start_snoop,
    message_codes.CHANGE_STATS: __change_stats,
    message_codes.TOO_EVIL: __too_evil,
    message_codes.MSG_750: __code_750,
    message_codes.VISIBLE: __set_visible,
    message_codes.GLOBAL: __global_message,
    message_codes.MSG_10001: __code_10001,
    message_codes.SHOUT: __shout,
    message_codes.SAY: __say,
    message_codes.TELL: __tell,
    message_codes.MSG_10010: __code_10010,
    message_codes.MSG_10011: __code_10011,
    message_codes.MSG_10020: __code_10020,
    message_codes.MSG_10021: __code_10021,
    message_codes.WEATHER: set_weather,

    # < -10099
    # message_codes.WIZARD: wizard,
    # message_codes.FLEE: flee,
}


# Parse
def handle(user, message):
    if message.code == message_codes.FLEE and Player.fpbn(message.user_to) == user.Blood.fighting:
        user.Blood.stop_fight()
        return

    if message.code >= -3:
        return __show_message(user, message)
    elif message.code < -10099:
        return new1rcv(
            message.is_my(user.name.lower()),
            message.channel_id,
            message.user_to,
            message.user_from,
            message.code,
            message.message,
        )

    handler = MESSAGE_HANDLERS.get(message.code)
    if handler is None:
        return
    return handler(user, message)
