# Weather
def set_weather(user, message):
    if not user.location.outdoors():
        return

    yield user.location.climate.weather_start(message.message)
