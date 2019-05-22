from ..screens import UserScreen, MainScreen, GameScreen, TestGameScreen


def wizard_only(option):
    def wrapper(user, *args):
        if not user.is_wizard:
            raise PermissionError()
        option(user, *args)
    return wrapper


def __get_person(game, screen, default=False):
    user_data = game.service.get_user(
        screen.input_username(),
        default,
    )
    screen.show_data(user=user_data)
    return user_data


def __input_password(username, old_password, game):
    try:
        new_password = MainScreen.input_new_password()
        game.service.get_validate_password(new_password)
        verify = MainScreen.input_verify_password()
        if verify != new_password:
            raise ValueError("\nNo!")

        game.service.post_password(username, old_password, new_password)
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
        game.service.get_auth(user.username, password)
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
    person = game.service.get_user(UserScreen.input_username())
    UserScreen.show_data(user=person)
    MainScreen.input_wait()


@wizard_only
def edit_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    username = UserScreen.input_username()
    person = game.service.get_user(username)
    if person is None:
        person = {
            'user_id': user.user_id,
            'username': username,
            'password': 'default'
        }
    UserScreen.show_data(user=person)
    try:
        game.service.put_user(
            UserScreen.input_field(label="Name:", value=person.username),
            UserScreen.input_field(label="Password:", value=person.password),
        )
    except ValueError as e:
        UserScreen.show_message(message=e)


@wizard_only
def delete_user(user, game):
    """

    :param user:
    :param game:
    :return:
    """
    person = game.service.get_user(MainScreen.input_username())
    MainScreen.show_data(user=person)
    try:
        game.service.delete_user(person.username)
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
