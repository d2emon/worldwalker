from .errors import CommandError
from .item.item import Item
from .weather import Weather, Indoors, Climate, ClimateCold, ClimateWarm
from .zone import Zone


class Location:
    directions = [
        "North",
        "East ",
        "South",
        "West ",
        "Up   ",
        "Down ",
    ]

    def __init__(self, location_id):
        self.location_id = location_id
        # Zones
        self.exits = [0] * 7
        # Weather
        self.weather = Weather()
        # Unknown
        self.__zone = None

        self.death_room = False
        self.no_brief = False
        self.short = ""
        self.description = []

    @property
    def climate(self):
        if not self.outdoors:
            return Indoors.climate()
        elif -179 <= self.location_id <= -199:
            return ClimateWarm.climate()
        elif -100 <= self.location_id <= -178:
            return ClimateCold.climate()
        else:
            return Climate.climate()

    @property
    def in_zone(self):
        return self.zone.in_zone(self.location_id)

    @property
    def is_dark(self):
        if self.location_id in (-1100, -1101):
            return False
        if -1113 >= self.location_id >= -1123:
            return True
        if self.location_id < -399 or self.location_id > -300:
            return False
        return True

    @property
    def items(self):
        return [item for item in ITEMS if item.location == self.location_id]

    # Zones
    @property
    def name(self):
        return str(self.zone) + self.in_zone

    # Weather
    @property
    def outdoors(self):
        if self.location_id in [-100, -101, -102]:
            return True
        elif self.location_id in [-170, -183]:
            return True
        elif -168 > self.location_id > -191:
            return True
        elif -181 > self.location_id > -172:
            return True
        else:
            return False

    # Unknown
    @property
    def visible_exits(self):
        return [e for e in self.exits if e < 0]

    @property
    def zone(self):
        if self.__zone is None:
            self.__zone = Zone.find(self.location_id)
        return self.__zone

    # Parse
    @property
    def __filename(self):
        return "{}{}".format(ROOMS, -self.location_id)

    def load(self, mode):
        return fopen(self.__filename, mode)

    # Zones
    @classmethod
    def find(cls, user, name, offset=1):
        zone = Zone.by_name(name)
        if zone is None:
            return 0

        user.set_wd_there(name, offset)

        if not offset:
            offset = 1
        else:
            offset = int(offset)

        return cls(-zone.location_id(offset))

    # Unknown
    @property
    def __items(self):
        return [item for item in ITEMS if item.is_in_location(self)]

    def __list_items(self, flannel):
        for item in (item for item in self.items if item.flannel == flannel and item.state <= 3):
            if not item.description:
                continue
            # OLONGT NOTE TO BE ADDED
            if item.is_destroyed:
                yield "--"

            yield item.show_description(user.debug_mode) + "\n"
            wd_it = item.name

    def list_items(self):
        yield from self.__list_items(1)
        yield self.weather_description()
        yield from self.__list_items(0)

    def list_people(self):
        for player in PLAYERS:
            if player.player_id == user.player_id:
                continue
            if not player.exists:
                continue
            if player.location_id != self.location_id:
                continue
            if not seeplayer(player):
                continue

            yield "{} ".format(player.name)
            if user.debug_mode:
                yield "{{{}}}".format(player.player_id)
            yield player.level_name
            if player.sex == player.SEX_FEMALE:
                wd_her = player.name
            else:
                wd_him = player.name
            yield " is here carrying\n"
            yield from player.list_items()

    def load_exits(self, file):
        self.exits = [file.scanf() for _ in range(6)]

    def get_name(self, user):
        user.set_wd_there(self.zone, self.in_zone)
        result = self.name
        if user.is_god:
            result += "[ {} ]".format(self.location_id)
        return result + "\n"

    # Weather
    def weather_description(self):
        yield from self.climate.weather

    # Tk
    def reload(self):
        self.death_room = False
        self.no_brief = False
        self.short = ""
        self.description = ""
        try:
            data = self.load("r")
            self.load_exits(data)
            for s in data:
                if s == "#DIE":
                    self.death_room = True
                elif s == "#NOBR":
                    self.no_brief = True
                elif self.short is None:
                    self.short = s
                else:
                    self.description += s + "\n"
            data.disconnect()
        except FileNotFoundError:
            self.short = "\nYou are on channel {}\n".format(self.location_id)

    # Events
    def on_dig_here(self, actor):
        events = [event for event in map(lambda item: item.on_dig_here(self), ITEMS) if event is not None]
        if events:
            yield from events
            return

        if self.location_id not in (-172, -192):
            raise CommandError("You find nothing.\n")

    def on_drop(self, actor, item):
        if self.location_id in [-5, -183]:
            yield "It disappears down into the bottomless pit.....\n"
            actor.send_global("The {} disappears into the bottomless pit.\n".format(item.name))
            actor.score += tscale() * item.base_value / 5
            yield from actor.update()
            item.set_location(-6, 0)

    def on_enter(self, actor):
        if self.location_id == -139:
            if actor.has_shield:
                yield "The shield protects you from the worst of the lava stream's heat\n"
            else:
                raise CommandError("The intense heat drives you back\n")

    def on_take_item(self, actor, item):
        if self.location_id == -1081:
            Item(20).state = 1
            yield "The door clicks shut....\n"
