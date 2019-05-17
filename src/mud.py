from gamelib.mudexe.user import User
from gamelib.mudexe.tk.talker import talker
from gamelib.mud1 import mud1


def main():
    # user = User(1, "username")
    # talker(user)

    print(">", "mud.1")
    mud1('mud.1')

    print(">", "mud.1", "-nName")
    mud1('mud.1', '-nName')

    print(">", "mud.1", "-nName", 1)
    mud1('mud.1', '-nName', 1)


if __name__ == "__main__":
    main()
