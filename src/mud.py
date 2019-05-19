import uuid
from gamelib.mudexe.user import User
from gamelib.mudexe.tk.talker import talker
from gamelib.mud1 import mud1


class Env:
    def __init__(self):
        self.user_id = uuid.uuid1()
        self.host = "DAVIDPOOTER"
        self.username = None
        self.password = None

    def getty(self):
        self.username = input("username:\t")
        self.password = input("password:\t")


def main():
    # user = User(1, "username")
    # talker(user)

    env = Env()

    print(">", "mud.1")
    mud1(env, 'mud.1')

    # print(">", "mud.1", "-nName")
    # mud1(env, 'mud.1', '-nName')

    # print(">", "mud.1", "-nName", 1)
    # mud1(env, 'mud.1', '-nName', 1)


if __name__ == "__main__":
    main()
