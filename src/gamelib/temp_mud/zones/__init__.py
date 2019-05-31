"""
Zone based name generator
"""


class User:
    wd_there = ""
    __location_id = 0

    class NewUaf:
        my_lev = 0

    @property
    def is_wizard(self):
        return self.NewUaf.my_lev > 9

    @property
    def is_god(self):
        return self.NewUaf.my_lev > 9999

    @property
    def location(self):
        return Location(self.__location_id)

    def set_wd_there(self, zone, location_id):
        self.wd_there = zone + " " + location_id


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
        self.exits = [0] * 7
        self.__zone = None

    @property
    def in_zone(self):
        return self.zone.in_zone(self.location_id)

    @property
    def name(self):
        return str(self.zone) + self.in_zone

    @property
    def zone(self):
        if self.__zone is None:
            self.__zone = Zone.find(self.location_id)
        return self.__zone

    def load_exits(self, file):
        self.exits = [file.scanf() for _ in range(6)]

    def show_name(self, user):
        user.set_wd_there(self.zone, self.in_zone)
        result = self.name
        if user.is_god:
            result += "[ {} ]".format(self.location_id)
        yield result + "\n"


class Zone:
    def __init__(self, name, last=0):
        self.name = name
        self.last = last

    @property
    def first(self):
        if not self.last:
            return 0

        zones = list(filter(lambda z: z.last < self.last, ZONES))
        if len(zones) < 1:
            return 0
        return zones[-1].last + 1

    def __str__(self):
        return self.name

    def in_zone(self, location_id):
        if not self.first:
            return 0

        return location_id - self.first

    def location_id(self, offset):
        if not offset:
            return 0
        location_id = self.first + offset - 1
        return location_id if location_id <= self.last else 0

    @classmethod
    def find(cls, channel_id):
        location_id = -channel_id
        if location_id <= 0:
            return DEFAULT_ZONE

        zones = list(filter(lambda z: z.first < location_id < z.last, ZONES))
        return DEFAULT_ZONE if len(zones) < 1 else zones[0]

    @classmethod
    def by_name(cls, name):
        zones = list(filter(lambda z: z.name.lower() == name, ZONES))

        if len(zones) < 1:
            return None
        return zones[0]


DEFAULT_ZONE = Zone("TCHAN")
ZONES = [
    Zone("LIMBO", 1),
    Zone("WSTORE", 2),
    Zone("HOME", 4),
    Zone("START", 5),
    Zone("PIT", 6),
    Zone("WIZROOM", 19),
    Zone("DEAD", 99),
    Zone("BLIZZARD", 299),
    Zone("CAVE", 399),
    Zone("LABRNTH", 499),
    Zone("FOREST", 599),
    Zone("VALLEY", 699),
    Zone("MOOR", 799),
    Zone("ISLAND", 899),
    Zone("SEA", 999),
    Zone("RIVER", 1049),
    Zone("CASTLE", 1069),
    Zone("TOWER", 1099),
    Zone("HUT", 1101),
    Zone("TREEHOUSE", 1105),
    Zone("QUARRY", 2199),
    Zone("LEDGE", 2299),
    Zone("INTREE", 2499),
    Zone("WASTE", 99999),
]


def roomnum(user, name, offset=1):
    zone = Zone.by_name(name)
    if zone is None:
        return 0

    user.set_wd_there(name, offset)

    if not offset:
        return -zone.location_id(1)

    return -zone.location_id(int(offset))


class Exits:
    @classmethod
    def action(cls, user):
        yield "Obvious exits are\n"

        exits = list(filter(lambda l: l < 0, user.location.exits))

        if not len(exits):
            yield "None....\n"
            return

        for direction_id, location_id in enumerate(exits):
            if location_id >= 0:
                continue
            direction = Location.directions[direction_id]
            yield direction
            if user.is_wizard:
                yield " : {}".format(Location(location_id).name)
            yield "\n"


class Loc:
    @classmethod
    def validate(cls, user):
        if not user.is_wizard:
            raise Exception("Oh go away, thats for wizards\n")

    @classmethod
    def action(cls, user):
        yield "\nKnown Location Nodes Are\n\n"
        for zone_id, zone in enumerate(ZONES):
            yield zone.name
            if zone_id % 4 == 3:
                yield "\n"
        yield "\n"
