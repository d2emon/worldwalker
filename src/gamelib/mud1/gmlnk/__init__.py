from ..errors import CrapupError
from ..gmainstubs import cls
from .options import OPTIONS


def __select_option(user):
    answer = input()[:2].lower()
    option = OPTIONS.get(answer)
    if option is None:
        raise ValueError()
    option(user)


def quick_start(user):
    try:
        execl(EXE, "   --}----- ABERMUD -----{--    Playing as ", user.username)
    except Exception:
        raise CrapupError("mud.exe : Not found\n")


def talker(user):
    user.is_wizard = user.user_id in ["wisner"]

    cls()
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
        __select_option(user)
    except ValueError:
        print("Bad Option")
        talker(user)
