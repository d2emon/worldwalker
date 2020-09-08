from ..direction import DIRECTIONS
from ..errors import CommandError
from .action import Action, ActionList


class Direction(Action):
    direction_id = None

    @classmethod
    def validate(cls, command, parser):
        if cls.direction_id is None:
            raise CommandError("That's not a valid direction\n")

    @classmethod
    def action(cls, command, parser):
        return parser.user.go(DIRECTIONS.get(cls.direction_id))

    @classmethod
    def flee(cls, parser):
        return parser.user.flee(cls.direction_id)


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
    def get_direction(cls, parser):
        direction = parser.require_next("GO where ?\n")
        if direction == "rope":
            return "up"
        return cls.exits.check(direction)

    @classmethod
    def action(cls, command, parser):
        return cls.get_direction(parser).execute(command, parser)


class QuitWorld(Action):
    # 8
    commands = "quit",

    @classmethod
    def action(cls, command, parser):
        return parser.user.quit_game()


class Look(Action):
    # 11
    commands = "look",

    @classmethod
    def action(cls, command, parser):
        word = next(parser)
        if word is None:
            parser.user.show_players = True
            return parser.user.look(full=True)
        elif word == "at":
            return examcom()
        elif word != "in" and word != "into":
            item = parser.user.get_item(parser.require_next("In what ?\n"))
            return parser.user.look_in(item)


class Reset(Action):
    # 14
    full_match = True
    commands = "reset",

    @classmethod
    def action(cls, command, parser):
        return parser.user.reset_world()


class Lightning(Action):
    # 15
    commands = "zap",

    @classmethod
    def action(cls, command, parser):
        target = parser.user.find(parser.require_next("But who do you wish to blast into pieces....\n"))
        return parser.user.lightning(target)


class Eat(Action):
    # 16
    commands = "eat", "drink",

    @classmethod
    def action(cls, command, parser):
        item_name = parser.require_next("What\n")

        if parser.user.location_id == -609 and item_name == "water":
            item_name = "spring"

        if item_name == "from":
            item_name = next(parser)

        item = parser.user.get_item(item_name)
        return parser.user.eat(item)


class Play(Action):
    # 17
    commands = "play",

    @classmethod
    def action(cls, command, parser):
        item = parser.user.get_item(parser.require_next("Play what ?\n"))
        return parser.user.play(item)


class Shout(Action):
    # 18
    commands = "shout",

    @classmethod
    def action(cls, command, parser):
        return parser.user.shout(parser.full())


class Say(Action):
    # 19
    commands = "say",

    @classmethod
    def action(cls, command, parser):
        return parser.user.say(parser.full())


class Tell(Action):
    # 20
    commands = "tell",

    @classmethod
    def action(cls, command, parser):
        player = parser.user.find(parser.require_next("Tell who ?\n"))
        return parser.user.tell(player, parser.full())


class Save(Action):
    # 21
    commands = "save",

    @classmethod
    def action(cls, command, parser):
        return parser.user.save()


class Score(Action):
    # 22
    commands = "score",

    @classmethod
    def action(cls, command, parser):
        return parser.user.show_score()


class Exorcise(Action):
    # 23
    commands = "exorcise",

    @classmethod
    def action(cls, command, parser):
        player = parser.user.find(parser.require_next("Exorcise who ?\n"))
        parser.user.exorcise(player)


class Give(Action):
    # 24
    commands = "give",

    @classmethod
    def action(cls, command, parser):
        word = parser.require_next("Give what to who ?\n")
        player = parser.user.find(word)
        if player is None:
            item = parser.user.get_item(word)

            player_name = parser.require_next("But to who ?\n")
            if player_name == "to":
                player_name = parser.require_next("But to who ?\n")

            player = parser.user.find(player_name)
            if player is None:
                raise CommandError("I don't know who {} is\n".format(player_name))
        else:
            item = parser.user.get_item(parser.require_next("Give them what ?\n"))

        return parser.user.give(item, player)


class Steal(Action):
    # 25
    commands = "steal","pinch",

    @classmethod
    def action(cls, command, parser):
        item_name = parser.require_next("Steal what from who ?\n")

        player_name = parser.require_next("From who ?\n")
        if player_name == "from":
            player_name = parser.require_next("From who ?\n")
        player = parser.user.find(player_name)

        item = find_item(
            item_name,
            owner=player,
            destroyed=parser.user.is_wizard,
        )
        return parser.user.steal(item, player)


class Tss(Action):
    # 151
    commands = "tss",

    @classmethod
    def action(cls, command, parser):
        return parser.user.tss(parser.full())


class RmEdit(Action):
    # 152
    commands = "rmedit",

    @classmethod
    def action(cls, command, parser):
        return parser.user.remote_editor()


class USystem(Action):
    # 156
    commands = "honeyboard",

    @classmethod
    def action(cls, command, parser):
        return parser.user.honeyboard()


class INumber(Action):
    # 157
    commands = "inumber",

    @classmethod
    def action(cls, command, parser):
        item = find_item(parser.require_next("What...\n"), destroyed=parser.user.is_wizard)
        return parser.user.item_number(item)


class Update(Action):
    # 158
    commands = "update",

    @classmethod
    def action(cls, command, parser):
        return parser.user.update_system()


class Become(Action):
    # 159
    commands = "become",

    @classmethod
    def action(cls, command, parser):
        return parser.user.become(parser.full())


class SysStat(Action):
    # 160
    commands = "systat",

    @classmethod
    def action(cls, command, parser):
        return parser.user.sys_stat()


class Converse(Action):
    # 161
    commands = "converse",

    @classmethod
    def action(cls, command, parser):
        return parser.user.converse()


class Shell(Action):
    # 163
    commands = "shell",

    @classmethod
    def action(cls, command, parser):
        return parser.user.shell()


class Raw(Action):
    # 164
    commands = "raw",

    @classmethod
    def action(cls, command, parser):
        return parser.user.raw(parser.full())


class Roll(Action):
    # 168
    commands = "roll",

    @classmethod
    def action(cls, command, parser):
        return parser.user.roll(parser.get_item())


class Credits(Action):
    # 169
    commands = "credits",

    @classmethod
    def action(cls, command, parser):
        return parser.user.credits()


class Brief(Action):
    # 170
    commands = "brief",

    @classmethod
    def action(cls, command, parser):
        return parser.user.switch_brief()


class Debug(Action):
    # 171
    commands = "debug",

    @classmethod
    def action(cls, command, parser):
        return parser.user.debug()


class MapWorld(Action):
    # 173
    commands = "map",

    @classmethod
    def action(cls, command, parser):
        return parser.user.map_world()


class Flee(Go):
    # 174
    commands = "flee",

    @classmethod
    def action(cls, command, parser):
        return cls.get_direction(parser).flee(command, parser)


class Bug(Action):
    # 175
    commands = "bug",

    @classmethod
    def action(cls, command, parser):
        return parser.user.bug(parser.full())


class Typo(Action):
    # 176
    commands = "typo",

    @classmethod
    def action(cls, command, parser):
        return parser.user.typo(parser.full())


class Pronouns(Action):
    # 177
    commands = "pn",

    @classmethod
    def action(cls, command, parser):
        return parser.user.list_pronouns()


class DebugMode(Action):
    # 180
    commands = "debugmode",

    @classmethod
    def action(cls, command, parser):
        parser.user.switch_debug()


class SetIn(Action):
    # 183
    commands = "setin",

    @classmethod
    def action(cls, command, parser):
        parser.user.set_in(parser.full())


class SetOut(Action):
    # 184
    commands = "setout",

    @classmethod
    def action(cls, command, parser):
        parser.user.set_out(parser.full())


class SetMin(Action):
    # 185
    commands = "setmin",

    @classmethod
    def action(cls, command, parser):
        parser.user.set_magic_in(parser.full())


class SetMout(Action):
    # 186
    commands = "setmout",

    @classmethod
    def action(cls, command, parser):
        parser.user.set_magic_out(parser.full())


class Dig(Action):
    # 188
    commands = "dig",

    @classmethod
    def action(cls, command, parser):
        parser.user.dig()


class Empty(Action):
    # 189
    commands = "empty",

    @classmethod
    def action(cls, command, parser):
        return parser.user.empty(parser.get_item())