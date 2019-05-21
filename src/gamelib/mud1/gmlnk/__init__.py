from ..screens import MainScreen, GameScreen
from .options import OPTIONS


def __select_option(*args):
    answer = MainScreen.input_option()
    option = OPTIONS.get(answer)
    if option is None:
        raise ValueError()
    option(*args)


def quick_start(user, game):
    GameScreen.show(show_intro=False)
    game.service.run_game("   --}----- ABERMUD -----{--    Playing as ", user.username)


def talker(user, game):
    try:
        MainScreen.show(admin=user.is_wizard)
        __select_option(user, game)
    except ValueError:
        MainScreen.show_message(message="Bad Option")
        talker(user, game)
