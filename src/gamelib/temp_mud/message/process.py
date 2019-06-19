from ..errors import LooseError
from ..player.player import Player
from ..world import World
from . import message_codes
from .weather import set_weather


# Parse
def check_name(name1, name2):
    name1 = name1.lower()
    name2 = name2.lower()
    if name1 == name2:
        return True
    if name1[:4] == "the " and name1[4:] == name2:
        return True
    return False


def __is_sender(user, message):
    return check_name(message.user_from, user.name)


def __is_receiver(user, message):
    return check_name(message.user_to, user.name)


def __private(f):
    def wrapped(user, message):
        if not __is_receiver(user, message):
            return
        return f(user, message)
    return wrapped


def __public(f):
    def wrapped(user, message):
        if __is_sender(user, message):
            return
        return f(user, message)
    return wrapped


def __to_other(f):
    def wrapped(user, message):
        if __is_receiver(user, message):
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
    user.snoopd = Player.find(message.user_from)


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
    if Player.find(message.user_from) is not None:
        user.loose()
    World.save()
    print("***HALT\n")
    raise SystemExit(0)


# VISIBLE
def __set_visible(user, message):
    Player(message.message[0]).visible = message.message[1]


# GLOBAL
@__to_other
@__local
def __global_message(user, message):
    yield message.message


# LIGHTNING
def __lightning(user, message):
    if __is_me(user, message):
        return user.hit_lightning(message.user_from)

    if message.channel_id == user.location_id:
        yield "\001cA massive lightning bolt strikes \001\001D{}\001\001c\n\001".format(message.user_to)


# SHOUT
@__public
def __shout(user, message):
    if user.__location_id == message.channel_id or user.is_wizard:
        yield "\001P{}\001\001d shouts '{}'\n\001".format(message.user_from, message.message)
    else:
        yield "\001dA voice shouts '{}'\n\001".format(message.message)


# SAY
@__public
@__local
def __say(user, message):
    yield "\001P{}\001\001d says '{}'\n\001".format(message.user_from, message.message)


# TELL
@__public
def __tell(user, message):
    yield "\001P{}\001\001d tells you '{}'\n\001".format(message.user_from, message.message)


# EXORCISE
def __exorcise(user, message):
    if __is_me(user, message):
        raise LooseError("You have been kicked off")
    yield "{} has been kicked off\n".format(message.user_to)


# PERSONAL
@__private
def __personal(user, message):
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


# NewUaf


# -10100
@__private
def cure(user, message):
    yield "All your ailments have been cured\n"
    user.is_dumb = False
    user.is_crippled = False
    user.is_blind = False
    user.is_deaf = False


# -10101
@__private
def cripple(user, message):
    if user.is_wizard:
        yield "\001p{}\001 tried to cripple you\n".format(message.user_from)
        return
    yield "You have been magically crippled\n"
    user.is_crippled = True


# -10102
@__private
def dumb(user, message):
    if user.is_wizard:
        yield "\001p{}\001 tried to dumb you\n".format(message.user_from)
        return
    yield "You have been struck magically dumb\n"
    user.is_dumb = True


# -10103
@__private
def force(user, message):
    if user.is_wizard:
        yield "\001p{}\001 tried to force you to {}\n".format(message.user_from, message.message)
        return
    yield "\001p{}\001 has forced you to {}\n".format(message.user_from, message.message)
    user.add_force(message.message)\


# -10104
@__to_other
def __code_10104(user, message):
    yield "\001p{}\001 shouts '{}'\n".format(message.user_from, message.message)


# -10105
@__private
def blind(user, message):
    if user.is_wizard:
        yield "\001p{}\001 tried to blind you\n".format(message.user_from)
        return
    yield "You have been struck magically blind\n"
    user.is_blind = True


# -10106
@__public
@__local
def bolt(user, message):
    yield "Bolts of fire leap from the fingers of \001p{}\001\n".format(message.user_from)
    if message.is_my(user.name.lower()):
        yield "You are struck!\n"
        wounded(message.message)
    else:
        yield "\001p{}\001 is struck\n".format(message.user_to)


# -10107
@__private
def change_sex(user, message):
    yield "Your sex has been magically changed!\n"
    user.sex = 1 - user.sex
    yield "You are now "
    yield "Male" if user.sex == 0 else "Female"
    yield "\n"
    yield from user.update()


# -10109
@__public
@__local
def fireball(user, message):
    yield "\001p{}\001 casts a fireball\n".format(message.user_from)
    if message.is_my(user.name.lower()):
        yield "You are struck!\n"
        wounded(message.message)
    else:
        yield "\001p{}\001 is struck\n".format(message.user_to)


# -10110
@__public
@__private
def shock(user, message):
    yield "\001p{}\001 touches you giving you a sudden electric shock!\n".format(message.user_from)
    wounded(message.message)


# -10111
@__private
def social(user, message):
    yield message.message + "\n"


# -10113
def wizard(user, message):
    if user.is_wizard:
        yield message.message


# -10120
@__private
def deaf(user, message):
    if user.is_wizard:
        yield "\001p{}\001 tried to deafen you\n".format(message.user_from)
        return
    yield "You have been magically deafened\n"
    user.is_deaf = True


# -20000
def flee(user, message):
    if Player.find(message.user_to.name) != user.Blood.fighting:
        return
    user.Blood.stop_fight()


MESSAGE_HANDLERS = {
    message_codes.STOP_SNOOP: __stop_snoop,  #
    message_codes.START_SNOOP: __start_snoop,  #
    message_codes.CHANGE_STATS: __change_stats,  #
    message_codes.TOO_EVIL: __too_evil,  #
    message_codes.MSG_750: __code_750,  #
    message_codes.VISIBLE: __set_visible,  #
    message_codes.GLOBAL: __global_message,
    message_codes.LIGHTNING: __lightning,
    message_codes.SHOUT: __shout,
    message_codes.SAY: __say,
    message_codes.TELL: __tell,
    message_codes.EXORCISE: __exorcise,
    message_codes.PERSONAL: __personal,
    message_codes.MSG_10020: __code_10020,  #
    message_codes.MSG_10021: __code_10021,  #
    message_codes.WEATHER: set_weather,

    # < -10099 NewUaf
    message_codes.CURE: cure,
    message_codes.CRIPPLE: cripple,
    message_codes.DUMB: dumb,
    message_codes.FORCE: force,
    message_codes.MSG_10104: __code_10104,  # Wizard shouts
    message_codes.BLIND: blind,  #
    message_codes.BOLT: bolt,
    message_codes.CHANGE_SEX: change_sex,
    message_codes.FIREBALL: fireball,
    message_codes.SHOCK: shock,
    message_codes.SOCIAL: social,
    message_codes.WIZARD: wizard,
    message_codes.DEAF: deaf,  #
    message_codes.FLEE: flee,
}


# Parse
def handle(user, message):
    if message.code >= -3:
        return __show_message(user, message)

    handler = MESSAGE_HANDLERS.get(message.code)
    if handler is None:
        return
    return handler(user, message)
