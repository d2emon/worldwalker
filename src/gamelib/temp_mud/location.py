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
        self.weather = Weather()
        self.__zone = None

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

    def show_weather(self, weather_id):
        yield from self.climate.show_weather(weather_id)
