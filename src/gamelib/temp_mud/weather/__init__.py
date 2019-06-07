"""
The next part of the universe...
"""
from gamelib.temp_mud.actions.action import Action
from ..errors import CommandError, NotFoundError
from ..item import Item
from ..message import MSG_WEATHER
from ..player import Player
from ..weather_data import WEATHER_SUN, WEATHER_RAIN, WEATHER_STORM, WEATHER_SNOW, WEATHER_BLIZZARD, WEATHER_START, \
    WEATHER_TEXT

"""
Weather Routines
 
Current weather defined by state of object 47
 
states are
 
0   Sunny
1   Rain
2   Stormy
3   Snowing
"""


class Climate:
    @classmethod
    def weather_description(cls, weather_id):
        return WEATHER_TEXT.get(weather_id, "")

    @classmethod
    def get_weather_id(cls, weather_id):
        return weather_id

    @classmethod
    def weather_start(cls, weather_id):
        return WEATHER_START.get(cls.get_weather_id(weather_id))

    @classmethod
    def weather(cls, weather_id):
        return cls.weather_description(cls.get_weather_id(weather_id))


class ClimateWarm(Climate):
    @classmethod
    def weather_description(cls, weather_id):
        if weather_id == WEATHER_RAIN:
            return "It is raining, a gentle mist of rain, which sticks to everything around\n" \
                   "you making it glisten and shine. High in the skies above you is a rainbow\n"
        return super().weather_description(weather_id)

    @classmethod
    def get_weather_id(cls, weather_id):
        return weather_id % 2


class ClimateCold(Climate):
    @classmethod
    def get_weather_id(cls, weather_id):
        if weather_id in (1, 2):
            return weather_id + 2
        return weather_id


class Indoors(Climate):
    @classmethod
    def weather_start(cls, weather_id):
        return None

    @classmethod
    def weather(cls, weather_id):
        return None


class Weather(Item):
    def __init__(self):
        super().__init__(0)

    def send_weather(self, user, new_weather):
        if self.state == new_weather:
            return

        self.state = new_weather
        user.send_message(user, MSG_WEATHER, None, new_weather)

    def autochange(self, user):
        chance = randperc()
        if chance < 50:
            return self.send_weather(user, 1)
        elif chance > 90:
            return self.send_weather(user, 2)
        else:
            return self.send_weather(user, 0)

    @classmethod
    def receive(cls, user, weather_id):
        if not user.location.outdoors():
            return

        yield user.location.climate.weather_start(weather_id)
