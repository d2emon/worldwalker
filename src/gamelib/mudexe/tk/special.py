def __start_game(user):
    user.__mode = user.MODE_GAME
    user.__channel = 5
    initme()
    WorldService.connect()

    user.player.strength = NewUaf.strength
    user.player.level = NewUaf.level
    if NewUaf.level < 10000:
        user.player.visible = 0
    else:
        user.player.visible = 10000
    user.player.weapon = None
    user.player.sex_all = NewUaf.sex
    user.player.helping = None

    sendsys(
        user.__name,
        user.__name,
        -10113,
        user.__channel,
        "<s user=\"{user}\">[ {user}  has entered the game ]\n</s>".format(user=user.__name),
    )

    user.rte()
    if randperc() <= 50:
        user.__channel = -183
    user.trapch(user.__channel)

    sendsys(
        user.__name,
        user.__name,
        -10000,
        user.__channel,
        "<s user=\"{user}\">{user}  has entered the game\n</s>".format(user=user.__name),
    )
    return True


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
