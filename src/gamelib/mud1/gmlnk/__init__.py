from ..screens import MainScreen
from .options import OPTIONS


def __select_option(*args):
    answer = input()[:2].lower()
    option = OPTIONS.get(answer)
    if option is None:
        raise ValueError()
    option(*args)


def quick_start(user, game):
    MainScreen.show()
    game.service.run_game("   --}----- ABERMUD -----{--    Playing as ", user.username)


def talker(user, game):
    MainScreen.show()
    print("Welcome To AberMUD II [Unix]")
    print()
    print()
    print("Options")
    print()
    print("1]  Enter The Game")
    print("2]  Change Password")
    print()
    print()
    print("0] Exit AberMUD")
    print()
    print()
    if user.is_wizard:
        print("4] Run TEST game")
        print("A] Show persona")
        print("B] Edit persona")
        print("C] Delete persona")
    print()
    print()
    print("Select > ")

    try:
        __select_option(user, game)
    except ValueError:
        print("Bad Option")
        talker(user, game)
