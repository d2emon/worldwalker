import logging
from services.world import WorldService


def initme(*args):
    logging.debug("initme(%s)", args)


def sendsys(*args):
    logging.debug("sendsys(%s)", args)


def randperc(*args):
    logging.debug("randperc(%s)", args)
    return 1


class NewUaf:
    score = 0
    level = 0
    strength = 0
    sex = [False] * 8


def __start_game(user):
    user.__mode = user.MODE_GAME
    user.__channel = 5
    initme()
    WorldService.connect()

    user.player.start(NewUaf)

    sendsys(
        user.name,
        user.name,
        -10113,
        user.channel,
        "<s user=\"{user}\">[ {user}  has entered the game ]\n</s>".format(user=user.name),
    )

    user.rte()
    if randperc() <= 50:
        user.channel = -183
    user.trapch(user.channel)

    sendsys(
        user.name,
        user.name,
        -10000,
        user.channel,
        "<s user=\"{user}\">{user}  has entered the game\n</s>".format(user=user.name),
    )
    return True


def gamecom(user, command):
    logging.debug("%s:\tgamecom(%s)", user.__name, command)


def special(user, command):
    if not command:
        return False

    command = command.lower()

    if command[0] != ".":
        return False

    command = command[1:]

    if command == "q":
        return True
    elif command == "g":
        return __start_game(user)
    else:
        print("\nUnknown . option\n")
        return True


def process_command(user, command):
    if user.mode == user.MODE_GAME:
        gamecom(user, command)
    else:
        special(user, command)
    return command.lower() == ".q"
