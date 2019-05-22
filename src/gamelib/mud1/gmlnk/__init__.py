from ..screens import UserScreen, MainScreen, GameScreen, TestGameScreen


def wizard_only(option):
    def wrapper(**kwargs):
        if not kwargs.get('admin'):
            raise PermissionError()
        option(**kwargs)
    return wrapper


def enter_game(**kwargs):
    return GameScreen.show(**kwargs)


def change_password(**kwargs):
    """
    Change your password

    :param user:
    :param game:
    :return:
    """
    MainScreen.change_password(**kwargs)
    return MainScreen.show(**kwargs)


def exit_game(**kwargs):
    raise SystemExit()


@wizard_only
def enter_test_game(**kwargs):
    return TestGameScreen.show(**kwargs)


@wizard_only
def show_user(**kwargs):
    """

    :param user:
    :param game:
    :return:
    """
    UserScreen.show_user(**kwargs)
    return MainScreen.show(**kwargs)


@wizard_only
def edit_user(**kwargs):
    """

    :param user:
    :param game:
    :return:
    """
    UserScreen.edit_user(**kwargs)
    return MainScreen.show(**kwargs)


@wizard_only
def delete_user(**kwargs):
    """

    :param user:
    :param game:
    :return:
    """
    MainScreen.delete_user(**kwargs)
    return MainScreen.show(**kwargs)


OPTIONS = {
    '0': exit_game,
    '1': enter_game,
    '2': change_password,
    '4': enter_test_game,
    'a': show_user,
    'b': edit_user,
    'c': delete_user,
}
