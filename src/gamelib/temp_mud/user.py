from .errors import CommandError
from .item import Item
from .message import Message
from .player import Player


class User:
    wd_there = ""

    class NewUaf:
        level = 0
        score = 0
        sex = 0
        strength = 0

        # Parse
        @classmethod
        def level_of(cls, score):
            score = score / 2  # Scaling factor
            if cls.level > 10:
                return cls.level
            elif score < 500:
                return 1
            elif score < 1000:
                return 2
            elif score < 3000:
                return 3
            elif score < 6000:
                return 4
            elif score < 10000:
                return 5
            elif score < 20000:
                return 6
            elif score < 32000:
                return 7
            elif score < 44000:
                return 8
            elif score < 70000:
                return 9
            else:
                return 10

    class Blood:
        fighting = None
        in_fight = 0

        @classmethod
        def stop_fight(cls):
            cls.in_fight = 0
            cls.fighting = None

        @classmethod
        def get_enemy(cls):
            return Player(cls.fighting)

        # Parse
        @classmethod
        def check_fight(cls):
            if cls.fighting is not None and cls.get_enemy().exists:
                cls.stop_fight()

            if cls.in_fight:
                cls.in_fight -= 1
