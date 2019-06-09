from .errors import CrapupError, ServiceError, CommandError, LooseError
from .item import Item, Door
from .location import Location
from .message import Broadcast, Message, Silly
from .player import Player
from .syslog import syslog
from .world import World


DIRECTIONS = [
    "north",
    "east",
    "south",
    "west",
    "up",
    "down",
]


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
    def quit_game(self):
        if self.Disease.is_force:
            raise CommandError("You can't be forced to do that\n")

        yield from self.read_messages()

        if self.Blood.in_fight:
            raise CommandError("Not in the middle of a fight!\n")

        yield "Ok"
        World.load()
        self.send_message(
            self,
            Message.GLOBAL,
            self.location_id,
            "{} has left the game\n".format(self.name)
        )
        self.send_message(
            self,
            Message.WIZARD,
            0,
            "[ Quitting Game : {} ]\n".format(self.name)
        )
        dumpitems()
        self.player.die()
        self.player.remove()
        World.save()
        self.location_id = 0
        self.show_players = False

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

    def go_in_direction(self, direction_id):
        if self.Blood.in_fight > 0:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")

        golem = Player(25)
        if Item(32).iscarrby(self) and golem.exists and golem.location == self.location_id:
            raise CommandError("\001cThe Golem\001 bars the doorway!\n")

        self.Disease.crippled.check()

        new_location = self.location.exits[direction_id]
        if 999 < new_location < 2000:
            door = Door(new_location)
            new_location = door.go_through()
            if new_location >= 0:
                if self.in_dark or door.invisible:
                    raise CommandError("You can't go that way\n")  # Invis doors
                else:
                    raise CommandError("The door is not open\n")
        if new_location == -139:
            shields = Item(113), Item(114), Item(89)
            if any(item.iswornby(self) for item in shields):
                yield "The shield protects you from the worst of the lava stream's heat\n"
            else:
                raise CommandError("The intense heat drives you back\n")
        if direction_id == 2:
            sorcerors = Item(101), Item(102), Item(103)
            figure = Player.fpbns("figure")
            if figure is not None and figure != self and figure.location == self.location_id:
                if any(item.iswornby(self.player) for item in sorcerors):
                    raise CommandError("\001pThe Figure\001 holds you back\n"
                                       "\001pThe Figure\001 says 'Only true sorcerors may pass'\n")
        if new_location >= 0:
            raise CommandError("You can't go that way\n")

        self.send_message(
            self,
            Message.GLOBAL,
            self.location_id,
            "\001s{user.player.name}\001{user.name} has gone {direction} {user.out_ms}.\n\001".format(
                user=self,
                direction=DIRECTIONS[direction_id],
            ),
        )
        self.send_message(
            self,
            Message.GLOBAL,
            new_location,
            "\001s{user.name}\001{user.name}{user.in_ms}.\n\001".format(
                user=self,
                direction=DIRECTIONS[direction_id],
            ),
        )
        self.location = new_location

    def lightning(self, victim):
        if victim is None:
            raise CommandError("There is no one on with that name\n")
        self.send_message(victim.name, -10001, victim.location, "")
        syslog("{} zapped {}".format(self.name, victim.name))
        if victim.is_mobile:
            woundmn(victim, 10000)
            # DIE
        self.broadcast("\001dYou hear an ominous clap of thunder in the distance\n\001")

    def eat(self, item):
        if item is None:
            raise CommandError("There isn't one of those here\n")
        elif item.item_id == 11:
            yield "You feel funny, and then pass out\n"
            yield "You wake up elsewhere....\n"
            self.teleport(-1076)
        elif item.item_id == 75:
            yield "very refreshing\n"
        elif item.item_id == 175:
            if self.NewUaf.level < 3:
                self.NewUaf.score += 40
                yield "You feel a wave of energy sweeping through you.\n"
            else:
                yield "Faintly magical by the taste.\n"
                if self.NewUaf.strength < 40:
                    self.NewUaf.strength += 2
            yield from self.update()
        else:
            if item.is_edible:
                item.destroy()
                yield "Ok....\n"
                self.NewUaf.strength += 12
                yield from self.update()
            else:
                yield "Thats sure not the latest in health food....\n"

    def play(self, item):
        if item is None:
            raise CommandError("That isn't here\n")
        if not self.item_is_available(item):
            raise CommandError("That isn't here\n")

    def shout(self, text):
        self.send_message(
            self,
            -10104 if self.is_wizard else -10002,
            self.location_id,
            text,
        )
        yield "Ok!"

    def say(self, text):
        self.send_message(
            self,
            -10003,
            self.location_id,
            text,
        )
        yield "You say '{}'\n".format(text)

    def tell(self, player, text):
        if player is None:
            raise CommandError("No one with that name is playing\n")
        self.send_message(player, -10004, self.location_id, text)
