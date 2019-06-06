from ..errors import CommandError, CrapupError
from .action import Action, ActionList


class Direction(Action):
    direction_id = None

    @classmethod
    def action(cls, command, parser):
        if cls.direction_id is None:
            raise CommandError("Thats not a valid direction\n")
        parser.user.go_in_direction(cls.direction_id)


class ExitsList(ActionList):
    default_action = Direction

    def __init__(self):
        super().__init__(
            GoNorth,
            GoEast,
            GoSouth,
            GoWest,
            GoUp,
            GoDown,
        )


class Go(Action):
    # 1
    exits = ExitsList()

    @classmethod
    def action(cls, command, parser):
        direction = parser.require_next("GO where ?\n")
        if direction == "rope":
            direction = "up"
        return cls.exits.check(direction).execute(command, parser)


class GoNorth(Direction):
    # 2
    direction_id = 0
    commands = "n", "north",


class GoEast(Direction):
    # 3
    direction_id = 1
    commands = "e", "east",


class GoSouth(Direction):
    # 4
    direction_id = 2
    commands = "s", "south",


class GoWest(Direction):
    # 5
    direction_id = 3
    commands = "w", "west",


class GoUp(Direction):
    # 6
    direction_id = 4
    commands = "u", "up",


class GoDown(Direction):
    # 7
    direction_id = 5
    commands = "d", "down",


class QuitWorld(Action):
    # 8
    commands = "quit",

    @classmethod
    def action(cls, command, parser):
        yield from parser.user.quit_game()

        parser.mode = parser.MODE_SPECIAL
        saveme()
        raise CrapupError("Goodbye")


class Groan(Action):
    # 139
    commands = "groan",

    @classmethod
    def validate(cls, command, parser):
        if parser.user.Blood.in_fight:
            raise CommandError("Not in a fight!\n")
        return True

    @classmethod
    def action(cls, command, parser):
        return gropecom()


class Credits(Action):
    # 169
    commands = "credits",

    @classmethod
    def action(cls, command, parser):
        yield "\001f{}\001".format(CREDITS)


class Brief(Action):
    # 170
    commands = "brief",

    @classmethod
    def action(cls, command, parser):
        parser.switch_brief()


class MapWorld(Action):
    # 173
    commands = "map",

    @classmethod
    def action(cls, command, parser):
        yield "Your adventurers automatic monster detecting radar, and long range\n"
        yield "mapping kit, is, sadly, out of order.\n"


class Flee(Action):
    # 174
    commands = "flee",

    @classmethod
    def action(cls, command, parser):
        parser.user.flee()
        return Go.execute(command, parser)


class DebugMode(Action):
    # 180
    commands = "debugmode",

    @classmethod
    def action(cls, command, parser):
        parser.switch_debug()

