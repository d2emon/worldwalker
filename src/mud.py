import logging
import uuid
# from gamelib.mudexe.user import User
# from gamelib.mudexe.tk.talker import talker
# from gamelib.mud1 import MudGame
from gamelib.temp_mud.game import Game


logging.basicConfig(level=logging.INFO)


class User:
    def __init__(self):
        self.host_id = uuid.uuid1()
        self.hostname = "DAVIDPOOTER"
        self.username = None
        self.password = None

    def getty(self):
        self.username = input("username:\t")
        self.password = input("password:\t")


def main():
    # user = User(1, "username")
    # talker(user)

    # user = User()

    # print(">", "mud.1")
    # MudGame(user).play()

    print(">", "mud.1", "-nName")
    # MudGame(user, "Phantom").play()
    game = Game(uuid.uuid1(), "Phantom", 0)
    game.play()


    # print(">", "mud.1", "-nName", 1)
    # mud1(env, 'mud.1', '-nName', 1)


if __name__ == "__main__":
    main()
