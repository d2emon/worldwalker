from ..weather_data import WEATHER_START


# Weather
def set_weather(user, message):
    if not user.location.outdoors():
        return

    yield WEATHER_START.get(message.message)
