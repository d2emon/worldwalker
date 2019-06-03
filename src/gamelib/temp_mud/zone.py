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
