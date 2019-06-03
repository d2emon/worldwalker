from .weather_data import WEATHER_RAIN, WEATHER_TEXT
from .zone import Zone


class Location:
    CLIMATE_DEFAULT = 0
    CLIMATE_WARM = 1
    CLIMATE_COLD = 2

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
    def climate(self):
        if -179 <= self.location_id <= -199:
            return self.CLIMATE_WARM
        elif -100 <= self.location_id <= -178:
            return self.CLIMATE_COLD
        else:
            return self.CLIMATE_DEFAULT

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
        if not self.outdoors:
            return

        weather_id = self.validate_weather_id(weather_id)
        if weather_id == WEATHER_RAIN:
            if self.climate == self.CLIMATE_WARM:
                yield "It is raining, a gentle mist of rain, which sticks to everything around\n"
                yield "you making it glisten and shine. High in the skies above you is a rainbow\n"
            else:
                yield "\001cIt is raining\n\001"
        else:
            yield WEATHER_TEXT.get(weather_id, "")

    def validate_weather_id(self, weather_id):
        if self.CLIMATE_WARM:
            weather_id %= 2
        elif self.CLIMATE_COLD:
            if weather_id in (1, 2):
                weather_id += 2
        return weather_id
