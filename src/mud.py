from gamelib.mudexe.user import User
from gamelib.mudexe.tk.talker import talker


def main():
    user = User(1, "username")
    talker(user)


if __name__ == "__main__":
    main()
