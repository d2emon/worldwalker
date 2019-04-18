from gamelib.mudexe.user import User
from gamelib.mudexe.tk.talker import talker


def main():
    user = User("username")
    talker(user)


if __name__ == "__main__":
    main()
