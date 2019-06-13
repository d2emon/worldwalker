from ..errors import CommandError, CrapupError, ServiceError
from ..item import Item
from ..player.player import Player
from ..syslog import syslog
from ..world import World
from .action import Action, ActionList


class Direction(Action):
    direction_id = None

    @classmethod
    def action(cls, command, parser):
        if cls.direction_id is None:
            raise CommandError("Thats not a valid direction\n")
        return parser.user.go(cls.direction_id)


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
            item = Item.fobna(parser.require_next("In what ?\n"))
            return parser.user.look_in(item)


class Reset(Action):
    # 14
    full_match = True
    commands = "reset",
    wizard_only = "What ?\n"

    @classmethod
    def action(cls, command, parser):
        return parser.user.reset_world()


class Lightning(Action):
    # 15
    commands = "zap",
    wizard_only = "Your spell fails.....\n"

    @classmethod
    def action(cls, command, parser):
        victim = Player.fpbn(parser.require_next("But who do you wish to blast into pieces....\n"))
        return parser.user.lightning(victim)


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

        item = Item.fobna(item_name)
        return parser.user.eat(item)


class Play(Action):
    # 17
    commands = "play",

    @classmethod
    def action(cls, command, parser):
        item = Item.fobna(parser.require_next("Play what ?\n"))
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
        player = Player.fpbn(parser.require_next("Tell who ?\n"))
        return parser.user.tell(player, parser.full())


class Score(Action):
    # 22
    commands = "score",

    @classmethod
    def action(cls, command, parser):
        return parser.user.show_score()


class Exorcise(Action):
    # 23
    commands = "exorcise",
    wizard_only = "No chance....\n"

    @classmethod
    def action(cls, command, parser):
        player = Player.fpbn(parser.require_next("Exorcise who ?\n"))
        parser.user.exorcise(player)


class Give(Action):
    # 24
    commands = "give",

    @classmethod
    def action(cls, command, parser):
        word = parser.require_next("Give what to who ?\n")
        player = Player.fpbn(word)
        if player is None:
            item = Item.fobna(word)

            player_name = parser.require_next("But to who ?\n")
            if player_name == "to":
                player_name = parser.require_next("But to who ?\n")

            player = Player.fpbn(player_name)
            if player is None:
                raise CommandError("I don't know who {} is\n".format(player_name))
        else:
            item = Item.fobna(parser.require_next("Give them what ?\n"))
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
        player = Player.fpbn(player_name)

        item = Item.fobncb(item_name, player)
        return parser.user.steal(item, player)


class Grope(Action):
    # 139
    commands = "grope",

    @classmethod
    def validate(cls, command, parser):
        if parser.user.Blood.in_fight:
            raise CommandError("Not in a fight!\n")
        return True

    @classmethod
    def action(cls, command, parser):
        return gropecom()


class Tss(Action):
    # 151
    commands = "tss",
    god_only = "I don't know that verb\n"

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
    wizard_only = "You'll have to leave the game first!\n"

    @classmethod
    def action(cls, command, parser):
        return parser.user.honeyboard()


class INumber(Action):
    # 157
    commands = "inumber",
    god_only = "Huh ?\n"

    @classmethod
    def action(cls, command, parser):
        item = Item.fobn(parser.require_next("What...\n"))
        return parser.user.inumber(item)


class Update(Action):
    # 158
    commands = "update",
    wizard_only = "Hmmm... you can't do that one\n"

    @classmethod
    def action(cls, command, parser):
        parser.user.update_system()


class Become(Action):
    # 159
    commands = "become",
    wizard_only = "Become what ?\n"

    @classmethod
    def action(cls, command, parser):
        x2 = parser.full()
        if not x2:
            raise CommandError("To become what ?, inebriated ?\n")
        parser.user.send_message(
            parser.user,
            message_codes.MSG_WIZARD,
            0,
            "{} has quit, via BECOME\n".format(parser.user.name),
        )

        keysetback()
        parser.user.loose()
        World.save()

        try:
            execl(EXE2, "   --}----- ABERMUD ------   ", "-n{}".format(parser.user.name))  # GOTOSS eek!
        except ServiceError:
            yield "Eek! someone's just run off with mud!!!!\n"


class SysStat(Action):
    # 160
    commands = "systat",

    @classmethod
    def action(cls, command, parser):
        if parser.user.level < 10000000:
            raise CommandError("What do you think this is a DEC 10 ?\n")


class Converse(Action):
    # 161
    commands = "converse",

    @classmethod
    def action(cls, command, parser):
        parser.conversation_mode = parser.CONVERSATION_SAY
        yield "Type '**' on a line of its own to exit converse mode\n"


class Shell(Action):
    # 163
    commands = "shell",
    god_only = "There is nothing here you can shell\n"

    @classmethod
    def action(cls, command, parser):
        parser.conversation_mode = parser.CONVERSATION_TSS
        yield "Type ** on its own on a new line to exit shell\n"


class Raw(Action):
    # 164
    commands = "raw",
    god_only = "I don't know that verb\n"

    @classmethod
    def action(cls, command, parser):
        raw = parser.full()
        if parser.user.level == 10033 and raw[0] == "!":
            parser.user.broadcast(raw[1:])
        else:
            parser.user.broadcast("** SYSTEM : {}\n\007\007".format(raw))


class Roll(Action):
    # 168
    commands = "roll",

    @classmethod
    def action(cls, command, parser):
        # item = get_item(parser)
        item = parser.ohereandget()
        if item is None:
            return
        if item.item_id in [122, 123]:
            parser.gamecom("push pillar")
        else:
            raise CommandError("You can't roll that\n")


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
        parser.user.switch_brief()


class Debug(Action):
    # 171
    commands = "debug",
    god_only = "I don't know that verb\n"

    @classmethod
    def action(cls, command, parser):
        return debug2()


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
        yield from parser.user.flee()
        return Go.execute(command, parser)


class Bug(Action):
    # 175
    commands = "bug",

    @classmethod
    def action(cls, command, parser):
        syslog("Bug by {} : {}".format(parser.user.name, parser.full()))


class Typo(Action):
    # 176
    commands = "typo",

    @classmethod
    def action(cls, command, parser):
        syslog("Typo by {} in {} : {}".format(parser.user.name, parser.user.location_id, parser.full()))


class DebugMode(Action):
    # 180
    commands = "debugmode",

    @classmethod
    def action(cls, command, parser):
        parser.switch_debug()


class SetMessage(Action):
    @classmethod
    def validate(cls, command, parser):
        if not parser.user.is_god and parser.user.name != "Lorry":
            raise CommandError("No way !\n")


class SetIn(SetMessage):
    # 183
    commands = "setin",

    @classmethod
    def action(cls, command, parser):
        parser.user.in_ms = parser.full()


class SetOut(SetMessage):
    # 184
    commands = "setout",

    @classmethod
    def action(cls, command, parser):
        parser.user.out_ms = parser.full()


class SetMin(SetMessage):
    # 185
    commands = "setmin",

    @classmethod
    def action(cls, command, parser):
        parser.user.min_ms = parser.full()


class SetMout(SetMessage):
    # 186
    commands = "setmout",

    @classmethod
    def action(cls, command, parser):
        parser.user.mout_ms = parser.full()


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
        # container = get_item(parser)
        container = parser.ohereandget()
        if container is None:
            return
        for item in Item.items():
            if not item.iscontin(container):
                item.set_location(parser.user.location_id, 1)
                yield "You empty the {} from the {}\n".format(item.name, container.name)
                parser.gamecom("drop {}".format(item.name))
                pbfr()
                World.load()
