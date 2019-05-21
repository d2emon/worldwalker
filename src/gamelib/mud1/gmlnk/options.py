from services.errors import CrapupError
from..gmainstubs import cls


def wizard_only(option):
    def wrapper(user, *args):
        if not user.is_wizard:
            raise PermissionError()
        option(user, *args)
    return wrapper


def __get_user_data(game, show=False, default=False):
    if show:
        cls()
    username = __input_username()
    user_data = game.service.get_user(username, default)
    if show:
        __show_user_data(user_data)
    return user_data


def __input_field(label, value):
    """

    :param label:
    :param value:
    :return:
    """
    try:
        new_value = input("{}(Currently {} ):".format(label, value))[:128]
        if not new_value:
            return new_value
        if new_value[0] == ".":
            return new_value
        if "." in new_value:
            raise ValueError("\nInvalid Data Field\n")
    except ValueError as e:
        print(e)
        return __input_field(label, value)


def __input_password(username, old_password, game):
    try:
        new_password = input("*")
        print()

        game.service.validate_password(new_password)

        print()
        print("Verify Password")
        verify = input("*")
        print()

        if verify != new_password:
            raise ValueError("\nNo!")

        game.service.put_password(username, old_password, new_password)
        print("Changed")
    except ValueError as e:
        print(e)
        return __input_password(username, old_password, game)


def __input_username():
    return input("\nUser Name:")[:79]


def __show_user_data(user):
    """
    for show user and edit user

    :return:
    """
    if user is None:
        print()
        print("No user registered in that name")
        print()
        print()
        return None

    print()
    print()
    print("User Data For {}".format(user.username))
    print()
    print("Name:{}".format(user.username))
    print("Password:{}".format(user.password))


def enter_game(user, game):
    cls()
    print("The Hallway")
    print("You stand in a long dark hallway, which echoes to the tread of your")
    print("booted feet. You stride on down the hall, choose your masque and enter the")
    print("worlds beyond the known......")
    print()
    game.service.run_game("   --{----- ABERMUD -----}--      Playing as ", user.username)


def change_password(user, game):
    """
    Change your password

    :param user:
    :param game:
    :return:
    """
    try:
        print()
        password = input("Old Password")
        game.service.auth(user.username, password)
    except PermissionError:
        print()
        print("Incorrect Password")
        return

    print()
    print("New Password")
    return __input_password(user.username, password, game)


def exit_game(user, game):
    raise SystemExit()


@wizard_only
def enter_test_game(user, game):
    cls()
    print("Entering Test Version")


@wizard_only
def show_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    __get_user_data(game, True)

    print()
    input("Hit Return...\n")


@wizard_only
def edit_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    user_data = __get_user_data(game, True, True)

    print()
    print("Editing : {}".format(user_data.username))
    print()
    __input_field("Name:", user_data.username)
    __input_field("Password:", user_data.password)

    try:
        game.service.update_user(user_data.username, user_data.password)
    except ValueError as e:
        print(e)


@wizard_only
def delete_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    user_data = __get_user_data(game)

    try:
        game.service.delete_user(user_data.username)
    except ValueError as e:
        print(e)


OPTIONS = {
    '0': exit_game,
    '1': enter_game,
    '2': change_password,
    '4': enter_test_game,
    'a': show_user,
    'b': edit_user,
    'c': delete_user,
}
