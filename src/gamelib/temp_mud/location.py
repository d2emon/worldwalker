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
            return Indoors
        elif -179 <= self.location_id <= -199:
            return ClimateWarm
        elif -100 <= self.location_id <= -178:
            return ClimateCold
        else:
            return Climate

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

    # Unknown
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
        yield from self.climate.weather(self.weather.state)

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
