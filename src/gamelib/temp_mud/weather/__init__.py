"""
The next part of the universe...
"""
from ..item import Item
from ..message import message_codes
from ..message.message import Message
from ..weather_data import WEATHER_RAIN, WEATHER_START, WEATHER_TEXT

"""
Weather Routines
 
Current weather defined by state of object 47
 
states are
 
0   Sunny
1   Rain
2   Stormy
3   Snowing
"""


class Weather(Item):
    def __init__(self):
        super().__init__(0)

    @property
    def user(self):
        raise NotImplementedError()

    # Weather
    @property
    def weather_id(self):
        return self.state

    @weather_id.setter
    def weather_id(self, value):
        if self.state == value:
            return
        self.state = value
        Message(
            None,
            None,
            message_codes.WEATHER,
            None,
            value,
        ).send(self.user)

    # Weather
    def __iter__(self):
        return self

    def __next__(self):
        chance = random_percent()
        if chance < 50:
            self.weather_id = 1
        elif chance > 90:
            self.weather_id = 2
        else:
            self.weather_id = 0


class Climate:
    __climate = None
    __weather = Weather()
    __weather_id = None

    @property
    def weather_id(self):
        return self.__weather.state

    @property
    def weather(self):
        return WEATHER_TEXT.get(self.weather_id, "")

    @classmethod
    def climate(cls):
        if cls.__climate is None:
            cls.__climate = cls()
        return cls.__climate


class ClimateWarm(Climate):
    __climate = None

    @property
    def weather_id(self):
        return self.__weather.state % 2

    @property
    def weather(self):
        if self.weather_id == WEATHER_RAIN:
            return "It is raining, a gentle mist of rain, which sticks to everything around\n" \
                   "you making it glisten and shine. High in the skies above you is a rainbow\n"
        return super().weather


class ClimateCold(Climate):
    __climate = None

    @property
    def weather_id(self):
        weather = self.__weather.state
        return weather + 2 if weather in (1, 2) else weather


class Indoors(Climate):
    __climate = None

    @property
    def weather(self):
        return None
