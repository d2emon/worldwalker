import logging


class NewUaf:
    score = 0
    level = 0
    strength = 0
    sex = [False] * 8


def __start_game(user):
    user.start(NewUaf)
    return True


def gamecom(user, command):
    logging.debug("\t\t%s:\t\tgamecom(%s)", user.name, command)


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
