from .errors import CrapupError, ServiceError, CommandError, LooseError
from .item import Item, Door
from .message import Message
from .player import Player
from .syslog import syslog
from .world import World


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

    # Unknown
    # For actions
    def flee(self):
        if not self.Blood.in_fight:
            return

        if Item(32).iscarrby(self):
            raise CommandError("The sword won't let you!!!!\n")

        self.send_message(
            self,
            Message.GLOBAL,
            self.location_id,
            "\001c{}\001 drops everything in a frantic attempt to escape\n".format(self.name),
        )
        self.send_message(
            self,
            Message.FLEE,
            self.location_id,
            "",
        )

        self.NewUaf.score -= self.NewUaf.score / 33  # loose 3%
        yield from self.update()
        self.Blood.in_fight = None
        self.on_flee_event()
