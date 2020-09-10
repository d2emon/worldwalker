import logging
import uuid
from .temp_mud.game import Game


class Mud:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

        # user = User(1, "username")
        # talker(user)

        # user = User()

        # print(">", "mud.1")
        # MudGame(user).play()

        print(">", "mud.1", "-nName")
        # MudGame(user, "Phantom").play()
        self.game = Game(uuid.uuid1(), "Phantom", 0)

    def run(self):
        self.game.play()

        # print(">", "mud.1", "-nName", 1)
        # mud1(env, 'mud.1', '-nName', 1)
