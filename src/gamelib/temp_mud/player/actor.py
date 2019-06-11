from ..errors import CommandError
from ..item import Item, Door
from ..location import Location
from ..message import message_codes
from .mobile import MOBILES


DIRECTIONS = {
    0: "north",
    1: "east",
    2: "south",
    3: "west",
    4: "up",
    5: "down",
}


def is_door(location_id):
    return 999 < location_id < 2000


class Actor:
    @property
    def Blood(self):
        raise NotImplementedError()

    @property
    def Disease(self):
        raise NotImplementedError()

    @property
    def location_id(self):
        raise NotImplementedError()

    @location_id.setter
    def location_id(self, value):
        raise NotImplementedError()

    @property
    def in_ms(self):
        raise NotImplementedError()

    @property
    def out_ms(self):
        raise NotImplementedError()

    def send_message(self, *args):
        raise NotImplementedError()

    @property
    def has_shield(self):
        shields = Item(113), Item(114), Item(89)
        return any(item.iswornby(self) for item in shields)

    @property
    def in_fight(self):
        return self.Blood.in_fight > 0

    @property
    def location(self):
        return Location(self.location_id)

    def send_global(self, message):
        self.send_message(
            self,
            message_codes.GLOBAL,
            self.location_id,
            message,
        )

    # 1 - 10
    def go(self, direction_id):
        def get_location_id(new_location_id):
            return new_location_id

        # 1 - 7
        direction = DIRECTIONS.get(direction_id)
        if direction is None:
            raise CommandError("Thats not a valid direction\n")
        if self.in_fight > 0:
            raise CommandError("You can't just stroll out of a fight!\n"
                               "If you wish to leave a fight, you must FLEE in a direction\n")
        location_id = self.location.exits[direction_id]
        map(lambda mobile: mobile.on_actor_leave(self, direction_id), MOBILES)
        self.Disease.crippled.check()
        if is_door(location_id):
            location_id = Door(location_id).go_through(self)
        Location(location_id).on_enter(self)
        map(lambda mobile: mobile.on_actor_enter(self, direction_id, location_id), MOBILES)
        if location_id >= 0:
            raise CommandError("You can't go that way\n")

        self.send_global(
            "\001s{actor.data.name}\001{actor.name} has gone {direction} {message}.\n\001".format(
                actor=self,
                direction=direction,
                message=self.out_ms
            ),
        )
        self.location_id = location_id
        self.send_global(
            "\001s{actor.name}\001{actor.name}{message}.\n\001".format(
                actor=self,
                # direction=direction,
                message=self.in_ms
            ),
        )

    def quit_game(self):
        raise NotImplementedError()

    def take(self):
        raise NotImplementedError()

    def drop(self):
        raise NotImplementedError()

    # 11 - 20
    def look(self):
        raise NotImplementedError()

    def inventory(self):
        raise NotImplementedError()

    def who(self):
        raise NotImplementedError()

    def reset_world(self):
        raise NotImplementedError()

    def zap(self):
        raise NotImplementedError()

    def eat(self):
        raise NotImplementedError()

    def play(self):
        raise NotImplementedError()

    def shout(self):
        raise NotImplementedError()

    def say(self):
        raise NotImplementedError()

    def tell(self):
        raise NotImplementedError()

    # 21 - 30
    def save(self):
        raise NotImplementedError()

    def score(self):
        raise NotImplementedError()

    def exorcise(self):
        raise NotImplementedError()

    def give(self):
        raise NotImplementedError()

    def steal(self):
        raise NotImplementedError()

    def levels(self):
        raise NotImplementedError()

    def help(self):
        raise NotImplementedError()

    def value(self):
        raise NotImplementedError()

    def stats(self):
        raise NotImplementedError()

    def examine(self):
        raise NotImplementedError()

    # 31 - 35
    def delete_player(self):
        raise NotImplementedError()

    def password(self):
        raise NotImplementedError()

    def summon(self):
        raise NotImplementedError()

    def wield(self):
        raise NotImplementedError()

    def kill(self):
        raise NotImplementedError()

    # 50
    def laugh(self):
        raise NotImplementedError()

    # 51 - 60
    def cry(self):
        raise NotImplementedError()

    def burp(self):
        raise NotImplementedError()

    def fart(self):
        raise NotImplementedError()

    def hiccup(self):
        raise NotImplementedError()

    def grin(self):
        raise NotImplementedError()

    def smile(self):
        raise NotImplementedError()

    def wink(self):
        raise NotImplementedError()

    def snigger(self):
        raise NotImplementedError()

    def pose(self):
        raise NotImplementedError()

    def set(self):
        raise NotImplementedError()

    # 61 - 66
    def pray(self):
        raise NotImplementedError()

    def storm(self):
        raise NotImplementedError()

    def rain(self):
        raise NotImplementedError()

    def sun(self):
        raise NotImplementedError()

    def snow(self):
        raise NotImplementedError()

    def go_to(self):
        raise NotImplementedError()

    # 100
    def wear(self):
        raise NotImplementedError()

    # 101 - 110
    def remove(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()

    def wave(self):
        raise NotImplementedError()

    def blizzard(self):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def lock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()

    def force(self):
        raise NotImplementedError()

    def light(self):
        raise NotImplementedError()

    # 111 - 120
    def extinguish(self):
        raise NotImplementedError()

    def where(self):
        raise NotImplementedError()

    # 113

    def invisible(self):
        raise NotImplementedError()

    def visible(self):
        raise NotImplementedError()

    # 116

    def push(self):
        raise NotImplementedError()

    def cripple(self):
        raise NotImplementedError()

    def cure(self):
        raise NotImplementedError()

    def dumb(self):
        raise NotImplementedError()

    # 121 - 130
    def change(self):
        raise NotImplementedError()

    def missile(self):
        raise NotImplementedError()

    def shock(self):
        raise NotImplementedError()

    def fireball(self):
        raise NotImplementedError()

    def translocate(self):
        raise NotImplementedError()

    def blow(self):
        raise NotImplementedError()

    def sigh(self):
        raise NotImplementedError()

    def kiss(self):
        raise NotImplementedError()

    def hug(self):
        raise NotImplementedError()

    def slap(self):
        raise NotImplementedError()

    # 131 - 140
    def tickle(self):
        raise NotImplementedError()

    def scream(self):
        raise NotImplementedError()

    def bounce(self):
        raise NotImplementedError()

    def wiz(self):
        raise NotImplementedError()

    def stare(self):
        raise NotImplementedError()

    def exits(self):
        raise NotImplementedError()

    def crash(self):
        raise NotImplementedError()

    def sing(self):
        raise NotImplementedError()

    def grope(self):
        raise NotImplementedError()

    def spray(self):
        raise NotImplementedError()

    # 141 - 150
    def groan(self):
        raise NotImplementedError()

    def moan(self):
        raise NotImplementedError()

    def directory(self):
        raise NotImplementedError()

    def yawn(self):
        raise NotImplementedError()

    def wizlist(self):
        raise NotImplementedError()

    def in_command(self):
        raise NotImplementedError()

    def smoke(self):
        raise NotImplementedError()

    def deafen(self):
        raise NotImplementedError()

    def ressurect(self):
        raise NotImplementedError()

    def log(self):
        raise NotImplementedError()

    # 151 - 160
    def tss(self):
        raise NotImplementedError()

    def rmedit(self):
        raise NotImplementedError()

    def loc(self):
        raise NotImplementedError()

    def squeeze(self):
        raise NotImplementedError()

    def users(self):
        raise NotImplementedError()

    def honeyboard(self):
        raise NotImplementedError()

    def inumber(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def become(self):
        raise NotImplementedError()

    def systat(self):
        raise NotImplementedError()

    # 161 - 170
    def converse(self):
        raise NotImplementedError()

    def snoop(self):
        raise NotImplementedError()

    def shell(self):
        raise NotImplementedError()

    def raw(self):
        raise NotImplementedError()

    def purr(self):
        raise NotImplementedError()

    def cuddle(self):
        raise NotImplementedError()

    def sulk(self):
        raise NotImplementedError()

    def roll(self):
        raise NotImplementedError()

    def credits(self):
        raise NotImplementedError()

    def brief(self):
        raise NotImplementedError()

    # 171 - 180
    def debug(self):
        raise NotImplementedError()

    def jump(self):
        raise NotImplementedError()

    def map(self):
        raise NotImplementedError()

    def flee(self):
        raise NotImplementedError()

    def bug(self):
        raise NotImplementedError()

    def typo(self):
        raise NotImplementedError()

    def pn(self):
        raise NotImplementedError()

    def blind(self):
        raise NotImplementedError()

    def patch(self):
        raise NotImplementedError()

    def debugmode(self):
        raise NotImplementedError()

    # 181 - 189
    def pflags(self):
        raise NotImplementedError()

    def frobnicate(self):
        raise NotImplementedError()

    def setin(self):
        raise NotImplementedError()

    def setout(self):
        raise NotImplementedError()

    def setmin(self):
        raise NotImplementedError()

    def setmout(self):
        raise NotImplementedError()

    def emote(self):
        raise NotImplementedError()

    def dig(self):
        raise NotImplementedError()

    def empty(self):
        raise NotImplementedError()
