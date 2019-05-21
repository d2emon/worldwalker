from ..gmainstubs import clear
from ..screens import UserScreen, MainScreen, GameScreen, TestGameScreen


def wizard_only(option):
    def wrapper(user, *args):
        if not user.is_wizard:
            raise PermissionError()
        option(user, *args)
    return wrapper


def __get_user_data(game, screen, default=False):
    screen.before_data()
    user_data = game.service.get_user(
        screen.input_username(),
        default,
    )
    screen.show_data(user=user_data)
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
        UserScreen.show_message(e)
        return __input_field(label, value)


def __input_password(username, old_password, game):
    try:
        new_password = MainScreen.input_new_password()
        game.service.validate_password(new_password)
        verify = MainScreen.input_verify_password()
        if verify != new_password:
            raise ValueError("\nNo!")

        game.service.put_password(username, old_password, new_password)
        MainScreen.show_message(message="Changed")
    except ValueError as e:
        MainScreen.show_message(message=e)
        return __input_password(username, old_password, game)


def enter_game(user, game):
    GameScreen.show()
    game.service.run_game("   --{----- ABERMUD -----}--      Playing as ", user.username)


def change_password(user, game):
    """
    Change your password

    :param user:
    :param game:
    :return:
    """
    try:
        password = MainScreen.input_old_password()
        game.service.auth(user.username, password)
        MainScreen.request_new_password()
        return __input_password(user.username, password, game)
    except PermissionError:
        return MainScreen.show_message("\nIncorrect Password")


def exit_game(user, game):
    raise SystemExit()


@wizard_only
def enter_test_game(user, game):
    TestGameScreen.show()


@wizard_only
def show_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    __get_user_data(game, UserScreen)
    MainScreen.input_wait()


@wizard_only
def edit_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    try:
        user_data = __get_user_data(game, UserScreen, True)

        __input_field("Name:", user_data.username)
        __input_field("Password:", user_data.password)

        game.service.update_user(user_data.username, user_data.password)
    except ValueError as e:
        UserScreen.show_message(message=e)


@wizard_only
def delete_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    try:
        user_data = __get_user_data(game, MainScreen)

        game.service.delete_user(user_data.username)
    except ValueError as e:
        MainScreen.show_message(message=e)


OPTIONS = {
    '0': exit_game,
    '1': enter_game,
    '2': change_password,
    '4': enter_test_game,
    'a': show_user,
    'b': edit_user,
    'c': delete_user,
}
