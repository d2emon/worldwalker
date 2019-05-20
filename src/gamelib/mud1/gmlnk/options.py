from ..errors import CrapupError
from..gmainstubs import cls


def wizard_only(option):
    def wrapper(user):
        if not user.is_wizard:
            raise PermissionError()
        option(user)
    return wrapper


def enter_game(user):
    cls()
    print("The Hallway")
    print("You stand in a long dark hallway, which echoes to the tread of your")
    print("booted feet. You stride on down the hall, choose your masque and enter the")
    print("worlds beyond the known......")
    print()
    try:
        execl(EXE, "   --{----- ABERMUD -----}--      Playing as ", user.username)
    except Exception:
        raise CrapupError("mud.exe: Not Found\n")


def __enter_password(username):
    print("*")
    pwd = gepass()
    print()

    if not pwd:
        return __enter_password(username)
    if "," in pwd:
        print("Illegal Character in password")
        return __enter_password(username)
    print()
    print("Verify Password")
    print("*")
    pv = gepass()
    print()

    if pv == pwd:
        print()
        print("NO!")
        return __enter_password(username)

    block = User(username, pwd)
    delu2(username)  # delete me and tack me on end!
    try:
        token = Pfl.connect_lock(permissions="a")
    except FileNotFoundError:
        return
    block = qcrypt(block)
    Pfl.add_line(token, block)
    Pfl.disconnect(token)
    print("Changed")


def change_password(user):
    """
    Change your password

    :param user:
    :return:
    """
    pv = ""
    fl = None

    block = logscan(user.username)
    pwd = block.password
    print()
    print("Old Password")
    data = gepass()
    if data != pwd:
        print()
        print("Incorrect Password")
        return

    print()
    print("New Password")
    return  __enter_password()


def exit_game(user):
    raise SystemExit()


@wizard_only
def enter_test_game(user):
    cls()
    print("Entering Test Version")


@wizard_only
def show_user(user):
    """

    :param user:
    :return:
    """
    a = 0
    block = ""

    cls()
    name = getunm()
    block = shu(name)
    print()
    input("Hit Return...\n")


@wizard_only
def edit_user(user):
    """

    :param user:
    :return:
    """
    cls()
    name = getunm()
    block = shu(name)
    if block is None:
        block = User(
            name,
            "default",
            "E"
        )
    nam2 = block.name
    pas2 = block.password
    print()
    print("Editing : {}".format(name))
    print()
    ed_fld("Name:", nam2)
    ed_fld("Password:", pas2)
    bk2 = User(nam2, pas2)
    delu2(name)
    try:
        token = Pfl.connect_lock(permissions="a")
        Pfl.add_line(token, qcrypt(bk2))
        Pfl.disconnect(token)
    except FileNotFoundError:
        return


@wizard_only
def delete_user(user):
    """

    :param user:
    :return:
    """
    name = getunm()
    block = logscan(name)
    if block is None:
        print("\nCannot delete non-existant user")
    else:
        delu2(name)


OPTIONS = {
    '0': exit_game,
    '1': enter_game,
    '2': change_password,
    '4': enter_test_game,
    'a': show_user,
    'b': edit_user,
    'c': delete_user,
}
